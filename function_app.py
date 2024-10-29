import os
import azure.functions as func
import datetime
import json
import logging
import requests
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

# Obter strg de conexão do Blob
connection_string = os.getenv("BLOB_STORAGE_CONNECTION_STRING")

# Configurar Time Trigger pra execução em um horário determinado
@app.timer_trigger(schedule="0 40-59 18 * * 1-5", arg_name="mTimer", run_on_startup=False, use_monitor=False)
def TimeTriggerFunction(mTimer: func.TimerRequest) -> None:
    if mTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    # 1. Buscar dados da URL
    try:
        url = "https://sistemaswebb3-balcao.b3.com.br/featuresDIProxy/DICall/GetRateDI/eyJsYW5ndWFnZSI6InB0LWJyIn0="
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve data: {e}")
        return

    # 2. Verificar se o dado já foi coletado no dia da consulta
    current_date = datetime.datetime.now().date()
    data_date_str = json_data.get('date')
    
    if data_date_str:
        data_date = datetime.datetime.strptime(json_data.get('date'), '%d/%m/%Y').date()
        if data_date == current_date:
            logging.info("Data já coletada hoje.")
            return

    # 3. Salvar o JSON no Blob Storage
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client("desafio-azure")
        
        # Garantir que o container existe
        if not container_client.exists():
            container_client.create_container()

        blob_client = container_client.get_blob_client(f"data-{current_date}.json")
        blob_client.upload_blob(json.dumps(json_data), overwrite=True)
        logging.info("JSON salvo no Blob Storage.")
    except Exception as e:
        logging.error(f"Failed to upload JSON to Blob Storage: {e}")

# Função HTTP Trigger para salvar taxa XML
@app.route(route="HttpRequestFunction", auth_level=func.AuthLevel.FUNCTION)
def HttpRequestFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        rate = req_body.get("rate").replace(",", ".")  # Converte "10,65" para "10.65"
    except ValueError:
        return func.HttpResponse("Invalid JSON data", status_code=400)
    
    # 1. Cria o XML
    xml_content = f"<xml><rate value=\"{rate}\"></rate></xml>"

    # 2. Salva o XML no Blob Storage
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client("desafio-azure")

        # Garantir que o container existe
        if not container_client.exists():
            container_client.create_container()

        blob_client = container_client.get_blob_client("rate.xml")
        blob_client.upload_blob(xml_content, overwrite=True)
        logging.info("XML stored on Blob Storage.")
    except Exception as e:
        logging.error(f"Failed to upload XML to Blob Storage: {e}")
        return func.HttpResponse("Failed to upload XML", status_code=500)

    return func.HttpResponse("XML created and uploaded successfully", status_code=200)
