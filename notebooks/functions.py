import os
import math
import pandas as pd
import re
import os
import unicodedata
import pandas as pd
import numpy as np

local = '/home/sun/Main/prototipos/NutriFind/nutrifind-data-ingestion'

def remove_nan_from_dict(document):
    new_document = {}
    for chave, valor in document.items():
        if isinstance(valor, float):
            if not math.isnan(valor):
                new_document[chave] = valor
        else:
            new_document[chave] = valor

    return new_document

def create_documents_with_pandas(df, index_name):
    for index, row in df.iterrows():
        yield {
            "_op_type": "create",
            "_index": index_name,
            "_source": remove_nan_from_dict(row.to_dict()),
        }

def remove_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean_text(texto):
    # Normaliza o texto para decompor acentos e caracteres especiais
    texto = unicodedata.normalize('NFKD', texto)
    # Mantém apenas caracteres alfanuméricos e espaços
    texto = u"".join([c for c in texto if not unicodedata.combining(c)])
    # Remove tudo que não for letra, número ou espaço
    return remove_spaces(re.sub(r'[^A-Za-z0-9 ]+', '', texto).lower())

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

def find_pattern_for_quantity(text, pattern):
    matches = re.findall(pattern, text)
    padrao = r'\d+x'
    matches_multiply = re.findall(padrao, text)

    if (len(matches) == 1):
        quantidade, unidade = matches[0]
        quantidade = float(str(quantidade).replace(',', '.'))
        if (len(matches_multiply) == 1):
            quantidade = quantidade * float(matches_multiply[0].replace('x', ''))
        return quantidade, unidade

    return None, None

def convert_to_grams(row):
    value = row['quantidade']
    unit = row['unidade']
    
    if pd.notna(value):
        if unit in ['kg']:
            value = float(value) * 1000
        try:
            value = int(float(value))
        except ValueError:
            pass
    else:
        value = -1
    
    return value

def replace_for_comprimidos(texto):
    palavras_substituir = ['caps', 'cap', 'vcaps', 'capsulas', 'capsules', 'comprimidos', 'comps', 'comp', 'capsulas', 'soft', 'softgel']
    if pd.notna(texto):
        for palavra in palavras_substituir:
            if clean_text(palavra) in clean_text(texto):
                return 'comprimidos'
    return texto

def relation_qnt_preco(row):
    resultado = (row['preco_numeric'] / row['quantidade']) if (row['quantidade'] > 0) else -1
    if resultado < 0:
        return np.nan
    return round(resultado, 3)

