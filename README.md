# comandos ELASTICSEARCH PROD

### indices
brazil_supplement_
brazil_supplement_whey_
brazil_supplement_bar_
brazil_supplement_preworkout_
brazil_supplement_promocoes_
brazil_supplement_whey_protein_
brazil_supplement_creatina_
brazil_supplement_proteinas_
brazil_supplement_barrinhas_de_proteina_
brazil_supplement_pre_treino_
brazil_supplement_cafeina_
brazil_supplement_energia_
brazil_supplement_resistencia_
brazil_supplement_imunidade_
brazil_supplement_hipercalorico_
brazil_supplement_carboidratos_
brazil_supplement_beta_alanina_
brazil_supplement_termogenico_
brazil_supplement_oleos_
brazil_supplement_temperos_
brazil_supplement_adocantes_
brazil_supplement_pasta_de_amendoim_
brazil_supplement_vegano_
brazil_supplement_vegetariano_
brazil_supplement_vitaminas_
brazil_supplement_minerais_
brazil_supplement_sono_
brazil_supplement_magnesio_
brazil_supplement_pele_
brazil_supplement_cabelo_
brazil_supplement_omega_
brazil_supplement_colageno_
brazil_supplement_combos_


### queries | GET

curl -X GET "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_whey_protein_09042024/_search?size=5" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn" -d'
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query": "whey",
          "fields": [
            "title^10",
            "brand^3",
            "product_def^10",
            "product_def_pred^1"
          ],
          "type": "best_fields"
        }
      },
      "boost_mode": "multiply",
      "functions": [
        {
          "filter": { "match": { "title": "whey" } },
          "weight": 2
        }
      ]
    }
  }
}' | jq





curl -X DELETE "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_history_price_03082024" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn"
curl -X GET "https://dataindex-elk-node-1.ngrok.app/brazil_supplement" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn"

curl -X HEAD "https://dataindex-elk-node-1.ngrok.app/brazil_supplement" -I -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn"

curl -X GET "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_history_price_09042024/_search?size=10" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn" -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "ref": "5c3be2f2" }}
      ]
    }
  }
}'

curl -X GET "https://dataindex-elk-node-1.ngrok.app/_cluster/health" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn"


curl -X GET "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_history_price_09042024/_count" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn" | grep -o '"count":[0-9]*' | cut -d: -f2


curl -X POST "https://dataindex-elk-node-1.ngrok.app/_reindex" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn" -d'
{
  "source": {
    "index": "brazil_supplement_preworkout"
  },
  "dest": {
    "index": "brazil_supplement_preworkout_temp"
  }
}'

curl -X GET "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_bar_09042024/_search?size=18" -H "Content-Type: application/json" -u "elastic:RJ6XXwfjHzYICKfGRTSn" -d'
{
  "query": {
    "match_all": {}
  }
}'

curl -X POST "https://dataindex-elk-node-1.ngrok.app/brazil_supplement_09042024/_count" -H "Content-Type: application/json" -d '{
  "query": {
    "match_all": {}
  }
}' -u "elastic:RJ6XXwfjHzYICKfGRTSn"
