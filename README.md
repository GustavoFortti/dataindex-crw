# Projeto de Extração e Processamento de Dados de Suplementos

## Visão Geral

Este projeto tem como objetivo realizar a extração, processamento e armazenamento de dados relacionados a suplementos de diversas marcas no mercado brasileiro. Utilizando técnicas de web scraping, os dados são extraídos de sites e processados para posterior ingestão em um sistema de banco de dados ou sistema de busca como o Elasticsearch.

A arquitetura do projeto está organizada em diferentes módulos, cada um responsável por uma etapa específica do pipeline de dados, como extração, transformação e carregamento (ETL).

## Estrutura de Diretórios

### `config/`
Este diretório contém configurações e scripts de inicialização. Alguns dos arquivos principais são:

- `entrypoint/`: Scripts necessários para inicialização e configuração de dependências, como:
  - `entrypoint.sh`: Script de inicialização do ambiente.
  - `requirements.sh`: Instalação das dependências.
  - `requirements.txt`: Arquivo de dependências Python.
- `setup/`: Scripts para configurar e inicializar serviços específicos, como:
  - `display.py`: Configurações de exibição de dados.
  - `elasticsearch.py`: Configurações do Elasticsearch.
  - `image_server.py`: Configuração de um servidor de imagens.

### `jobs/`
Esta pasta armazena os jobs que executam os processos de coleta de dados para diferentes páginas e marcas de suplementos.

- `data_intelligence/`: Contém jobs específicos para definição de produtos.
- `master_page/` e `slave_page/`: Responsáveis por coordenar o scraping de páginas principais e secundárias. Dentro de `pages/`, há subdiretórios com configurações específicas para diferentes marcas de suplementos.

### `lib/`
Contém bibliotecas de suporte para as operações do projeto.

- `extract/`: Módulos responsáveis pela extração dos dados das páginas.
  - `crawler.py`: Contém o código para crawling de páginas web.
  - `extract.py`: Funções específicas de extração de dados.
  - `selenium_service.py`: Serviço para manipulação do Selenium no processo de scraping.

- `load/`: Responsável pela ingestão dos dados extraídos em bancos de dados ou sistemas de busca.
  - `image_ingestion.py`: Ingestão de dados relacionados a imagens.
  - `ingestion.py`: Funções gerais de ingestão de dados.

- `transform/`: Realiza a transformação e enriquecimento dos dados.
  - `product_definition.py`: Definição dos dados transformados relacionados aos produtos.
  - `transform_functions.py`: Funções auxiliares para a transformação de dados.

### `utils/`
Contém funções utilitárias usadas em várias partes do projeto:

- `dataframe.py`: Funções para manipulação de dataframes.
- `file_system.py`: Funções auxiliares para manipulação de arquivos.
- `log.py`: Configurações e funções para logging.
- `py_functions.py`: Funções utilitárias gerais em Python.
- `wordlist/`: Diretório contendo listas de palavras e dicionários específicos para o mercado brasileiro.

## Principais Tecnologias

- **Python**: Linguagem de programação principal utilizada para a implementação do projeto.
- **Selenium**: Utilizado para a automação e scraping de páginas web.
- **Elasticsearch**: Sistema de busca utilizado para armazenar e consultar os dados processados.
- **Docker**: O projeto pode ser executado em contêineres para garantir a consistência do ambiente.

## Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone <URL-do-repositorio>
   cd <diretorio-do-projeto>


# Para ativar o ambiente virtual (Linux/macOS):
source venv/bin/activate

# Para desativar o ambiente virtual (sair da venv):
deactivate