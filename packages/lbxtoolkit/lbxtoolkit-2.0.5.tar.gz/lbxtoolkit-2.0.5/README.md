# Biblioteca de ferramentas LBX S/A

Esta biblioteca possui ferramentas de uso recorrente para interação com banco de dados e API, além de autenticação/validação de credenciais de usuário no Microsoft Entra ID

## Classe e funções

**auth_EntraID**:        Usa o Microsoft Entra ID (antiga Azure AD) para evitar execução não autorizada
  - _.disclaimer_:       Mensagem sobre a necessidade de autenticação
  - _.valida_grupo_:     Autentica o usuário e aborta se checa não pertencer ao grupo de segurança


**postgreSQL**:          Interage com o banco de dados PostgreSQL
  - _.db_:               Inicia sessão com o banco
  - _.csv_df_:           Lê arquivo CSV e gera Dataframe (pandas) a partir dele
  - _.db_insert_df_:     Insere informações de Dataframe em tabela do banco com estrutura equivalente
  - _.db_select_:        Retorna um cursor a partir de uma query
  - _.db_update_:        Executa update em tabelas


**api_rest**:            Interage com APIs RESTfull, especialmente providas para a plataforma Sienge
  - _.auth_base_:        Autentica (HTTPBasicAuth) sessão na API
  - _.auth_bearer_:      Autentica sessão na API pelos métodos: OAuth, JWT, Bearer  
  - _.endpoint_json_:    Realizad chama ao endpoint. Payload em formato `json` opcional.
  - _.trata_erro_sienge_: Retorna a mensagem de erro do Sienge caso código de retorno seja diferente de 200.
  - _.close_:            Encerra a sessão autenticada

**lbx_logger**:          Manipula e formata as mensagens de saída do script para direcioná-las para tela (stdout) e/ou arquivo de log
  - _.add_:              Adiciona a mensagem a um _buffer_ sem exibir, acumulando até a próxima chamada em algum dos níveis abaixo.
  - _.print_:            Contorna o manipulador de log e imprime diretamente na tela (stdout), sem formatar a mensagem nem registrar no arquivo
  - _.debug, .info, .aviso, .erro, .critico_:  Classifica as mensagens por nível de severidade/relevância e rediciona a saída (arquivo, tela, tela+arquivo) conforme a configuração do nível
  - _.stop_logging_:   Interrompe a manipulação das saídas pelo logger e restaura as saídas padrão (stdout/stderr) para a tela 
  - _.filtra_:          Filtra os eventos do arquivo de log registrados em um intervalo de tempo específico

**misc**:                 Classe de miscelâneas/diversos
  - _.seleciona_arquivo_: Abre um picker do sistema operacionar para selecionar um *arquivo* e retorna seu path
  - _.seleciona_dir_:     Abre um picker do sistema operacionar para selecionar um *diretório* e retorna seu path
  - _.normaliza_:         Limpa caracteres especiais e espaços de strings e retorna tudo em minúsculo
  - _.get_cmd_window_:    Captura a referencia da janela atual (cmd.exe) para retornar o foco à ela depois de chamar os pickers 
  - _.maximize_console_:  Maxima a janela do console (cmd.exe)

## Instalação e uso:

### Instalação

```
pip install lbx_toolkit
```

### Uso
```
from lbx_toolkit import auth_EntraID, PostgreSQL, api_rest, lbx_logger
```

#### Classe **auth_EntraID**

Este recurso tem o propósito de controlar as permissões de execução do script usando as credencias do ambiente AD em nuvem da Microsoft (Azure AD >> Microsoft Entra ID), abortando se a autentição falhar ou o usuário não pertencer ao grupo.

Essa classe possui apenas dois métodos:

- `auth_EntraID.disclaimer()`: apenas exibe uma tela de informações/instruções ao usuário.

- `auth_EntraID.valida_grupo([client_id], [client_secret], [tenant_id], timeout=60, log_file='auth_EntraID.log')`: efetua a autenticação do usuário e verifica se ele pertence ao grupo informado,  abortando a execução caso não pertença ao grupo ou a autenticação não seja validada no tempo estabelecido. Os argumentos `timeout` e `log_file` são opcionais e, se omitidos, os valores aqui atribuídos serão adotados como padrão.

