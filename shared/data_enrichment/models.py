import numpy as np
import pandas as pd
import joblib

from utils.log import message

from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from imblearn.pipeline import Pipeline as imbpipeline
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

from utils.general_functions import (
    save_json,
    delete_file,
    read_json,
    flatten_list
)

def run_models(df, model_path):
    refs = df["ref"].values

    models = read_json(f"{model_path}/_models_.json")

    for target_col, models in models.items():
        df_statistics = pd.read_csv(f"{model_path}/{target_col}.csv")
        best_recall_models, best_precision_models = select_best_models(df_statistics, models)
        
        recall_model, recall_value = best_recall_models[0]
        message(f"{recall_model} - {recall_value}")
        df_pred_reacll = run_predict(df, refs, model_path, recall_model, recall_value, target_col)

        recall_model, recall_value = best_recall_models[1]
        message(f"{recall_model} - {recall_value}")
        df_pred_reacll_aux = run_predict(df, refs, model_path, recall_model, recall_value, target_col)
        df_pred_reacll = df_pred_reacll.merge(df_pred_reacll_aux, on='ref', how='inner')

        precision_model, precision_value = best_precision_models[0]
        message(f"{precision_model} - {precision_value}")
        df_pred_precision = run_predict(df, refs, model_path, precision_model, precision_value, target_col)

        precision_model, precision_value = best_precision_models[1]
        message(f"{precision_model} - {precision_value}")
        df_pred_precision_aux = run_predict(df, refs, model_path, precision_model, precision_value, target_col)
        df_pred_precision = df_pred_precision.merge(df_pred_precision_aux, on='ref', how='inner')

        print(df_pred_reacll)
        print(df_pred_precision)
  
    return df

def run_predict(df, refs, model_path, model_name, model_value, target_col):
    model = load_model(f"{model_path}/{model_name}-{target_col}.pkl")
    X, _ = prep_dataframe(df.copy(), pd.DataFrame())

    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)
    df_pred = pd.DataFrame(y_proba,  columns=[f'y_proba_0_{model_name}_{target_col}', f'y_proba_1_{model_name}_{target_col}'])
    df_pred = df_pred.mul(model_value)
    df_pred[f'y_pred_{model_name}_{target_col}'] = str(y_pred)[1:-1].replace(".", "").split(" ")
    df_pred['ref'] = refs

    return df_pred

def select_best_models(df, models):
    df = df[df['Model'].isin(models)]

    best_precision_models = df.nlargest(2, 'Precision')[['Model', 'Precision']]
    best_recall_model = df.nlargest(2, 'Recall')[['Model', 'Recall']]

    return best_recall_model.values, best_precision_models.values

def generate_models(df_x, df_y, models_path):
    message("running training models...")

    X = df_x
    models_savad = {}
    for target_col in df_y.columns:

        results = []
        size = sum(df_y[target_col])
        if (size < 8):
            continue
        if ("whey" not in target_col):
            continue

        y = df_y[target_col]
        models_savad[target_col] = []
        message(f"TARGET: {target_col}")
        for model_name, model in get_models(X, y).items():
            try:
                message(f"MODEL: {model_name}")
                pipeline, result = train_model(model, X, y)
                result['Model'] = model_name
                result['Target'] = target_col
                results.append(result)

                file_name = f"{model_name}-{target_col}.pkl"
                model_path = f"{models_path}/{file_name}"
                models_savad[target_col].append(model_name)
                save_model(pipeline, model_path)
            except Exception as e:
                print(f"Erro ao avaliar o modelo {model_name} para a coluna {target_col}: {e}")

        results_df = pd.DataFrame(results)
        results_df.to_csv(models_path + f"/{target_col}.csv", index=False)
        message("Statistics...")
        print(results_df)
    
    models_list_path = f"{models_path}/_models_.json"
    delete_file(models_list_path)
    save_json(models_list_path, models_savad)

def train_model(model, X, y, n_splits=5):
    # Configurando o KFold
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Listas para armazenar os resultados de cada fold
    auc_rocs, accuracies, precisions, recalls, f1s = [], [], [], [], []

    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Configurando o SMOTE
        smote = SMOTE(random_state=42, k_neighbors=1)
        
        # Criando o pipeline com SMOTE e o modelo fornecido
        pipeline = imbpipeline([('smote', smote), ('model', model)])
        
        # Treinando o modelo
        pipeline.fit(X_train, y_train)
        
        # Fazendo previsões
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]  # Para AUC-ROC

        # Calculando métricas e adicionando aos resultados
        auc_rocs.append(roc_auc_score(y_test, y_proba))
        accuracies.append(accuracy_score(y_test, y_pred))
        precisions.append(precision_score(y_test, y_pred, zero_division=1))
        recalls.append(recall_score(y_test, y_pred, zero_division=1))
        f1s.append(f1_score(y_test, y_pred, zero_division=1))


    # Calculando a média das métricas
    results = {
        'AUC-ROC': np.mean(auc_rocs),
        'Accuracy': np.mean(accuracies),
        'Precision': np.mean(precisions),
        'Recall': np.mean(recalls),
        'F1-Score': np.mean(f1s)
    }

    return pipeline, results

def get_models(x, y):
    return {
        'ExtraTrees': ExtraTreesClassifier(n_estimators=200, random_state=42, class_weight='balanced'),
        'XGBClassifier': XGBClassifier(scale_pos_weight=(len(y) - sum(y)) / sum(y), use_label_encoder=False, eval_metric='logloss'),
        'RandomForest': RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced'),
        'DecisionTree': DecisionTreeClassifier(random_state=42, class_weight='balanced')
    }

def prep_dataframe(df_x, df_y):
    new_df_x = df_x[[i for i in df_x.columns if i not in ["title", "ref", "brand"]]]
    new_df_y = df_y[[i for i in df_y.columns if i not in ["title", "ref", "brand"]]]

    return new_df_x, new_df_y

def save_model(model, filename):
    # Salvando o modelo usando joblib
    joblib.dump(model, filename)
    message(f"Model saved successfully as {filename}")

def load_model(filename):
    # Carregando o modelo treinado
    loaded_model = joblib.load(filename)
    return loaded_model