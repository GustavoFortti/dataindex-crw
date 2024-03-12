import os
import math
import pandas as pd
import re
import os
import unicodedata
import pandas as pd
import numpy as np

local = '/home/mage/main/dataindex-crw/data/supplement/brazil'

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

def get_all_origins(file):
    diretorio_inicial = local
    nome_arquivo = file + '.csv'

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



WORDLIST_SUPLEMENTO = [['whey'],
 ['protein', 'proteina', 'proteica'],
 ['fibras'],
 ['beta alanina', 'betaalanina', 'alanina'],
 ['hair', 'cabelo'],
 ['nail', 'unha'],
 ['antioxidantes'],
 ['concentrado'],
 ['iso', 'isolado', 'isolate'],
 ['hidrolisado'],
 ['albumina'],
 ['barrinha', 'barra', 'bar'],
 ['colageno', 'colagen'],
 ['chocolate'],
 ['wafer', 'bolacha', 'biscoito'],
 ['blend', 'mistura'],
 ['veg', 'vegan', 'vegano', 'vegie', 'vegana'],
 ['rice', 'arroz'],
 ['ervilha', 'pea'],
 ['crisp'],
 ['soy', 'soja'],
 ['nuts'],
 ['alfajor'],
 ['egg', 'ovo'],
 ['caseinato'],
 ['calcio'],
 ['verisol'],
 ['zinco'],
 ['creatina', 'creatine', 'creatin'],
 ['monohidratada'],
 ['glutamin', 'glutamina', 'lglutamina'],
 ['arginin', 'arginine', 'arginina'],
 ['bcaa', 'bca'],
 ['hmb', 'hydroxymethylbutyrate'],
 ['carnitin', 'carnitina', 'lcarnitina'],
 ['aminoacido'],
 ['triptofano'],
 ['taurina'],
 ['maca peruana'],
 ['leucin', 'leucine', 'lleucine'],
 ['mass', 'massa', 'hipercalorico'],
 ['malto', 'dextrina', 'maltodextrina'],
 ['frutose'],
 ['dextrose', 'maltodextrose'],
 ['waxy maize', 'amido de milho'],
 ['batata doce'],
 ['dribose'],
 ['curcuma', 'acafrao'],
 ['coco'],
 ['oleo'],
 ['zinco'],
 ['melatonina'],
 ['psyllium'],
 ['transresveratrol'],
 ['testofen'],
 ['cha'],
 ['astaxantina'],
 ['zeaxantina'],
 ['cafein', 'cafe', 'cafeina', 'coffe', 'caffe', 'coffee'],
 ['cafe verde'],
 ['termogenico'],
 ['pretreino', 'workout', 'pretrein', 'preworkout', 'pre workout'],
 ['biotina'],
 ['hialuronico'],
 ['optimsm'],
 ['palatinose'],
 ['levagen'],
 ['fosfatidilserina'],
 ['acetil', 'nacetil'],
 ['cistein', 'lcisteina'],
 ['linhaca'],
 ['primula'],
 ['borragem'],
 ['krill'],
 ['peixe', 'dha', 'omega 3'],
 ['laranja'],
 ['cromo'],
 ['resveratrol'],
 ['zinco'],
 ['betacaroteno'],
 ['cartamo'],
 ['quitosana'],
 ['propolis'],
 ['lecitina'],
 ['melatonina'],
 ['multivitaminico', 'polivitaminico'],
 ['zma'],
 ['magnesio'],
 ['coco'],
 ['chia'],
 ['cromo'],
 ['picolinato'],
 ['spirulina'],
 ['picolinato'],
 ['alho'],
 ['beauty', 'beleza'],
 ['skin', 'pele'],
 ['imune', 'imunidade'],
 ['uva'],
 ['semente'],
 ['antiox'],
 ['espirulina'],
 ['gengibre'],
 ['tempero'],
 ['xylitol'],
 ['vit', 'vitamina', 'vitamin'],
 ['pasta de amendoim'],
 ['cha verde'],
 ['coenzima q10', 'vitamina q10'],
 ['vitamina a'],
 ['complexo b', 'vitamina b'],
 ['vitamina b1', 'tiamina'],
 ['vitamina b2', 'riboflavina'],
 ['vitamina b3', 'niacina'],
 ['vitamina b5', 'pantotenico'],
 ['vitamina b6', 'piridoxina'],
 ['vitamina b7', 'biotina'],
 ['vitamina b9', 'folico'],
 ['vitamina b12', 'cobalamina'],
 ['vitamina c', 'ascorbico'],
 ['vitamina d', 'calciferol'],
 ['vitamina e', 'tocoferol'],
 ['vitamina k', 'filoquinona'],
 ['vitamina k1', 'fitoquinona'],
 ['vitamina k2', 'menaquinona'],
 ['vitamina k7', 'mk7'],
 ['vitamina j', 'lipoico'],
 ['vitamina l1'],
 ['vitamina l2'],
 ['vitamina m'],
 ['vitamina o'],
 ['vitamina p', 'bioflavonoides'],
 ['vitamina t', 'bioflavonoides'],
 ['vitamina b4', 'adenina'],
 ['vitamina b8', 'inositol'],
 ['vitamina b10', 'paraaminobenzoico'],
 ['vitamina b11', 'salicilico'],
 ['vitamina b13', 'orotico'],
 ['vitamina b15', 'pangamico'],
 ['vitamina b17', 'amigdalina'],
 ['vitamina b22', 'ratanhia'],
 ['vitamina n', 'pantotenico'],
 ['vitamina w'],
 ['vitamina f', 'graxos essenciais'],
 ['vitamina g', 'monofosfato de nicotinamida'],
 ['vitamina h', 'biotina'],
 ['vitamina l', 'adipico'],
 ['vitamina q', 'coenzima q10'],
 ['vitamina r', 'flavina'],
 ['vitamina s', 'aminobenzoico']
]

WORDLIST = {
    "supplement": WORDLIST_SUPLEMENTO,
}

def best_words(text):
    text = clean_text(text)

    words_count = {}
    for item in WORDLIST:
        for sub_item in item:
            count = len(re.findall(" " + clean_text(sub_item) + " ", text))
            if (count != 0):
                words_count[sub_item] = count
                break

    if (words_count == {}):
        return None

    words_count = dict(sorted(words_count.items(), key=lambda item: item[1], reverse=True))
    limit = int(list(words_count.values())[0] * 0.30)
    words = ""
    limit_size = 3
    for item, value in words_count.items():
        if ((value >= limit) & (limit_size > 0)): 
            limit_size -= 1
            words += f" {item}"
        else: break

    return words