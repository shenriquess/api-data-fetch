import requests
import pandas as pd
import json
import argparse
import logging
from tqdm import tqdm

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_response(cod_conhecimento, num_conhecimento):
    """
    Função para obter a resposta da API com base nos parâmetros fornecidos.
    
    :param cod_conhecimento: Código de conhecimento (CE)
    :param num_conhecimento: Número de conhecimento (BL)
    :return: Resposta JSON da API ou None em caso de erro
    """
    url = f"https://api-shiva.rhmg.agricultura.gov.br/api/publico/madeira/datem/status?codConhecimento={cod_conhecimento}&numConhecimento={num_conhecimento}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lança um erro para status de resposta 4xx/5xx
        response.encoding = response.apparent_encoding
        json_data = response.json()
        
        # Corrigir caracteres especiais
        json_str = json.dumps(json_data)
        json_str_corrected = bytes(json_str, 'latin1').decode('ISO-8859-1')
        return json.loads(json_str_corrected)
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar a API para CE {cod_conhecimento} e BL {num_conhecimento}: {e}")
        return None

def flatten_json(json_obj, prefix=''):
    """
    Função para transformar um objeto JSON aninhado em um dicionário plano.
    
    :param json_obj: Objeto JSON a ser achatado
    :param prefix: Prefixo para as chaves (usado para recursão)
    :return: Dicionário plano
    """
    flat_dict = {}
    for key, value in json_obj.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_json(value, f'{prefix}{key}.'))
        else:
            flat_dict[f'{prefix}{key}'] = value
    return flat_dict

def main(input_csv, output_csv):
    """
    Função principal para processar o arquivo CSV de entrada, consultar a API e gerar um novo CSV com os resultados.
    
    :param input_csv: Caminho para o arquivo CSV de entrada
    :param output_csv: Caminho para o arquivo CSV de saída
    """
    # Ler o arquivo CSV de entrada
    df = pd.read_csv(input_csv)
    
    # Lista para armazenar os resultados
    results = []

    # Iterar sobre cada linha do DataFrame com uma barra de progresso
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processando"):
        cod_conhecimento = row['CE']
        num_conhecimento = row['BL']
        
        # Obter resposta da API
        json_response = get_api_response(cod_conhecimento, num_conhecimento)
        
        if json_response and 'data' in json_response:
            flat_data = flatten_json(json_response['data'])
            results.append(flat_data)
        else:
            # Em caso de erro ou falta de dados, adicionar uma entrada de erro
            results.append({
                'codConhecimento': cod_conhecimento, 
                'numConhecimento': num_conhecimento, 
                'error': 'No data found or API error'
            })

    # Converter lista de resultados em DataFrame
    results_df = pd.DataFrame(results)

    # Salvar resultados em um novo arquivo CSV
    results_df.to_csv(output_csv, index=False, encoding='ISO-8859-1')
    logging.info(f"Resultados salvos em {output_csv}")

if __name__ == "__main__":
    # Configuração do argparse para CLI
    parser = argparse.ArgumentParser(description="Consulta API e gera um CSV com os resultados.")
    parser.add_argument('--input', required=True, help="Caminho para o arquivo CSV de entrada.")
    parser.add_argument('--output', required=True, help="Caminho para o arquivo CSV de saída.")
    args = parser.parse_args()
    
    main(args.input, args.output)
