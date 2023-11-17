# ELASTICSEARCH

#### Baixar a imagem do Elasticsearch versão 8.10.4
``` docker pull docker.elastic.co/elasticsearch/elasticsearch:8.10.4 ```

#### Executar um contêiner do Elasticsearch com um nó único
``` docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.10.4 ```

#### Configurar senhas automáticas para usuários do Elasticsearch
``` docker exec -it elasticsearch bin/elasticsearch-setup-passwords auto -b ```

##### Senhas geradas para os usuários do Elasticsearch:
```
    apm_system = PjLFWb4035OfkAsbDiFa
    kibana_system = rvQSVJgNXFhGCNHlHqKx
    kibana = rvQSVJgNXFhGCNHlHqKx
    logstash_system = wfRwGEiwScAJXgeSY5BW
    beats_system = DkOFnepJ1anwBI8peybP
    remote_monitoring_user = yj3bpmokAlSe0vyVWy4R
    elastic = norpfQkVx3PQKrjZpGno
```

curl -X GET "https://localhost:9200/_nodes/stats/jvm?pretty" -u elastic:norpfQkVx3PQKrjZpGno
curl -X GET "https://localhost:9200/_nodes/stats/jvm,indices?pretty" -u elastic:norpfQkVx3PQKrjZpGno
curl -X GET "https://localhost:9200/_cat/thread_pool?v&pretty" -u elastic:norpfQkVx3PQKrjZpGno
curl -X GET "https://localhost:9200/_cluster/health?pretty" -u elastic:norpfQkVx3PQKrjZpGno



#### Fazer uma solicitação para o Elasticsearch usando as senhas
curl -k -u elastic:norpfQkVx3PQKrjZpGno https://localhost:9200

#### Informações sobre a instância do Elasticsearch
{
  "name" : "b3194cefd15d",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "upmlQoHRTBi16_LbDJUJ9g",
  "version" : {
    "number" : "8.10.4",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "b4a62ac808e886ff032700c391f45f1408b2538c",
    "build_date" : "2023-10-11T22:04:35.506990650Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}


# KIBANA

#### Baixar a imagem do Kibana versão 8.10.4
docker pull docker.elastic.co/kibana/kibana:8.10.4

#### Executar um contêiner do Kibana conectado ao Elasticsearch
docker run --name kibana --link elasticsearch:elasticsearch -p 5601:5601 -e "ELASTICSEARCH_HOSTS=https://elasticsearch:9200" docker.elastic.co/kibana/kibana:8.10.4

#### Acessar o shell do contêiner do Elasticsearch
docker exec -it elasticsearch /bin/bash

#### Gerar um token de inscrição para o Kibana
elasticsearch@b3194cefd15d:~$ bin/elasticsearch-create-enrollment-token -s kibana

#### O token de inscrição gerado
eyJ2ZXIiOiI4LjEwLjQiLCJhZHIiOlsiMTcyLjE3LjAuMjo5MjAwIl0sImZnciI6IjY0YTgwZWIzZWEyNzZhNTRmNGU5NTc3Zjk2YmRlYz1mMzM1NWFmNGQxYjljYmYwNWNmMjgyZjgzNjAyY2FkYjEiLCJrZXkiOiJCZEl0bVlzQnNEX3ItYlhuclB2RzpHOVVUTUo3RlRhYVF1enBGaU9RdXBBIn0=

#### Acessar o shell do contêiner do Kibana
docker exec -it kibana /bin/bash

#### Editar o arquivo de configuração do Kibana para adicionar credenciais
kibana@b83629c23c52:~$ cd /usr/share/kibana/config
kibana@b83629c23c52:~/config$ printf "\nelasticsearch.username: \"kibana_system\"\n" >> kibana.yml
kibana@b83629c23c52:~/config$ printf "elasticsearch.password: \"rvQSVJgNXFhGCNHlHqKx\"\n" >> kibana.yml

#### Exibir o arquivo de configuração atualizado do Kibana
kibana@b83629c23c52:~/config$ cat kibana.yml 

################################   NGROK   ##################################

#### Baixar a imagem do ngrok
docker pull ngrok/ngrok 

#### Executar o ngrok para criar um túnel para o Elasticsearch
docker run -d --name ngrok_elasticsearch \
  --net="host" \
  wernight/ngrok \
  ngrok http -authtoken=1rFgnZ3LpLqH4uYhJanGFzpJV4m_7oSNtMgUqLVeRCuXHyzS4 https://localhost:9200

#### Exibir os logs do ngrok
docker logs ngrok_elasticsearch -f

#### Acessar o painel de status do ngrok
http://localhost:4040/status

#### Fazer uma solicitação usando o domínio ngrok (substitua com o seu próprio domínio)
curl -X GET https://eb27-179-193-37-16.ngrok-free.app