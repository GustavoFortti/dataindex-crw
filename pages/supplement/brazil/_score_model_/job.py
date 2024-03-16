import importlib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.model_selection import KFold

from utils.wordlist import WORDLIST
from config.env import LOCAL
from utils.log import message

from utils.general_functions import (
    get_all_dfs_in_dir,
    create_directory_if_not_exists,
    flatten_list
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

CONF = {
    "name": "_score_models_ ",
    "languages": ['pt_br'],
    "wordlist": WORDLIST["supplement"],
    "data_path": f"{LOCAL}/data/supplement/brazil/_score_model_",
}

pd.set_option('display.max_rows', None)

def run(args):
    global DATA_PATH_FILE_SYSTEM
    global DATA_PATH
    global WORDLIST

    print("JOB_NAME: " + CONF["name"])
    CONF.update(vars(args))
    DATA_PATH_FILE_SYSTEM = (f'{LOCAL}/data/supplement/brazil')
    MODELS_PATH = (f'{LOCAL}/data/supplement/brazil/_score_model_')
    WORDLIST = CONF['wordlist']
    DATA_PATH = CONF['data_path']

    create_directory_if_not_exists(MODELS_PATH)

    message("READ all score_model.csv")
    df = get_all_dfs_in_dir(DATA_PATH_FILE_SYSTEM, "score_model")

    message("exec data_prep")
    df_train, df_predictic, df_validation = data_prep(df)

    message("load train")
    model = run_score_train(df_train)

    message("run predict")
    df = run_score_predict(df_predictic, model)

    df = pd.merge(df, df_validation, on=['ref', 'subject_encoded', 'location'])

    # df.to_csv("./scores.csv")
    # df = pd.read_csv("./scores.csv")

    df = prepare_score(df)

    df.to_csv(f"{DATA_PATH}/model_result.csv")

def prepare_score(df):
    aggregated_df = df.groupby(['ref', 'subject_encoded']).agg({
        'location': 'sum',
        'product_predicted': 'sum',
        'probability_class_0': 'sum',
        'probability_class_1': 'sum',
        'subject': unique_subject,
    }).reset_index()
    
    df = aggregated_df.sort_values(by=['ref', 'product_predicted', 'probability_class_1'])
    df = df[df['product_predicted'] != 0]

    max_prob_by_ref = df.groupby('ref')['probability_class_1'].max()
    threshold_by_ref = max_prob_by_ref * 0.25

    df = df[df.apply(lambda row: row['probability_class_1'] > threshold_by_ref[row['ref']], axis=1)].reset_index(drop=True)
    df = df[['ref', 'subject']]

    for idx, row in df.iterrows():
        for item in WORDLIST.values():
            if (row['subject'] in item['subject']):
                row['subject'] = ", ".join(item['subject'])

    return df

def unique_subject(subjects):
    unique_subjects = set()
    for subject in subjects:
        cleaned_subject = subject.strip()
        unique_subjects.add(cleaned_subject)
    return ' '.join(unique_subjects)

def run_score_train(df):
    X = df.drop(['target', 'ref'], axis=1)
    y = df['target']

    model = train_and_evaluate_models(X, y)

    return model

def run_score_predict(df, model):
    df_temp = df.copy()
    X_predict = df_temp.drop(['target', 'ref'], axis=1)
    
    y_pred = model.predict(X_predict)
    y_probability = model.predict_proba(X_predict)

    df['product_predicted'] = y_pred
    df['probability_class_0'] = y_probability[:, 0]
    df['probability_class_1'] = y_probability[:, 1]

    return df[['ref', 'location', 'subject_encoded', 'product_predicted', 'probability_class_0', 'probability_class_1']]

def train_and_evaluate_models(X, y, n_splits=5):
    # Define o modelo
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=200, random_state=42)
    
    # Inicializa o KFold
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Listas para armazenar os resultados de cada fold
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    aucs = []

    # Loop sobre os folds
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # Treina o modelo
        model.fit(X_train, y_train)
        # Faz predições
        y_pred = model.predict(X_test)
        
        # Calcula as métricas
        accuracies.append(accuracy_score(y_test, y_pred))
        precisions.append(precision_score(y_test, y_pred, average='binary'))
        recalls.append(recall_score(y_test, y_pred, average='binary'))
        f1_scores.append(f1_score(y_test, y_pred, average='binary'))
        aucs.append(roc_auc_score(y_test, y_pred))

    # Calcula a média das métricas
    print("RESULTADOS MÉDIOS K-FOLD:")
    print(f'Accuracy: {np.mean(accuracies)}')
    print(f'Precision: {np.mean(precisions)}')
    print(f'Recall: {np.mean(recalls)}')
    print(f'F1 Score: {np.mean(f1_scores)}')
    print(f'AUC: {np.mean(aucs)}')

    return model

