import io
import json
import os
import zipfile

import requests
import toml
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pathlib3x import Path
from rich.console import Console

from worker_automate_hub.config.settings import (
    get_package_version,
    load_env_config,
)
from worker_automate_hub.utils.logger import logger

console = Console()


def write_env_config(env_dict: dict, google_credentials: dict):
    try:
        current_dir = Path.cwd()
        assets_path = current_dir / "assets"
        logs_path = current_dir / "logs"
        assets_path.mkdir(exist_ok=True)
        logs_path.mkdir(exist_ok=True)

        config_file_path = current_dir / "settings.toml"
        config_data = {
            "name": "WORKER",
            "params": {
                "api_base_url": env_dict["API_BASE_URL"],
                "api_auth": env_dict["API_AUTHORIZATION"],
                "notify_alive_interval": env_dict["NOTIFY_ALIVE_INTERVAL"],
                "version": get_package_version("worker-automate-hub"),
                "log_level": env_dict["LOG_LEVEL"],
                "drive_url": env_dict["DRIVE_URL"],
            },
            "google_credentials": google_credentials["content"],
        }

        with open(config_file_path, "w") as config_file:
            toml.dump(config_data, config_file)

        log_msg = f"Arquivo de configuração do ambiente criado em {config_file_path}"
        logger.info(log_msg)
        console.print(f"\n{log_msg}\n", style="green")

        return {
            "Message": log_msg,
            "Status": True,
        }
    except Exception as e:
        err_msg = f"Erro ao criar o arquivo de configuração do ambiente. Comando retornou: {e}"
        logger.error(err_msg)
        return {
            "Message": err_msg,
            "Status": False,
        }


def add_worker_config(worker):
    try:
        current_dir = Path.cwd()
        config_file_path = current_dir / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(
                f"O arquivo de configuração não foi encontrado em: {config_file_path}"
            )

        with open(config_file_path, "r") as config_file:
            config_data = toml.load(config_file)

        config_data["id"] = {
            "worker_uuid": worker["uuidRobo"],
            "worker_name": worker["nomRobo"],
        }

        with open(config_file_path, "w") as config_file:
            toml.dump(config_data, config_file)

        log_msg = f"Informações do worker adicionadas ao arquivo de configuração em {config_file_path}"
        console.print(f"\n{log_msg}\n", style="green")
        return {
            "Message": log_msg,
            "Status": True,
        }
    except Exception as e:
        err_msg = f"Erro ao adicionar informações do worker ao arquivo de configuração.\n Comando retornou: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        return {
            "Message": err_msg,
            "Status": False,
        }


def list_files_in_folder(folder_id, service):
    query = f"'{folder_id}' in parents"
    results = (
        service.files()
        .list(q=query, pageSize=1000, fields="files(id, name, mimeType)")
        .execute()
    )
    items = results.get("files", [])
    print("items: ", items)
    return items


def download_file(file_id, file_name, output_folder, service):
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(output_folder, file_name)

    with io.FileIO(file_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloading {file_name}, {int(status.progress() * 100)}% complete.")


def download_assets_and_extract_from_drive():
    try:
        console.print("\nIniciando download dos assets...\n", style="bold green")
        env_config, creds_loaded = load_env_config()
        creds_loaded = json.loads(creds_loaded)["web"]
        folder_url = env_config["DRIVE_URL"]

        # Diretório de execução atual
        current_dir = Path.cwd()
        output_folder = current_dir / "assets"

        if not output_folder.exists():
            output_folder.mkdir(parents=True, exist_ok=True)

        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
        credentials = service_account.Credentials.from_service_account_file(
            f"{current_dir}/credentials.json", scopes=SCOPES
        )
        service = build("drive", "v3", credentials=credentials)

        # Extrair o ID da pasta do URL
        folder_id = folder_url.split("/")[-1].replace("?usp=drive_link", "")
        files = list_files_in_folder(folder_id, service)

        for file in files:
            file_id = file["id"]
            file_name = file["name"]

            # Download do arquivo
            download_file(file_id, file_name, output_folder, service)

            file_path = output_folder / file_name
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(output_folder)
                os.remove(file_path)  # Remove the zip file after extraction

        console.print("\nAssets baixados com sucesso!\n", style="bold green")
    except Exception as e:
        err_msg = f"Erro ao baixar os assets: {e}"
        logger.error(err_msg)
        console.print(f"\n{err_msg}\n", style="bold red")


def list_files_in_folder(folder_id, service):
    results = (
        service.files()
        .list(q=f"'{folder_id}' in parents", fields="files(id, name)")
        .execute()
    )
    return results.get("files", [])


def download_file(file_id, file_name, output_folder, service):
    request = service.files().get_media(fileId=file_id)
    file_path = output_folder / file_name
    with open(file_path, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                console.print(f"Download {int(status.progress() * 100)}%.")
