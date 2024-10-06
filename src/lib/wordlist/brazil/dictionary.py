import numpy as np



def get_dictionary(local):
    conjugacoes = np.genfromtxt(f'{local}/src/lib/wordlist/brazil/conjugacoes.txt', dtype=str)
    dicionario = np.genfromtxt(f'{local}/src/lib/wordlist/brazil/palavras.txt', dtype=str)

    personal_pronouns = ["Eu", "Tu", "Ele", "Ela", "Nós", "Vós", "Eles", "Elas", "Mim", "Ti", "Si", "Consigo"]
    oblique_pronouns = ["Me", "Te", "Se", "Nos", "Vos", "O", "A", "Lhe", "Os", "As", "Nos", "Vos", "Se", "Convosco", "Lhes", "Contigo"]
    demonstrative_pronouns = ["Este", "Esse", "Aquele", "Esta", "Essa", "Aquela", "Isto", "Isso", "Aquilo", "Estes", "Esses", "Aqueles", "Estas", "Essas", "Aquelas", "Iste"]
    possessive_pronouns = ["Meu", "Teu", "Seu", "Nosso", "Vosso", "Seu", "Minha", "Tua", "Sua", "Nossa", "Vossa", "Sua", "Meus", "Teus", "Seus", "Nossos", "Vossos", "Minhas", "Tuas", "Suas", "Nossas", "Vossas"]
    indefinite_pronouns = ["Alguém", "Ninguém", "Todo", "Algum", "Nenhum", "Outro", "Muito", "Pouco", "Tanto", "Cada", "Algo", "Tudo", "Nada", "Cada um", "Qualquer", "Poucos", "Muitos", "Vários", "Outrem"]
    relative_pronouns = ["Que", "Qual", "Quem", "Onde", "Cujo", "O qual", "Cuja", "Quanto"]
    interrogative_pronouns = ["Quem", "O que", "Qual", "Quanto", "Onde", "Quando", "Como", "Por que", "Qualquer coisa", "Quanto a"]
    prepositions = ["A", "Ante", "Até", "Após", "Com", "Contra", "De", "Desde", "Em", "Entre", "Para", "Por", "Perante", "Sem", "Sob", "Sobre", "Trás", "Conforme", "Contudo", "Durante", "Exceto", "Mediant", "Menos", "Salvo", "Segundo", "Visto"]

    brazil_pronouns = personal_pronouns + oblique_pronouns + demonstrative_pronouns + possessive_pronouns + indefinite_pronouns + relative_pronouns + interrogative_pronouns + prepositions
    brazil_conectores = ['a', 'o', 'e', 'ou', 'nem', 'mas', 'porque', 'como', 'apesar', 'além', 'entretanto', 'porém', 'todavia', 'logo', 'portanto', 'assim', 'contudo', 'embora', 'ainda', 'também', 'quer', 'seja', 'isto', 'aquilo']

    brazil_pronouns_numpy = np.array(brazil_pronouns)
    brazil_conectores_numpy = np.array(brazil_conectores)

    return np.unique(np.concatenate((conjugacoes, dicionario, brazil_pronouns_numpy, brazil_conectores_numpy)))