É necessário obter parametros da plataforma de identidade da Microsoft (AD Azure, agora Microsoft Entra ID), no [*Centro de administração do Microsoft Entra*](https://entra.microsoft.com).
Sugerimos não armazenar estas ou outras informações sensíveis no script. Considere usar o pacote `dotenv` para isso.

Os argumentos obrigatórios (posicionais) são:

1) `tenant_id` corresponde ao campo *ID do Locatário*, que pode ser obtido na página [visão geral de identidade do domínio](https://entra.microsoft.com/#blade/Microsoft_AAD_IAM/TenantOverview.ReactView)

2) `client_id` corresponde ao *ID do aplicativo (cliente)*, obtido na secção [_Identidade > Aplicativos > Registros de Aplicativo_](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM). Considere não reaproveitar aplicativos e criar um específico para essa finalidade.

3) `secret_id` corresponde ao *Valor* do _ID secreto_ (não ao próprio ID Secreto) do aplicativo. Este token não é passivel de consulta após gerado e para obtê-lo, é necessário criar um novo segredo para o aplicativo na subsecção _"Certificados e Segredos"_, após clicar no nome do aplicativo exibo na indicada no item (2). O token (_Valor do segredo_) deve ser copiado e anotado no ato da criação, pois *não é possível consultá-lo posteriormente*.


```
from lbx_toolkit import auth_EntraID

client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'
tenant_id = 'SEU_TENANT_ID'

# inicializa instância
auth = auth_EntraID(client_id, client_secret, tenant_id, timeout=60, log_file='auth_EntraID.log')  

# exibe a mensagem padrão de aviso
auth.disclaimer()

auth.valida_grupo('Nome do Grupo de Distribuição') 
# se usuário não pertencer a grupo informado, a execução do script é abortada.
```

#### Classe **postgreSQL**

Recursos de interação com o banco de dados relacional PostgreSQL

1) O método `postgreSQl.db()` exige que as credenciais e parametros de acesso sejam fornecidas em um *dicionário* com, ao mínimo, o seguinte formato:

```
credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
              }

conexao = postgreSQL.db(credenciais)
```

O nome do schema é ser declarado no contexto da query, mas se desejar alterar o schema padrão, adicione *`'options' : '-c search_path=[NOME_SCHEMA]',`* ao dicionário.

Qualquer argumento de conexão previsto no pacote *psycopg2* são aceitos como entrada no dicionário acima.

2) O método `postgreSQl.csv_df()` lê arquivo texto do tipo CSV e o converte para o objeto Dataframe do `pandas`. A assinatura da função exige que se forneça o caminho do arquivo CSV e, opcionalmente o caracter delimitador. Se o caracter demilitador não for informado, será assumido `;`. Considere usar a função `Path` para tratar o caminho do arquivo de origem.

```
from pathlib import Path
arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'
```

3) O método `postgreSQl.db_insert_df()` insere dados a partir de um Dataframe (pandas) em uma tabela do banco com estrutura de colunas equivalente.

A assinatura da função é `postgreSQL.db_insert_df([conexao], [dataframe_origem], [tabela_destino], Schema=None, Colunas=None, OnConflict=None)`

É necessário que os nomes das colunas do dataframe coincidam com o nome das colunas da tabela. 
Não há como traduzir/compatibilizar (de-para) nomes de colunas entre o dataframe e a tabela.

Os três primeiros parametros são posicionais e correspondem, respectivamente, (1) ao objeto da conexão com o banco, (2) ao objeto que contém o dataframe e (3) ao nome da tabela de destino.
Assume-se que a tabela pertença ao schema padrão (definido na variável _search_path_ do servidor). Caso a tabela de destino esteja em um _schema_ diferente do padrão, deve-se informar seu nome no parâmetro opcional `Schema`.

O parametro opcional `Colunas` espera um objeto do tipo _lista_ que contenha a relação das colunas a serem importadas. 
As colunas listadas neste objeto precisam existir nas duas pontas (dataframe e tabela).
Caso seja omisso, todas as colunas do dataframe serão inseridas na tabela. Neste caso, admite-se que haja colunas na tabela que não exitam no dataframe (serão gravadas como NULL), mas o contrário provocará erro. 

O último parametro opcional `OnConflict` espera uma declaração para tratar o que fazer caso o dado a ser inserido já exista na tabela, baseado na cláusula [*ON CONFLICT*](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT) do comando INSERT. A claúsula deve ser declarada explicita e integralmente nessa variável (clausula, _target_ e _action_) e não há crítica/validação desse argumento, podendo gerar erros se declarado inconforme com o padrão SQL.

