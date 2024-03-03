# data_enrichment

## check_component e create_spec_columns_with_keywords

#### Explicação do Algoritmo: Uso do `not_contain`

A parte not_contain do algoritmo verifica se certos termos que não devem aparecer estão presentes nas especificações de um produto. Se qualquer um desses termos proibidos for encontrado, o produto é desconsiderado para aquela categoria específica. É como filtrar produtos que têm características que não queremos.

#### Exemplo Prático: Whey Protein
Vamos usar o exemplo do whey para explicar o not_contain de forma simples:

Imagine que estamos buscando produtos que sejam whey protein, mas não queremos produtos que sejam barrinhas, alfajores ou wafers mesmo que tenham whey. Então, se um produto tem as palavras "whey", "protein" e "concentrado" (cumprindo o "minimum_of_components" de 3), ele seria considerado. Porém, se o produto também menciona "barrinha", "alfajor" ou "wafer", ele é desconsiderado, porque essas palavras estão na lista not_contain, indicando que whey não pode ser uma barrinha, por que whey não contem isso, mas o inverso pode ser verdade.

```
    not_contain_flag = not_contain_spec(specs[0]) or \
                        not_contain_spec(specs[1]) or \
                        not_contain_spec(specs[2])
```

Nesse caso o filtro é feito somente nas 3 preimiras colunas de spec (spec_5, spec_4, spec_3), que tem uma pontuação maior e o risco do erro é menor.