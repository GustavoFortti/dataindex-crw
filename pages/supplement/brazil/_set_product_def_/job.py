import importlib
import numpy as np
import pandas as pd
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
    "name": "_set_product_def_",
    "languages": ['pt_br'],
    "wordlist": WORDLIST["supplement"],
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_product_def_",
}

pd.set_option('display.max_rows', None)

def run(args):
    global DATA_PATH_FILE_SYSTEM
    global DATA_PATH
    global WORDLIST
    global LOCAL

    print("JOB_NAME: " + CONF["name"])
    CONF.update(vars(args))
    DATA_PATH_FILE_SYSTEM = (f'{LOCAL}/data/supplement/brazil')
    WORDLIST = CONF['wordlist']
    DATA_PATH = CONF['data_path']

    create_directory_if_not_exists(DATA_PATH)

    message("READ all product_info.csv")
    df = get_all_dfs_in_dir(DATA_PATH_FILE_SYSTEM, "product_info")

    message("exec data_prep")
    df_train, df_ref_train, df_predict, df_ref_predict, df_product_def = data_prep(df)

    message("load train")
    model = run_score_train(df_train)

    message("run predict")
    df_predicted = run_score_predict(df_predict, model)
    df_predicted = pd.merge(df_predicted, df_ref_predict, on=['ref', 'subject_encoded', 'document_index', 'location'])

    df_product_def_predicted = calc_def_product(df_predicted)

    df_product_def_predicted = add_synonyms_to_cols_with_wordlist(df_product_def_predicted, "subject")
    df_product_def_predicted = df_product_def_predicted.rename(columns={'subject': 'product_def_pred'})
    
    df_product_def = add_synonyms_to_cols_with_wordlist(df_product_def, "subject")
    df_product_def = df_product_def.rename(columns={'subject': 'product_def'})

    df_product_def_predicted.to_csv(f"{DATA_PATH}/product_def_predicted.csv", index=False)
    df_product_def.to_csv(f"{DATA_PATH}/product_def.csv", index=False)

def add_synonyms_to_cols_with_wordlist(df, col):
    for idx, row in df.iterrows():
        ref = row['ref']
        synonyms = []
        for key, value in WORDLIST.items():
            words = value['subject']
            aux_subject = [words for subject in row['subject'].split(", ") if subject in words]
            if (aux_subject != []):
                synonyms.extend(aux_subject)
        
        synonyms = ", ".join(flatten_list(synonyms))
        df.loc[idx, col] = synonyms

    return df

def calc_def_product(df):
    df_filtered = df[(df['product_predicted'] != 0) & 
                    (df['probability_class_1'] >= 0.7)]
    
    def filter_document_index(df):
        if ((len(df) == 1) or (df['document_index'].max() == df['document_index'].min())):
            return df
        return df[df['document_index'] != df['document_index'].max()]

    df_filtered = df_filtered.groupby('ref', as_index=False).apply(filter_document_index).reset_index(drop=True)

    df_grouped = df_filtered.groupby(['ref', 'subject_encoded']).agg({
        'location': 'sum',
        'product_predicted': 'sum',
        'probability_class_0': 'sum',
        'probability_class_1': 'sum',
        'subject': unique_subject,
    }).reset_index()[['ref', 'product_predicted', 'probability_class_1', 'subject']]

    def filter_class_1(df):
        if len(df) == 1:
            return df
        return df[df['probability_class_1'] == df['probability_class_1'].max()]
    
    df = df_grouped.groupby('ref', as_index=False).apply(filter_class_1).reset_index(drop=True)

    return df[['ref', 'subject']]

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

    return df[['ref', 'location', 'document_index', 'subject_encoded', 'product_predicted', 'probability_class_0', 'probability_class_1']]

