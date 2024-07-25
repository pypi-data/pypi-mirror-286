import asyncio
import math
import os
import subprocess
import warnings

import aiohttp
import psutil
import pyautogui
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from rich.console import Console

from worker_automate_hub.config.settings import (
    load_env_config,
    load_worker_config,
)
from worker_automate_hub.utils.logger import logger

console = Console()


async def get_system_info():
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "situacao": "{'status': 'em desenvolvimento'}",
    }


async def get_new_task_info():
    env_config, _ = load_env_config()
    worker_config = load_worker_config()
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": env_config["VERSION"],
    }


async def kill_process(process_name: str):
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            logger.error(f"Erro ao listar processos: {stderr.decode().strip()}", None)
            console.print(
                f"Erro ao listar processos: {stderr.decode().strip()}", style="bold red"
            )
            return

        if stdout:
            lines = stdout.decode().strip().split("\n")
            for line in lines:
                # Verifique se o processo atual corresponde ao nome do processo
                if process_name in line:
                    try:
                        # O PID(Process ID) é a segunda coluna na saída do tasklist
                        pid = int(line.split(",")[1].strip('"'))
                        await asyncio.create_subprocess_exec(
                            "taskkill", "/PID", str(pid), "/F"
                        )
                        # logger.info(
                        #     f"Processo {process_name} (PID {pid}) finalizado.", None
                        # )
                        console.print(
                            f"\nProcesso {process_name} (PID {pid}) finalizado.\n",
                            style="bold green",
                        )
                    except Exception as ex:
                        # logger.error(
                        #     f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}",
                        #     None,
                        # )
                        console.print(
                            f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}",
                            style="bold red",
                        )
        else:
            logger.info(
                f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}.",
                None,
            )
            console.print(
                f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}.",
                style="bold yellow",
            )

    except Exception as e:
        logger.error(f"Erro ao tentar matar o processo: {e}", None)
        console.print(f"Erro ao tentar matar o processo: {e}", style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                # logger.info(str(ex), None)
                # console.print(
                #     f"Erro em locateCenterOnScreen: {str(ex)}", style="bold red"
                # )
                console.print(f"Elemento não encontrado na pos: {region_to_look}")

            if element_center:
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await asyncio.sleep(1)

        return None
    except Exception as ex:
        # logger.info(str(ex), None)
        # console.print(f"Erro em find_element_center: {str(ex)}", style="bold red")
        console.print(
            f"{counter} - Buscando elemento na tela: {region_to_look}",
            style="bold yellow",
        )
        return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)

    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await asyncio.sleep(1)
                if element.wait("exists", timeout=2):
                    await asyncio.sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await asyncio.sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False


async def login_emsys(config, app, task):

    from pywinauto.application import Application

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    await asyncio.sleep(10)
    # Testa se existe alguma mensagem no Emsys
    window_message_login_emsys = await find_element_center(
        "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 15
    )

    # Clica no "Não mostrar novamente" se existir
    if window_message_login_emsys:
        pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
        pyautogui.click(
            window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
        )
        console.print("Mensagem de login encontrada e fechada.", style="bold green")

    # Ve se o Emsys esta aberto no login
    image_emsys_login = await find_element_center(
        "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 600
    )

    if image_emsys_login:
        if await wait_element_ready_win(app["Login"]["Edit2"], 80):
            disconect_database = await find_element_center(
                "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 300
            )

            if disconect_database:
                # Realiza login no Emsys
                type_text_into_field(config["user"], app["Login"]["Edit2"], True, "50")
                pyautogui.press("tab")
                type_text_into_field(
                    config["pass"],
                    app["Login"]["Edit1"],
                    True,
                    "50",
                )
                pyautogui.press("enter")

                # Seleciona a filial do emsys
                selecao_filial = await find_element_center(
                    "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 350
                )

                if selecao_filial:
                    type_text_into_field(
                        task["configEntrada"]["filialEmpresaOrigem"],
                        app["Seleção de Empresas"]["Edit"],
                        True,
                        "50",
                    )
                    pyautogui.press("enter")

                    button_logout = await find_element_center(
                        "assets/emsys/button_logout.png", (0, 0, 130, 150), 750
                    )

                    if button_logout:
                        console.print(
                            "Login realizado com sucesso.", style="bold green"
                        )
                        return {
                            "sucesso": True,
                            "retorno": "Logou com sucesso no emsys!",
                        }
        else:
            logger.info("Elemento de login não está pronto.")
            console.print("Elemento de login não está pronto.", style="bold red")
            return {"sucesso": False, "retorno": "Falha ao logar no EMSys!"}


async def api_simplifica(
    urlSimplifica: str,
    status: str,
    observacao: str,
    uuidsimplifica: str,
    numero_nota: str,
    valor_nota: str,
):

    data = {
        "uuid_simplifica": uuidsimplifica,
        "status": status,
        "numero_nota": numero_nota,
        "observacao": observacao,
        "valor_nota": valor_nota,
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(f"{urlSimplifica}", data=data) as response:
                console.print(
                    f"\nSucesso ao enviar {response.content}\n para o simplifica",
                    style="bold green",
                )
                logger.info(
                    f"\nSucesso ao enviar {response.content}\n para o simplifica"
                )

    except Exception as e:
        console.print(
            f"Erro ao comunicar com endpoint do Simplifica: {e}", style="bold green"
        )
        logger.info(f"Erro ao comunicar com endpoint do Simplifica: {e}")


def add_start_on_boot_to_registry():
    import winreg as reg

    try:
        # Caminho para a chave Run
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Nome da chave
        key_name = "worker-automate-hub"

        # Caminho para o executável no diretório atual        
        directory_value = os.path.join(os.getcwd(), "worker.bat")

        # Acessar a chave de registro
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE
        )

        # Adicionar ou modificar o valor
        reg.SetValueEx(registry_key, key_name, 0, reg.REG_SZ, directory_value)

        # Fechar a chave de registro
        reg.CloseKey(registry_key)

        console.print(
            f"\nChave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!\n",
            style="bold green",
        )
        logger.info(f"Chave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!")

    except Exception as e:
        console.print(f"\nErro ao adicionar ao registro: {e}\n", style="bold red")
        logger.error(f"Erro ao adicionar ao registro: {e}")

def create_worker_bat():
    try:
        # Caminho do diretório atual
        current_dir = os.getcwd()
        nome_arquivo = 'worker.bat'

        # Conteúdo do arquivo
        bat_content = """@echo off
cd %USERPROFILE%
start /min "" "worker" "run"
"""

        # Caminho completo para o arquivo
        bat_file_path = os.path.join(current_dir, nome_arquivo)

        # Escrevendo o conteúdo no arquivo
        with open(bat_file_path, 'w') as file:
            file.write(bat_content.strip())

        console.print(f"\nArquivo {nome_arquivo} criado com sucesso em {bat_file_path}!\n", style="bold green")
        logger.info(f"Arquivo {nome_arquivo} criado com sucesso em {bat_file_path}!")

    except Exception as e:
        console.print(f"\nErro ao criar o arquivo {nome_arquivo}: {e}\n", style="bold red")
        logger.error(f"Erro ao criar o arquivo {nome_arquivo}: {e}")