Exemplo de uso:

```
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
              }

conexao = postgreSQL.db(credenciais)

arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'

postgreSQL.db_insert_df(conexao, dados, 'teste_table', Schema='meu_esquema', OnConflict='on conflict (coluna_chave_primaria) do nothing')

# conexão com o banco precisa ser fechada explicitamente após a chamada do método, caso não seja mais utilizada:
conexao.close()
```

4) O método `postgreSQl.db_select()` executa consultas no banco de dados e retorna um `cursor` com o resultado.

A assinatura da função é `postgreSQL.db_select([conexao], [query])`

São permitidas apenas instruções de consulta (podendo serem complexas, por exemplo, com uso de [CTE](https://www.postgresql.org/docs/current/queries-with.html)). A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query, se presentes.

O `cursor` é fechado no contexto do método, antes do retorno, *não podendo* ser manipulado após recebido como retorno da função.

A função retorna *dois objetos*, o primeiro contendo os dados do cursor, o segundo, contendo os nomes das respectivas colunas.

Exemplo de uso:

```
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
              }

conexao = postgreSQL.db(credenciais)

query = 'select * from meu_esquema.teste_table'

dados, colunas = postgreSQL.db_select(conexao, query)
conexao.close()
```

5) O método `postgreSQl.db_update()` executa updates no banco

A assinatura da função é `postgreSQL.db_update([conexao], [query])`

São permitidas apenas instruções de update. A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query.

A função retorna *a quantidade de linhas alteradas*.

Exemplo de uso:

```
from lbx_toolkit import postgreSQL
from pathlib import Path

credenciais = {
                'dbname': 'NOME_BANCO',
                'user': 'USUARIO'',        
                'password': 'SENHA',     
                'host': 'IP_OU_DNS_SERVIDOR',
                'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
              }

conexao = postgreSQL.db(credenciais)

query = "update meu_esquema.teste_table set coluna='novo_valor' where pk='chave'"

result = postgreSQL.db_update(conexao, query)
conexao.close()
```

#### Classe **api_rest**

Destina-se a interatir com APIs RESTfull, em especial as publicadas pela SoftPlan para a [Plataforma Sienge](https://api.sienge.com.br/docs/).

A classe deve ser instanciada conforme sintaxe abaixo:

`api_rest(url, credenciais, cadencia, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True)`

São nessários 2 parâmetros posicionais obrigatórios, e 5 parametros nominais facultativos (valor padrão, se omisso, indicado na sintaxe acima):
  - `url`: o endereço da URL de autenticação da API
  - `crednciais`: Dicionário com credenciais de autenticação. 
  - `cadencia` Número máximo de chamadas *por segudo* à API 
  - `timeout` Tempo máximo (segundos) para aguardar retorno à chamada. Padrão 6s, se omisso.
  - `logger` O objeto _log handler_ para lidar com as informações de saída. Se não informado, todas as saídas serão direcionadas para a stdout.
  - `headers` Cabeçalhos _http_ para a requisição à API.
  - `verify` Verifica a validade do certificado SSL do servidor de destino da requisição.

Quanto às credenciais de autenticação, assim como a classe de interação com o PostgreSQL, elas precisam ser fornecidas na forma de um *dicionário*. 
Para o método `api_rest.aut_basic()`, o formato deve ser: 
```
credenciais = {
                'user': 'USUARIO_API',
                'password': 'TOKEN_USUARIO'
              }
```
Caso a autenticação seja pelo método `api_rest.aut_bearer()`, o dicionário deve corresponder ao formato previsto pelo endpoint e seu conteúdo será enviado como um JSON ao endereço indicado no parametro `url`


A classe possui 3 métodos: 
  - `api_rest.auth_basic()`: instanciamento da sessão autenticando pelo método HTTPBasicAuth
  - `api_rest.auth_bearer()`: instanciamento da sessão autenticando pelos métodos OAuth, JWT, Bearer    
  - `api_rest.endpoint_json([endereço], [método], payload=None)`: para a chamada ao endpoint
  - `close()` para encerra a instância/sessão

O consumo é feito pelo método `api_rest.endpoint_json` que suporta apenas APIs cujo payload (opcional) seja aceito no formato JSON. 

Esse método espera 2 parametros posicionais obrigatórios: o endereço do endpoint e o verbo (get, post, patch ou put), tendo parametro opcional o objeto de 'payload' (json). 
Note que o endereço do endpoint deve ser informado completo. A URL informada no instanciamento da classe corresponde apenas ao endereço de autenticação. 

O tempo, em segundos, transcorrido entre a chamada a atual e a chamada anterior ao endpoint pode ser consultado pelo argumento `.Intervalo` no objeto recebido do retorno à chamada ao método `.endpoint_json`. 

Da mesma forma, o tempo de espera imposto para respeitar a cadência do webservcie também pode ser consultado pelo argumento `.Espera`.

Exemplo de uso:

```
from lbx_toolkit import api_rest

UrlBase=r'https://api.sienge.com.br/lbx/public/api/v1'
Credenciais = {
                'user': 'USUARIO_API',
                'password': 'TOKEN_USUARIO'
              }
ApiSienge = api_rest(UrlBase,Credenciais,2.5) # limite de 2 requisições/segundo para cadência de chamada ao endpoint
Auth = ApiSienge.auth_basic()

Nutitulo=input('Numero do título:')
Nuparcela=input('Numero da parcela:')
Vencimento=input('Vencimento [AAAA-MM-DD]:')
Payload = {
                "dueDate": f"{Vencimento}"
            }
EndPoint = f'{UrlBase}/bills/{Nutitulo}/installments/{Nuparcela}'

#chama o endpoint e recebe o retorno no objeto AlteraVcto
AlteraVcto = ApiSienge.endpoint_json(EndPoint, 'patch', Payload)
```

No exemplo acima não é esperado que o endpoint retorne nenhum dado (`patch`).

Quando se usa o verbo `get` e se espera o retorno de algum dado, use o método `.json` do pacote `request` para acessar o objeto recebido.

Para uso em APIs com autenticação JWT (JSON Web Token), OAuth, Bearer Token Authentication, a construção é a mesma indicada acima, bastando-se usar `.auth_bearer()` ao invés de _.auth_basic()_, e ajustar o dicionário `credenciais` informado no instanciamento da classe, que deve ser estruturado conforme o padrão fornecido peo mantendor da API e será enviado como payload ao endpoint (`json=credenciais`). 

#### Classe **lbx_logger**

Essa classe requer a importação do módulo `logging` no script em que for instanciada e tem o propósito de manipular/formatar as mensagens de saída do script, alterando o formato e redirecionando destino padrão (stdout e stderr) para uma combinação de tela e/ou arquivo.

O comportamento padrão é registrar todas as saídas *simultaneamente* em tela e no arquivo com endereço informado no parâmetro `log_file_path`. Se este parametro for omisso no instanciamento da classe, as mensagens serão exibidas apenas na tela.

A mensagens devem ser classificadas por grau de severidade/relevância, da menor para a maior, na seguinte ordem: *debug, info, warning (aviso), error (erro), critical (critico)*

A classificação do nível de serveridade da mensagem se dá pelo método escolhido para invocar a mensagem, correspondente aos níveis de severidade equivalentes.

A classe deve ser instanciada conforme sintaxe abaixo:

`lbx_logger(log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None):`

Todos os parametros são nominativos e facultativos. Em caso de omissão, os valores padrão são assumidos conforme o exemplo acima.

Os parametros para o instanciamento da classe são:

- `log_file_path` Define o caminho e o nome do arquivo de log. Se omisso, as mensagens serão todas direcionadas apenas para a tela.
- `log_level` Define o nível mínimo de severidade das mensagens a serem manipuladas pelo logger. Se omisso, será assumido o nível mais baixo (_debug_). As mensagens com nível abaixo do especificado são descartadas. Os níveis devem ser informados de acordo com a sintaxe acima (prefixados com _logging._ e com o nome do nível em inglês e maiúsculas). Exemplo: 
  - `logging.DEBUG` para manipular chamadas do método *.debug()* e acima.
  - `logging.INFO` para manipular chamadas do método *.info()* e acima.
  - `logging.WARNING` para manipular chamadas do método *.aviso()* e acima.
  - `logging.ERROR` para manipular chamadas do método *.erro()* e acima.
  - `logging.CRITICAL` para manipular chamadas do método *.critico()* e acima.        
- `formato_log` Define o formato em que a mensagem será apresentada. Se omisso, o padrá é *DATA_HORA - NIVEL - MENSAGEM*. Para maiores opções veja: [Atributos de log](https://docs.python.org/3/library/logging.html#logrecord-attributes)
- `modulo` Nome do módulo para o qual os logs serão monitorados. Permite instanciar várias vezes a classe para criar manipuladores diferentes para módulos diferente. Informe o nome do módulo para criar um log específico para ele ou simplesmente omita o parametro para criar um log para o script em geral.
- `ignore_console` Lista com os níveis de severidade a serem ignorados para *apresentação na tela*, registrando *apenas no arquivo* (quando informado no parametro `log_file_path`) e obedecendo ao nível mínimo estabelecido no parametro `log_level`. Note que omitir o parametro `log_file_path` e incluir um nível na lsita `ignore_console` implica em ignorar/suprimir esse nível de mensagem de qualquer apresentação.
- `ignore_file` Mesma lógica do parametro `ignore_console`, mas com lógica invertida: suprime o registro do nível do arquivo e demonstra *apenas na tela*.

1) As mensagem são manipuladas substituindo-se o comando `print()` pela chamada a um dos 5 métodos acima (_.add(), .debug(), .info(), .aviso(), .erro(), .critico()_). Exceto o método `.add()`, qualquer um dos demais métodos pode interromper a execução do script, através da passagem do parâmetro `exit`. Ao informar esse parametro na chamadada do método, atribua a ele o código de saída desejado (0 para normal, qualquer outro número para saída com erro). Exemplo:

```
log.erro('Essa mensagem apenas resulta em uma mensagem de nível ERROR')
log.erro('Essa mensagem resulta em uma mensagem de nível ERRO e encerra o script com código de retorno -1', exit=-1)
```

Qualquer chamada ao comando `print()`, uma vez instanciado manipulador de log, será registada como uma chamada ao método _.info()_ e registrada com este nível de severidade. 
Para retornar ao comportamente padrão do comando print, ou interromper o manipulador, faça chamada ao método `.stop_logging()`

2) O método _.add()_ não exibe/grava imediatamente a mensagem, mas apenas a diciona a _buffer_. Todas as chamas a _.add()_ irão concatenar a mensagem recebida até a próxima chamada em algum dos níveis _.debug(), .info(), .aviso(), .erro(), .critico()_. Na primeira chama de um destes níveis após uma (ou mais) chamada(s) ao método _.add()_ o *buffer* será concatenado à mensagem recebida por um destes métodos e o resultado será manipulado pelo log conforme os parametros definidos no intanciamento da classe e o método chamado. Essa função é útil para tratar mensagens com retorno condicional. Exemplo:

```
log.add('Mensagem 1# ') ## não será exibida/registrada
log.add('Mensagem 2# ') ## não será exibida/registrada
log.info('Mensagem 3) ## será exibida/registrada como nível "info" e com texto: "Mensagem 1# Mensagem 2# Mensagem 3"
```

3) Os métodos que exibem as mensagens (`.debug()`,`.info()`,`.aviso()`, `.erro()`, `.critico()`) possuem 3 parametros: `message`, `corte=None`, `exit=None`.

 - `message`: posicional e obrigatório. corresponde à mensagem a ser exibida
 - `corte`: o tamanho máximo da mensagem a ser exibida. opcional e se omitido, exibe a mensagem inteira. se fornecido, corta a mensagem no comprimento informado
 - `exit`: opcional. se informado (requer um código de retorno), aborta o script com o código informado. se omisso (padrão) a mensagem apenas é minutada pelo log, sem interferir no funcionamento do script