def train_and_evaluate_models(X, y, n_splits=5):
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=200, random_state=42)
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    aucs = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracies.append(accuracy_score(y_test, y_pred))
        precisions.append(precision_score(y_test, y_pred, average='binary'))
        recalls.append(recall_score(y_test, y_pred, average='binary'))
        f1_scores.append(f1_score(y_test, y_pred, average='binary'))
        aucs.append(roc_auc_score(y_test, y_pred))

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
    dictionaries = importlib.import_module("packages.dictionaries.pt_br").get_dictionary(LOCAL)

    brands = np.array(list(set(df['brand'].values)))
    dictionaries = np.unique(np.concatenate([dictionaries, subjects, brands]))

    message("normalize_columns")
    normalize_columns = ["subject", "word_5", "word_4", "word_3", "word_2", "word_1", "brand"]
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

    df["target"] = df["target"].astype(int)

    df = create_new_features(df)

    cols = [
        'subject_encoded_count',
        'location_mean',
        'subject_encoded_count_total',
        'location_mean_total',
    ]
    df = convert_type_columns(df, cols, int)

    select_cols = lambda df_aux: df_aux[[col for col in df_aux.columns if col not in normalize_columns]]

    df_train = df[df['target'].isin([1, 0])]
    df_predict = df[df['target'] == -1]
    df_ref_train = df_predict[['ref', 'subject', 'document_index', 'subject_encoded', 'location']]
    df_ref_predict = df_predict[['ref', 'subject', 'document_index', 'subject_encoded', 'location']]
    
    df_product_def = df[df['target'] == 1][['ref', 'subject']]
    df_product_def = df_product_def.groupby('ref')['subject'].unique().reset_index()
    df_product_def['subject'] = df_product_def['subject'].apply(lambda x: ', '.join(x))

    df_train = select_cols(df_train)
    df_predict = select_cols(df_predict)

    return df_train, df_ref_train, df_predict, df_ref_predict, df_product_def

def create_new_features(df):
    # Grouping by columns 'ref', 'subject', and 'document_index'
    cols = ['ref', 'subject', 'document_index']
    
    # Aggregating 'subject_encoded' by count and 'location' by taking the mean of the smallest 20% or 1 observation
    grouped_df = df.groupby(cols).agg({
        'subject_encoded': 'count',  # Counting occurrences of 'subject_encoded'
        'location': (lambda x: x.nsmallest(max(int(len(x) * 0.20), 1)).mean()),  # Calculating the mean of the smallest 20% or 1 observation of 'location'
    }).reset_index()
    
    # Renaming columns for clarity
    grouped_df = grouped_df[['ref', 'subject', 'document_index', 'subject_encoded', 'location']]
    grouped_df.columns = [
        'ref', 
        'subject', 
        'document_index', 
        'subject_encoded_count',  # Renaming 'subject_encoded' count column
        'location_mean',  # Renaming 'location' mean column
    ]
    
    # Merging the aggregated data back to the original DataFrame based on 'ref', 'subject', and 'document_index'
    df = df.merge(grouped_df, on=cols)

    # Grouping by columns 'ref' and 'document_index'
    cols = ['ref', 'document_index']
    
    # Aggregating 'subject_encoded' by count and 'location' by taking the mean
    grouped_df = df.groupby(cols).agg({
        'subject_encoded': 'count',  # Counting occurrences of 'subject_encoded'
        'location': 'mean',  # Calculating the mean of 'location'
    }).reset_index()
    
    # Renaming columns for clarity
    grouped_df.columns = [
        'ref', 
        'document_index', 
        'subject_encoded_count_total',  # Renaming 'subject_encoded' count column
        'location_mean_total',  # Renaming 'location' mean column
    ]
    
    # Merging the aggregated data back to the original DataFrame based on 'ref' and 'document_index'
    df = df.merge(grouped_df, on=cols)

    # Grouping by columns 'ref' and 'document_index'
    cols = ['ref', 'document_index']
    
    # Aggregating 'subject_encoded_count' by taking the mean
    grouped_df = df.groupby(cols).agg({
        'subject_encoded_count': 'mean',  # Calculating the mean of 'subject_encoded_count'
    }).reset_index()
    
    # Renaming columns for clarity
    grouped_df.columns = [
        'ref', 
        'document_index', 
        'subject_encoded_count_max',  # Renaming 'subject_encoded_count' mean column
    ]
    
    # Merging the aggregated data back to the original DataFrame based on 'ref' and 'document_index'
    df = df.merge(grouped_df, on=cols)

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