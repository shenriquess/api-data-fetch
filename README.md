# Consulta API de Vigilância Agropecuária

Este projeto consiste em um script VBA para Excel e um script Python que consultam a API de Vigilância Agropecuária Nacional, fornecendo informações detalhadas sobre documentos específicos. 

## Funcionalidades

- Consulta uma API pública de vigilância agropecuária para obter informações detalhadas.
- Preenche uma planilha Excel com os resultados da consulta.
- Script Python adicional para processar um arquivo CSV de entrada e gerar um arquivo CSV de saída com os resultados da consulta.

## Requisitos

### VBA para Excel

- Microsoft Excel com suporte a VBA.
- Biblioteca `WebClient` instalada e configurada.

### Python

- Python 3.x
- Bibliotecas Python: `requests`, `pandas`, `argparse`, `logging`, `tqdm`

## Utilização

### Script VBA

O script VBA preenche automaticamente uma planilha Excel com informações obtidas a partir da API de vigilância agropecuária.

### Script Python

O script Python processa um arquivo CSV de entrada e gera um arquivo CSV de saída com os resultados da consulta à API.

#### Como executar o script Python:

1. **Preparar o ambiente:**

   ```sh
   pip install requests pandas tqdm

2. **Executar o script:**

   ```sh
   python script.py --input caminho_para_o_csv_de_entrada --output caminho_para_o_csv_de_saida

#### Exemplo de Uso do Script Python:
   
   ```sh
   python script.py --input input.csv --output output.csv

   ```

   - Este comando lê os dados do arquivo `input.csv`, consulta a API para cada entrada, e salva os resultados em `output.csv`.

## Estrutura do Projeto
- VBA-Web - Teste de Automatização: Planilha com VBA.
- script.py: Script Python para processamento dos dados.
- input.csv: Arquivo CSV de entrada com os dados a serem consultados.
- output.csv: Arquivo CSV de saída com os resultados da consulta.

## Considerações Finais
Este projeto foi desenvolvido para automatizar a consulta a uma API pública, facilitando a obtenção de informações detalhadas sobre documentos específicos e integrando esses dados em uma planilha Excel ou um arquivo CSV.