4) O método `.filtra()` possui 3 parametros posicionais, todos opcionais: `log_file`, `dh_ini`, `dh_fim`.

Se os 3 forem omitidos, serão exibidas as entradas de log do arquivo corrente, definido no instanciamento da classe `lbx_logger`, registradas na última hora. Deste modo, o valor padrão para `dh_fim` é `now()`  e para `dh_ini` é `now()` menos 1 hora.

Caso queira filtrar os registro de outro arquivo de log, que não seja o do script corrente, informe o endereço do arquivo no primeiro parametro.

E caso queira alterar alterar o período de filtragem, informe nos parametros 2 e 3 a data/hora de início e fim do período. Estes dois parametros aceitam tanto um objeto do tipo `datetime` como uma string (que será convertida para datetime), desde que ela esteja no formato `dd/mm/aaaa hh:mm:[ss]` (segundos são opcionais).

Considerando que os parametros são posicionais, caso queira omitir apenas um dos parametros, preencha a posição do parametro a ser omitido com `None`.

A saída dessa função retorna um objeto, que pode ser salvo em disco ou impresso na tela.


5) Exemplos de uso:

```
from lbx_toolkit import lbx_logger 
import logging
import os
from pathlib import Path

DirBase = Path('./')  # diretório corrente do script
BaseName = os.path.splitext(os.path.basename(__file__))[0] # nome do script sem extensão
LogFile = Path(DirBase, BaseName + '.log') # salva logs no diretório corrente, em um arquivo nomeado com nome do script + extensão ".log"

### instancia o manipulador para tratar todas as mensagens (nível DEBUG acima), 
#   mas suprime a apresentação em tela das mensagens de nível "DEBUG" na tela, 
#   apenas registrando-as somente no arquivo
#   e sumprime o registro no arquivo das mensagens de nível "ERROR", 
#   mostrando-as apenas na tela
log = lbx_logger(LogFile, logging.DEBUG, ignore_console=[logging.DEBUG], ignore_file=[logging.ERROR]) 

# Exemplo de mensagens de log
log.debug('Esta é uma mensagem de debug') 
log.info('Esta é uma mensagem informativa')
log.add('Esta mensagem não será exibida agora, mas acumulada no buffer# ')
log.aviso('Esta é uma mensagem de aviso')
log.erro('Esta é uma mensagem de erro')
log.erro('Esta é uma mensagem erro muito comprida e será limitada a 40 caracteres, o restante será cortado e ingorado ao ser manipulado', 40)
log.critico('Esta é uma mensagem crítica')

# Exemplo de função que gera uma exceção
def funcao_com_erro():
    raise ValueError('Este é um erro de exemplo')

# Testando redirecionamento de print e captura de exceção
print('Mensagem de teste via print')
try:
    funcao_com_erro()
except Exception as e:
    print(f'Capturado um erro: {e}')

log.erro('Essa é uma mensagem de erro e abortará a execução do script', exit=1)

log.info('Essa mensagem não será exibida pois o script foi abortado na mensagem anterior')

# obtem os registros de log da última hora (comportamento padrão)
filtra_log = log.search() 

# obtem os registros das últimas 6 horas
ultimas_6h = datetime.datetime.now() - datetime.timedelta(hours=6) ## carimbo de tempo de 6 horas atrás !!! requer>> import datetime
filtra_log = log.search(None, ultimas_6h) # None no 1º parametro impõe o log do arquivo corrente como padrão (definido em 'LogFile' e apontado no instanciamento da classe)

# obtem os registros do dia 14/01/2020 até 3h atrás
ultimas_3h = datetime.datetime.now() - datetime.timedelta(hours=3) ## carimbo de tempo de 6 horas atrás !!! requer>> import datetime
filtra_log = log.search(None, '14/01/2020 00:00', ultimas_3h) # 

# obtem os registros do horário comercial do dia 23/12/2023 do arquivo salvo em C:\temp\outro_arquivo.log
Outro_Log = Path(r'c:\temp\outro_arquivo.log')
filtra_log = log.search(Outro_Log, '23/12/2023 08:00', '23/12/2023 18:00') # 

# salva conteúdo filtrado em um arquivo:
filtrado = 'filtered_log.txt'
with open(filtado, 'w', encoding='ISO-8859-1') as output_file:  # indique o enconding conforme salvo (UTF-8 ou ISO-8859-1)
    output_file.writelines(filta_log)    

# mostra o conteúdo filtrado na tela
print(''.join(filtra_log))

# mostra o conteúdo filtrado na tela, listando apenas as os registros do nível "DEBUG"
for line in filtered_lines:
    if "DEBUG" in line:
        print(line, end='')
```

#### Classe **misc**

Classe que reune pequenas funções uteis para agilizar tarefas comuns.

Sintaxe e exemplos de uso. Parametros omissos assume  os valores padrão indicados abaixo:

  - `Arquivo = seleciona_arquivo(DirBase, TiposArquivo=[('Todos os arquivos', '*.*')], Titulo='Selecionar arquivo')`
  - `Diretório = seleciona_dir(DirBase=Path(r'./'), Titulo='Selecionar diretório'):`
  - `NomeLimpo = normaliza('String # SEM Noção!') #>>> string_sem_nocao`
  - `cmd_window = get_cmd_window()`
  - `maximize_console()`