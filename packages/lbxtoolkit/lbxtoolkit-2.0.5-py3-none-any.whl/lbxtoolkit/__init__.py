import os
import sys
import locale
import time
import threading
import logging
import msal
import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import validators
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import re 
from unicodedata import normalize 
import pygetwindow as gw
import ctypes    
import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class auth_EntraID: # Classe de autenticação de usuários no Microsoft Entra ID (antiga Azure AD)
    def __init__(self, client_id, client_secret, tenant_id, grupo, timeout=60, log_file='auth_EntraID.log'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.grupo = grupo
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.redirect_uri = "http://localhost:8000"
        self.response = ""
        self.status_code = 0
        self.server = None
        self.log_file = log_file

        # Configura o logger
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def valida_grupo(self): # Valida se o usuário autenticado pertence a grupo de segurança informado
        # Redireciona stdout e stderr para arquivos de log
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open('stdout.log', 'a')
        sys.stderr = open('stderr.log', 'a')

        # Configurações do Selenium
        chrome_options = Options()
        chrome_options.add_argument("--incognito")

        # Inicializa a aplicação MSAL
        try:        
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret,
            )
        except BaseException as err:
            print(f'Falha ao iniciar aplicação MSAL: {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado por falha aplicação MSAL. Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)

        # Inicia o fluxo de código de autorização
        try:
            flow = app.initiate_auth_code_flow(scopes=self.scope, redirect_uri=self.redirect_uri)
            auth_url = flow["auth_uri"]
            self.response = f"Acessando a URL de autenticação Microsoft Entra ID (antiga Azure AD): {auth_url}"
            self.logger.info(self.response)
        except BaseException as err:
            print(f'Falha no fluxo de autorização Microsoft Entra ID (antiga Azure AD): {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado por falha no fluxo de autorização Microsoft Entra ID (antiga Azure AD). Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)            

        # Inicializa o ChromeDriver com redirecionamento de saída
        try:
            service = Service(ChromeDriverManager().install())
            service.start()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(auth_url)
        except BaseException as err:
            print(f'Falha na inicialização do Chrome: {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado na inicialização do Chrome. Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)                    

        class AuthHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                self.server.logger.info("%s - - [%s] %s\n" %
                                        (self.client_address[0],
                                         self.log_date_time_string(),
                                         format % args))

            def do_GET(self):
                parsed_path = urlparse.urlparse(self.path)
                query_params = urlparse.parse_qs(parsed_path.query)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Captura o código de autorização e o estado
                if 'code' in query_params and 'state' in query_params:
                    self.server.auth_code = query_params['code'][0]
                    self.server.state = query_params['state'][0]
                    self.wfile.write(b'''
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 16px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: #007bff;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Autentica&#231;&#227;o realizada com sucesso!</h1>
                                            Aguarde que esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     ''')
                else:
                    self.wfile.write(b'''
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 16px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: red;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Falha na autentica&#231;&#227;o!</h1>
                                            Esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     ''')

        # Inicializa o servidor HTTP
        self.server = HTTPServer(('localhost', 8000), AuthHandler)
        self.server.logger = self.logger  # Passa o logger para o servidor

        # Função para monitorar o tempo limite
        def monitor_timeout():
            time.sleep(self.timeout)
            if not hasattr(self.server, 'auth_code'):
                self.response = "tempo limite para autenticação foi excedido"
                self.status_code = 490
                self.logger.error(self.response)
                sys.stdout.close()
                sys.stderr.close()
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                print(f'Código retorno: {self.status_code} ', end='') ## self.status_code = 200, usuário pertence ao grupo informado. self.status_code = 299, grupo existe mas usuário NÃO pertence à ele. Erros retornam 4xx.
                print(f'Resposta: {self.response}', end='\n\n')  
                print('Falha na autenticação! Execução abortada!')
                driver.quit()
                self.server.server_close()
                os._exit(0)       

        # Inicia a thread para monitorar o tempo limite
        timeout_thread = threading.Thread(target=monitor_timeout)
        timeout_thread.start()

        # Espera pelo código de autorização
        self.response = "Esperando pela autenticação..."
        self.logger.info(self.response)
        self.server.handle_request()

        # Restaura stdout e stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Verifica se o código de autorização foi obtido dentro do tempo limite
        if not hasattr(self.server, 'auth_code'):
            return

        # Obtém o código de autorização e o estado capturados pelo servidor HTTP
        auth_code = self.server.auth_code
        state = self.server.state

        # Adquire o token usando o código de autorização, verificando o estado
        try:
            result = app.acquire_token_by_auth_code_flow(flow, {"code": auth_code, "state": state})
        except ValueError as e:
            self.response = f"Erro ao obter o token de acesso: {e}"
            self.status_code = 401
            self.logger.error(self.response)
            driver.quit()
            return

        if "access_token" in result:
            access_token = result['access_token']
            headers = {
                'Authorization': 'Bearer ' + access_token
            }

            # Obtém o email do usuário autenticado
            me_response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers=headers
            )
            self.status_code = me_response.status_code
            if me_response.status_code == 200:
                me_data = me_response.json()
                user_email = me_data['userPrincipalName']
                self.response = f"Email do usuário autenticado: {user_email}"
                self.logger.info(self.response)

                # Verifica se o usuário pertence ao grupo
                group_name = self.grupo

                # Obtém o ID do usuário
                user_response = requests.get(
                    f'https://graph.microsoft.com/v1.0/users/{user_email}',
                    headers=headers
                )
                self.status_code = user_response.status_code
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user_id = user_data['id']

                    # Pesquisa o grupo pelo nome
                    group_response = requests.get(
                        f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{group_name}'",
                        headers=headers
                    )
                    self.status_code = group_response.status_code
                    if group_response.status_code == 200:
                        group_data = group_response.json()
                        if 'value' in group_data and len(group_data['value']) > 0:
                            group_id = group_data['value'][0]['id']

                            # Verifica se o usuário está no grupo
                            members_response = requests.get(
                                f'https://graph.microsoft.com/v1.0/groups/{group_id}/members',
                                headers=headers
                            )
                            self.status_code = members_response.status_code
                            if members_response.status_code == 200:
                                members_data = members_response.json()
                                if 'value' in members_data:
                                    user_in_group = any(member['id'] == user_id for member in members_data['value'])
                                    if user_in_group:
                                        self.response = f"O usuário {user_email} liberado para uso desta aplicação."
                                    else:
                                        self.response = f"O usuário {user_email} NÃO liberado para uso desta aplicação. Solicite acesso à TI."
                                        self.status_code = 299
                                else:
                                    self.response = "Resposta da API de membros não contém a chave 'value'."
                                    self.status_code = 460
                            else:
                                self.response = f"Erro na resposta da API de membros: {members_response.status_code}"
                                self.response += f"\n{members_response.json()}"
                        else:
                            self.response = f"Grupo '{group_name}' não encontrado."
                            self.status_code = 470
                    else:
                        self.response = f"Erro na resposta da API de grupos: {group_response.status_code}"
                        self.response += f"\n{group_response.json()}"
                else:
                    self.response = f"Erro na resposta da API de usuário: {user_response.status_code}"
                    self.response += f"\n{user_response.json()}"
            else:
                self.response = f"Erro ao obter informações do usuário: {me_response.status_code}"
                self.response += f"\n{me_response.json()}"
        else:
            self.response = f"Erro ao obter o token de acesso: {result.get('error')}"
            self.response += f"\n{result.get('error_description')}"
            self.status_code = 480
    
        # Fecha o navegador
        driver.quit()
        service.stop()

        # Define o retorno
        print(f'\nCódigo retorno: {self.status_code} ', end='') ## self.status_code = 200, usuário pertence ao grupo informado. self.status_code = 299, grupo existe mas usuário NÃO pertence à ele. Erros retornam 4xx.
        print(f'Resposta: {self.response}', end='\n\n')  
        if self.status_code == 200:
            print('Acesso autorizado!')
        else:
            print('Permissões inválidas! Execução abortada!')
            os._exit(0)        

    def disclaimer(self): # Mostra o aviso do funcionamento e necessidade de autenticação
        input(f'''
              
        Para ser utilizado de forma adequada e segura, este script requer autenticação no Microsoft Entra ID (antiga Azure AD).
        Também requer que seu usuário pertença a um grupo de segurança específico. Se você não tem a segurança que tem permissão de uso, solicite previamente à TI.
        
        Para continuar, é necessário fornecer suas credenciais, aquelas que costumeiramente utiliza para acessar os serviços de e-mail corporativo.
        Uma janela de navegador será aberta e você será direcionado à tela de Logon do Microsoft Entra ID.
        Faça o Logon fornecendo usuário, senha e validação de duplo fator (no autenticador da Microsoft, instalado em seu celular).        
        Após a autenticação, a janela do navegador será fechada e o script iniciará o processo de execução.

        Você tem {self.timeout} segundos para realizar a autenticação ou a execução será abortada.

        Tecle [ENTER] para continuar ...
        
        ''')

class postgreSQL: # Classe de acesso e interação com banco PostgreSQL      
    def __init__(self, config, logger=None):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        try:
            self.Conexao = psycopg2.connect(**config)  ## na chamada de uma função/método, o * explode os valores de um dicionário em argumentos posicionais (só valores) e ** explode discionário em argumentos nominais (nome=valor)
        except Exception as Err:
            raise

    def csv_df(self, CsvPath, CsvDelim=';'): # Le arquivo CSV e gera Dataframe do Pandas
        try:
            DataFrame = pd.read_csv(CsvPath, delimiter=CsvDelim)  # Verifique se o delimitador é ';'
            DataFrame.replace({np.nan: None}, inplace=True)  ## troca 'NaN' por None (null no postgresql)
            return DataFrame
        except Exception as Err:
            raise

    def db_insert_df(self, DataFrame, Tabela, Schema=None, Colunas=None, OnConflict=None): # Insere os dados de um dataframe em uma tabela equivalente no banco (exige mesma estrutura de colunas)
        # Essa função exige que os nomes dos cabeçalhos das colunas do CSV sejam os mesmos das colunas da tabela de destino
        Colunas = Colunas or DataFrame.columns.tolist()     # Caso não seja fornecida a lista de colunas, assume as colunas do DataFrame
        Valores = [tuple(Linha) for Linha in DataFrame[Colunas].values]    
        Schema = Schema or 'public'
        Query = f'insert into {Schema}.{Tabela} ({', '.join(Colunas)}) values %s '
        if not OnConflict is None:
            Query = Query + OnConflict

        try:
            self.Cursor = self.Conexao.cursor() 
            execute_values(self.Cursor, Query, Valores)  
            self.Conexao.commit()
        except Exception as Err:
            self.Conexao.rollback()
            raise
        finally:        
            self.Cursor.close()
            #Conexao.close() ## conexão precisa ser fechada explicitamente fora da classe

    def db_select(self, Query): # Retorna um cursor à partir de um select
        BlackList = ['INSERT ', 'DELETE ', 'UPDATE ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas consultas. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None    
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                Dados = self.Cursor.fetchall()
                Colunas = [Col[0] for Col in self.Cursor.description]
                self.Conexao.commit()
                self.Cursor.close()
                return Dados, Colunas
            except Exception as Err:
                self.Conexao.rollback()
                raise   

    def db_update(self, Query): # Retorna um cursor à partir de um select
        UpdRows = 0
        BlackList = ['INSERT ', 'DELETE ', 'SELECT ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas updates. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None            
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                UpdRows = self.Cursor.rowcount
                self.Conexao.commit()
                self.Cursor.close()
                return UpdRows
            except Exception as Err:
                self.Conexao.rollback()
                raise  

class api_rest: # Classe para interação com APIs Rest (especialmente Sienge)
    def __init__(self, url, credenciais, cadencia=3, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        if not validators.url(url):
            self.logger.critico('URL inválida: {url}. Primeiro parametro precisar uma URL válida. Script abortado', exit=1)
        if not isinstance(credenciais, dict):
            self.logger.critico('O segundo parametro posicional precisa ser um dicionário. Script abortado', exit=1)

        self.RetEndPoint = None  # Inicializa self.RetEndPoint como None            
        self.Headers = headers
        self.Verify = verify            
        self.Url = url
        self.Timeout = timeout
        self.Credenciais = credenciais
        self.Cadencia = 1/cadencia  ## candencia corresponde a chamadas por segundo, não minuto
        self.TempoUltReq = None 
        self.Intervalo = self.Cadencia + 1     

    def controla_cadencia(self): ## para controle apenas, não deve ser chamada fora da classe
        # Verificar o tempo atual
        Agora = time.time()
        
        # Calcular intervalo entre requisições
        if self.TempoUltReq:
            self.Intervalo = Agora - self.TempoUltReq
        else:
            self.Intervalo = float('inf')  # Primeira requisição não espera
        
        # Calcular o tempo de espera necessário para respeitar o limite
        if self.Intervalo < self.Cadencia:
            self.Espera = self.Cadencia - self.Intervalo
            time.sleep(self.Espera)
            return self.Espera
        else:
            self.Espera = 0
            return self.Espera, self.Intervalo

    def auth_basic(self): # Autentica e abre sessão na API 
        if not self.Credenciais['user'] or not self.Credenciais['password']:
            self.logger.critico('Dicionário de credenciais não possui chaves "user" e/ou "password". Script abortado', exit=1)             
        try:          
            self.Sessao = requests.Session()
            #Sessao.auth = (ApiUser, ApiPass)
            self.Sessao.auth = HTTPBasicAuth(self.Credenciais['user'], self.Credenciais['password'])
            Auth = self.Sessao.post(self.Url)  
            #print(f'Status: {Auth.status_code}')
            #print(f'Retorno: {Auth.text}')
            return self.Sessao
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}", exit=1)

    def auth_bearer(self): # Autentica e abre sessão na API
        #self.UrlLogin = UrlLogin if UrlLogin is not None else self.Url
        try:          
            self.Sessao = requests.Session()
            Token = self.Sessao.post(self.Url, headers=self.Headers, json=self.Credenciais, verify=self.Verify)            
            self.Headers.update({"Authorization": f"Bearer {Token.text}"})
            if 200 <= Token.status_code <= 299:
                self.Sessao.status_code = Token.status_code
                self.Sessao.token = Token.text
                return self.Sessao
            else:
                self.logger.critico(f"Erro ao autenticar API: {Token.status_code} - {Token.text}", exit=1)    
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}", exit=1)    

    def endpoint_json(self, endpoint, metodo, payload=None): # Interage com End Point
        self.ult_tempo_req = time.time() 
        self.Metodo = metodo.lower()
        #self.EndPoint = self.Url + endpoint
        self.EndPoint = endpoint
        self.Payload = payload
        MetodosAceitos = ['post', 'get', 'patch', 'put']
        if not any(element in self.Metodo for element in MetodosAceitos):
            self.logger.critico(f'Método {self.Metodo} não previsto. Abortando chamada!', exit=1)
        else:
            ChamadaApi = f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify)' if self.Payload is None else f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify, json=self.Payload)'
            self.controla_cadencia()
            self.TempoUltReq = time.time()   
            try: 
                self.RetEndPoint = eval(ChamadaApi)
                if self.RetEndPoint.status_code >= 500:
                    self.logger.critico(f'Erro {self.RetEndPoint.status_code} na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nResposta: {self.RetEndPoint.text}', exit=1)   
                self.RetEndPoint.Espera = self.Espera ## adiona o tempo de espera ao retorno da API
                self.RetEndPoint.Intervalo = self.Intervalo ## adiciona o intervalo entre chamada ao retorno da API                                
                return self.RetEndPoint
            except requests.exceptions.ReadTimeout as Err:
                self.logger.critico(f'Excedido tempo limite {self.Timeout} para retorno do endpoint: {Err}\nEndpoint: {self.EndPoint}', exit=1)            
            except Exception as Err:
                self.logger.critico(f'Falha na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nCodigo retorno: {self.RetEndPoint.status_code}\nResposta:{self.RetEndPoint.text}', exit=1)

    def trata_erro_sienge(CodRet, Retorno):
        if not 200 <= CodRet <= 299:        
            try:
                DicRetorno = eval(Retorno.replace('null','None').replace(r'\n\t',' '))
                if 'clientMessage' in DicRetorno and DicRetorno['clientMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['clientMessage']
                elif 'developerMessage' in DicRetorno and DicRetorno['developerMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['developerMessage']
                elif 'message' in DicRetorno and DicRetorno['message'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['message']
                else:
                    MsgErro = Retorno
            except:
                MsgErro = Retorno.replace(r'\n\t',' ')        
            finally:
                return MsgErro
        else:
            return Retorno      

    def close(self): # Encerra a cessão
        self.Sessao.close()                   

class lbx_logger: # Classe para gerenciar a saída para log
    class LevelFilter(logging.Filter):    
        def __init__(self, levels_to_ignore):
            self.levels_to_ignore = levels_to_ignore
        
        def filter(self, record):
            return record.levelno not in self.levels_to_ignore

    def __init__(self, log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None):
        self.ignore_file = [] if ignore_file is None else ignore_file       
        self.ignore_console = [] if ignore_console is None else ignore_console
        self.modulo = __name__ if modulo is None else modulo
        self.logger = logging.getLogger(self.modulo)
        self.logger.setLevel(log_level)
        self.msg = ''
        self.log_file_path = log_file_path
        
        if log_file_path:
            # Criando um handler para escrever em um arquivo de log
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(log_level)  # Sempre registrar tudo no arquivo
            
            # Criando um handler para exibir no console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar DEBUG e acima no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            file_handler.addFilter(self.LevelFilter(self.ignore_file))
            console_handler.addFilter(self.LevelFilter(self.ignore_console))

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Adicionando os handlers ao logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        else:
            # Tudo direcionado para o console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            console_handler.addFilter(self.LevelFilter(self.ignore_console))        

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            console_handler.setFormatter(formatter)
            
            # Adicionando o handler ao logger
            self.logger.addHandler(console_handler)
        
        # Redirecionando exceções para o logger
        sys.excepthook = self.handle_exception
        
        # Redirecionando saída padrão
        self.original_stdout = sys.stdout
        sys.stdout = self
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exceção não prevista", exc_info=(exc_type, exc_value, exc_traceback))

    def print(self, *args, **kwargs):
        # Imprime diretamente na saída padrão
        print(*args, **kwargs, file=self.original_stdout)

    def add(self, message, corte=None):
        message = message[:corte] if corte else message
        self.msg = self.msg + message if not message is None else self.msg
    
    def write(self, message):
        if message.strip():  # Ignorar mensagens vazias
            self.logger.info(message.strip())
    
    def flush(self):
        pass  # Método necessário para compatibilidade com sys.stdout
    
    def debug(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.debug(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
    
    def info(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.info(msg)
        self.msg = ''
        if exit:
            os._exit(exit)        
    
    def aviso(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.warning(msg)
        self.msg = ''
        if exit:
            os._exit(exit)

    def erro(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.error(msg)
        self.msg = ''
        if exit:
            os._exit(exit)

    def critico(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.critical(msg)
        self.msg = ''
        if exit:
            os._exit(exit)

    def stop_logging(self):
        # Restaurar o stdout original
        sys.stdout = self.original_stdout
        # Remover handlers do logger
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def filtra(self, log_file, dh_ini, dh_fim):
        # Validar parametros de entrada
        if dh_ini:
            if not isinstance(dh_ini, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_ini) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_ini += ":00"
                try:
                    self.inicio = datetime.datetime.strptime(dh_ini, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.inicio = dh_ini
        else:
            self.inicio = datetime.datetime.now() - datetime.timedelta(hours=1) ## assume a última hora como intervalo, se omisso

        if dh_fim:
            if not isinstance(dh_fim, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_fim) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_fim += ":00"
                try:
                    self.fim = datetime.datetime.strptime(dh_fim, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.fim = dh_fim
        else:
            self.fim = datetime.datetime.now() ## assume a última hora como intervalo, se omisso

        if not log_file and not self.log_file_path:
            self.logger.critical('Nenhum arquivo de log disponível. Log desta instância configurado apenas para exibição em tela, sem registro em arquivo')
            return None
        elif not log_file and self.log_file_path:
            log_file_path = self.log_file_path
        elif log_file:
            if Path(log_file).is_file():
                log_file_path = log_file
            else:
                self.logger.critical(f'Arquivo de log {log_file} não existe!')
                return None
        else:
            self.logger.critical('Erro validação arquivo de entrada. Abortando!')
            return None
                   
        # Função para verificar se a linha está dentro do intervalo de tempo
        def is_within_time_range(timestamp, dh_inicio, dh_fim):
            return dh_inicio <= timestamp <= dh_fim

        # Ler e filtrar o arquivo de log com a codificação ISO-8859-1
        with open(log_file_path, 'r', encoding='ISO-8859-1') as log_file:
            log_lines = log_file.readlines()

        # Variável para armazenar o último timestamp válido
        last_valid_timestamp = None
        filtered_lines = []

        for line in log_lines:
            try:
                # Extraia a data e a hora da linha
                timestamp_str = line.split()[0] + " " + line.split()[1]
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                last_valid_timestamp = timestamp
                if is_within_time_range(timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)
            except Exception as e:
                # Caso a linha não tenha um carimbo de tempo, use o último timestamp válido
                if last_valid_timestamp and is_within_time_range(last_valid_timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)

        # Retornar o objeto contendo as linhas filtradas
        return filtered_lines
                
class misc: # Classe de miscelâneas
    def __init__(self):
        return None

    # Picker para selecionar arquivo
    def seleciona_arquivo(DirBase, TiposArquivo=[('Todos os arquivos', '*.*')], Titulo='Selecionar arquivo'):    
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal do Tkinter
        Arquivo = filedialog.askopenfilename(initialdir=DirBase, filetypes=TiposArquivo, title=Titulo)
        Arquivo = Path(Arquivo)
        root.destroy()
        return Arquivo

    # Picker para selecionar diretório
    def seleciona_dir(DirBase=Path(r'./'), Titulo='Selecionar diretório'):
        root = tk.Tk() # objeto picker  (Tkinter)para selecionar arquivos e diretórios
        root.withdraw()  # Esconde a janela principal do Tkinter
        Diretorio = filedialog.askdirectory(initialdir=DirBase, title=Titulo)
        Diretorio = Path(Diretorio)
        root.destroy()
        return Diretorio

    # Limpa e padroniza nomes
    def normaliza(Original):
        Lixo = r'/\\?%§ªº°`´^~*:|"<>!@#$%¨&*()_+=-[]{}"\' ' 
        Normalizar = normalize('NFKD', Original).encode('ASCII', 'ignore').decode('ASCII')
        RemoverLixo = [c if c not in Lixo else '_' for c in Normalizar]    
        Limpo = "".join(RemoverLixo)
        Limpo = re.sub(r'\.(?=.*\.)', '_', Limpo) # troca todos os pontos por underline
        Limpo = re.sub(r'_+', '_', Limpo)  # limpa as reptições do underline
        return Limpo.lower()

    # Captura a referencia da janela atual para retornar o foco à ela depois de chamar os pickers
    def get_cmd_window():
        pid = os.getpid()
        windows = gw.getWindowsWithTitle("")
        for window in windows:
            if window.title and window.visible and window.topleft:
                return window
        return None

    def maximize_console():
        # Ajustar o buffer de console
        # os.system('mode con: cols=500 lines=100')
        
        # Obter o handle da janela do console
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        
        if hWnd:
            # Definir as dimensões da tela
            user32.ShowWindow(hWnd, 3)  # 3 = SW_MAXIMIZE  