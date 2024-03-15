import numpy as np

conjugacoes = np.genfromtxt('./packages/conjugacoes.txt', dtype=str)
dicionario = np.genfromtxt('./packages/palavras.txt', dtype=str)

DICT_PT_BR = np.unique(np.concatenate((conjugacoes, dicionario)))