def data_prep(df):

    df = df.drop_duplicates()

    subjects = []
    for items in WORDLIST.values():
        subjects.append(items['subject'])

    subjects = np.array(flatten_list(subjects))

    message("read dictionaries")
    module = importlib.import_module("packages.dictionaries.pt_br")
    dictionaries = getattr(module, 'DICTIONARY')

    dictionaries = np.unique(np.concatenate([dictionaries, subjects]))

    message("normalize_columns")
    normalize_columns = ["subject", "word_5", "word_4", "word_3", "word_2", "word_1"]
    stacked = df[normalize_columns].stack()
    words = list(set(stacked))
    df = normalize_words(df, normalize_columns, dictionaries, words)

    cols = [
        "location",
        "word_number",
        "document_size",
        "document_index",
    ]
    
    df = convert_type_columns(df, cols, int)
    df = convert_type_columns(df, [f"{col}_encoded" for col in normalize_columns], int)

    # df.to_csv("./score_model.csv", index=False)
    # df = pd.read_csv("./score_model.csv")

    df["target"] = df["target"].astype(int)

    df = create_new_features(df)

    select_cols = lambda df_aux: df_aux[[col for col in df_aux.columns if col not in normalize_columns]]

    df_train = df[df['target'].isin([1, 0])]
    df_predictic = df[df['target'] == -1]
    df_validation = df_predictic[['ref', 'subject', 'subject_encoded', 'location']]

    df_train = select_cols(df_train)
    df_predictic = select_cols(df_predictic)

    return df_train, df_predictic, df_validation

def create_new_features(df):
    # Primeiro, calcula as contagens únicas e as somas de 'location' para cada combinação de agrupamento.
    grouped_df = df.groupby('ref').agg({
        'subject': 'nunique', 
        'document_index': 'nunique',
        'location': 'sum'
    }).reset_index()

    # Renomeia as colunas do resultado do agrupamento por 'ref' para refletir os dados que representam.
    grouped_df.rename(columns={
        'subject': 'subject_count', 
        'document_index': 'subject_for_document_count',
        'location': 'sum_location_ref'
    }, inplace=True)

    # Repete o processo para [ref, subject] e [ref, subject, document_index], calculando a soma de 'location'.
    sum_location_ref_subject = df.groupby(['ref', 'subject']).agg({
        'location': 'sum'
    }).reset_index().rename(columns={'location': 'sum_location_ref_subject'})

    sum_location_ref_subject_doc_index = df.groupby(['ref', 'subject', 'document_index']).agg({
        'location': 'sum'
    }).reset_index().rename(columns={'location': 'sum_location_ref_subject_doc_index'})

    # Mescla os resultados de volta ao DataFrame original 'df'.
    df = df.merge(grouped_df, on='ref')
    df = df.merge(sum_location_ref_subject, on=['ref', 'subject'])
    df = df.merge(sum_location_ref_subject_doc_index, on=['ref', 'subject', 'document_index'])

    return df

def convert_type_columns(df, cols, cols_types):
    for col in cols:
        if cols_types == int:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float).astype(int)
        else:
            df[col] = df[col].astype(cols_types)
    return df

def normalize_words(df, columns, dictionaries, words):
    mask = np.isin(dictionaries, words)
    filtered_data_set = dictionaries[mask]
    filtered_data_set = np.insert(filtered_data_set, 0, "0")

    for col in columns:
        df[f"{col}_encoded"] = df[col].apply(lambda x: np.where(filtered_data_set == x)[0][0] if x in filtered_data_set else x)
        df[f"{col}_encoded"] = df[f"{col}_encoded"].where(~df[col].isnull(), other="0")
        df[f"{col}_encoded"] = df[f"{col}_encoded"].replace(regex=r'.*\D+.*', value='-1', inplace=False)

    df = df.astype(str)
    return df