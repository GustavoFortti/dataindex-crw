import os
import pandas as pd
import re

local = '/home/sun/Main/prototipos/NutriFind/nutrifind-data-ingestion'

def get_all_origins():
    diretorio_inicial = local
    nome_arquivo = 'origin_csl.csv'

    dataframes = []

    # Percorre recursivamente o diretório e seus subdiretórios
    for pasta_raiz, _, arquivos in os.walk(diretorio_inicial):
        for nome_arquivo_encontrado in arquivos:
            if nome_arquivo_encontrado == nome_arquivo:
                caminho_completo = os.path.join(pasta_raiz, nome_arquivo_encontrado)
                df = pd.read_csv(caminho_completo)
                dataframes.append(df)

    # Una todos os DataFrames em um único DataFrame
    df = pd.concat(dataframes, ignore_index=True)
    return df

def mask_qnt(text, pattern):
    # Padrão de regex para combinar quantidades e unidades
    

    # Buscar por correspondências
    match = re.search(pattern, text)

    # Extrair quantidade e unidade se houver correspondência
    if match:
        quantidade, unidade = match.groups()
        return quantidade, unidade

    return None, None

def convert_to_gr(row):
    value = row['quantidade']
    unit = row['unidade']
    
    if pd.notna(value):  # Verifica se 'value' não é nulo
        value = str(value).replace(',', '.')
        if unit in ['kg', 'l']:
            value = float(value) * 1000
        try:
            value = int(float(value))
        except ValueError:
            pass
    else:
        value = -1  # Converte NaN em -1
    
    return value

def substituir_por_comprimidos(texto):
    palavras_substituir = ['caps', 'cap', 'cáps', 'v-caps', 'cápsulas', 'capsulas', 'capsules', 'cáp', 'comprimidos', 'comps', 'comp', 'capsulas', 'soft', 'softgel']
    if pd.notna(texto):  # Verifica se o texto não é nulo
        for palavra in palavras_substituir:
            if palavra in texto:
                return 'comprimidos'
    return texto

def relacao_preco_qnt(row):
    resultado = row['preco_numeric'] / row['qnt_gramas']
    if resultado < 0:
        return np.nan  # Substitui valores negativos por NaN
    return resultado
