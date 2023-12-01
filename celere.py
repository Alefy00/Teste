import requests
import base64
import logging
from sqlalchemy import create_engine, Column, String, Integer, Boolean, MetaData, Table
import sqlalchemy.exc

# Chave da API da T-Shield
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6WyI2NTkzMjMxNTE3MiIsIjY1OTMyMzE1MTcyIl0sImp0aSI6IjMwODhlMjZmYjE1ZjQ4MDZiYzMwMmQ2NTJmZmU3OTgzIiwidXNlcklkIjoiMTIyNjMxIiwiY2xpZW50SWQiOiIxOTc1NyIsIkNhbkxpc3RBbmFseXNpcyI6Ikxpc3RhciBhbmFsaXNlcyIsIkNhbkNyZWF0ZUFuYWx5c2lzIjoiQ3JpYXIgYW7DoWxpc2VzIiwiQ2FuQ3JlYXRlRXh0ZXJuYWxBbmFseXNpcyI6IkNyaWFyIGFuw6FsaXNlIEV4dGVybmEiLCJDYW5DcmVhdGVJbnRlcm5hbEFuYWx5c2lzIjoiQ3JpYXIgYW7DoWxpc2UgSW50ZXJuYSIsIkNhbkNyZWF0ZVRvdXJpc21BbmFseXNpcyI6IkNyaWFyIGFuw6FsaXNlIFR1cmlzbW8iLCJDYW5PcGVuQW5hbHlzaXNEZXRhaWxzIjoiVmlzdWFsaXphciBkZXRhbGhlcyBkYSBhbsOhbGlzZSIsIkNhbkFwcHJvdmVBbmFseXNpc01hbnVhbGx5IjoiQXByb3ZhciBhbsOhbGlzZSBtYW51YWxtZW50ZSIsIkNhbkxpc3RQZXJzb25zIjoiTGlzdGFyIHBlc3NvYXMiLCJDYW5DcmVhdGVQZXJzb24iOiJDcmlhciBwZXNzb2EiLCJDYW5PcGVuUGVyc29uRGV0YWlscyI6IlZpc3VhbGl6YXIgZGV0YWxoZXMgZGEgcGVzc29hIiwiQ2FuTGlzdFBlcnNvblRyYW5zYWN0aW9ucyI6Ikxpc3RhciB0cmFuc2HDp8O1ZXMgZGEgcGVzc29hIiwiQ2FuT3BlblRyYW5zYWN0aW9uQ3JlZGl0Q2FyZCI6IlZpc3VhbGl6YXIgY2FydMOjbyBkZSBjcsOpZGl0byBkYSB0cmFuc2HDp8OjbyIsIkNhbkFwcHJvdmVUcmFuc2FjdGlvbk1hbnVhbGx5IjoiQXByb3ZhciB0cmFuc2HDp8OjbyBtYW51YWxtZW50ZSIsIkNhbkNyZWF0ZVRyYW5zYWN0aW9uIjoiQ3JpYXIgdHJhbnNhw6fDo28gcGFyYSBwZXNzb2EiLCJDYW5SZVNlbmRQZXJzb25MaW5rIjoiUmVlbnZpYXIgbGluayBwYXJhIHBlc3NvYSIsIkNhblJlbW92ZVBlcnNvbiI6IlJlbW92ZXIgcGVzc29hIiwiQ2FuRXhwb3J0RXhjZWxQZXJzb25MaXN0IjoiRXhwb3J0YXIgbGlzdGEgZGUgcGVzc29hcyBlbSBleGNlbCIsIkNhbkxpc3RVc2VycyI6Ikxpc3RhciB1c3XDoXJpb3MiLCJDYW5DcmVhdGVVc2VyIjoiQ3JpYXIgdXN1w6FyaW8iLCJDYW5PcGVuVXNlckRldGFpbHMiOiJWaXN1YWxpemFyIGRldGFsaGVzIGRvIHVzdcOhcmlvIiwiQ2FuRWRpdFVzZXIiOiJFZGl0YXIgdXN1w6FyaW8iLCJDYW5SZVNlbmRVc2VyTGluayI6IlJlZW52aWFyIGxpbmsgcGFyYSB1c3XDoXJpbyIsIkNhbkFjdGl2YXRlSW5hY3RpdmF0ZVVzZXIiOiJBdGl2YXIvSW5hdGl2YXIgdXN1w6FyaW8iLCJDYW5MaXN0Q29uZmlndXJhdGlvbnMiOiJMaXN0YXIgY29uZmlndXJhw6fDtWVzIiwiQ2FuTGlzdENvbnNvbGlkYXRvcnMiOiJMaXN0YXIgY29uc29saWRhZG9yYXMiLCJDYW5DcmVhdGVDb25zb2xpZGF0b3IiOiJDcmlhciBjb25zb2xpZGFkb3JhIiwiQ2FuRWRpdENvbnNvbGlkYXRvciI6IkVkaXRhciBjb25zb2xpZGFkb3JhIiwiQ2FuUmVtb3ZlQ29uc29saWRhdG9yIjoiUmVtb3ZlciBjb25zb2xpZGFkb3JhIiwiQ2FuT3BlbkNvbnNvbGlkYXRvclBhc3N3b3JkIjoiVmlzdWFsaXphciBzZW5oYSBkZSBjb25zb2xpZGFkb3JhIiwiQ2FuTGlzdEFuYWx5c2lzRGVmYXVsdENvbmZpZ3VyYXRpb25zIjoiTGlzdGFyIGNvbmZpZ3VyYcOnw6NvIGRlIGFuw6FsaXNlcyBwYWRyw6NvIiwiQ2FuQ3JlYXRlQW5hbHlzaXNEZWZhdWx0Q29uZmlndXJhdGlvbiI6IkNyaWFyIGNvbmZpZ3VyYcOnw6NvIGRlIGFuw6FsaXNlIHBhZHLDo28gKFBGKSIsIkNhbkVkaXRBbmFseXNpc0RlZmF1bHRDb25maWd1cmF0aW9uIjoiRWRpdGFyIGNvbmZpZ3VyYcOnw6NvIGRlIGFuw6FsaXNlIHBhZHLDo28iLCJDYW5SZW1vdmVBbmFseXNpc0RlZmF1bHRDb25maWd1cmF0aW9uIjoiUmVtb3ZlciBjb25maWd1cmHDp8OjbyBkZSBhbsOhbGlzZSBwYWRyw6NvIiwiQ2FuTGlzdFByb2ZpbGVzIjoiTGlzdGFyIHBlcmZpcyIsIkNhbkNyZWF0ZVByb2ZpbGUiOiJDcmlhciBwZXJmaWwiLCJDYW5FZGl0UHJvZmlsZSI6IkVkaXRhciBwZXJmaWwiLCJDYW5PcGVuQW5hbHlzaXNEb2N1bWVudCI6IlZpc3VhbGl6YXIgZG9jdW1lbnRvIiwiQ2FuUmVtb3ZlQW5hbHlzaXMiOiJSZW1vdmVyIGFuw6FsaXNlIiwiQ2FuTGlzdEFsbEFuYWx5c2lzIjoiTGlzdGFyIHRvZGFzIGFuw6FsaXNlcyIsIkNhbkxpc3RDb21wYW5pZXMiOiJMaXN0YXIgZW1wcmVzYSIsIkNhbkNyZWF0ZUV4dGVybmFsQ29tcGFueSI6IkNhZGFzdHJhciBlbXByZXNhIiwiQ2FuT3BlbkNvbXBhbnlEZXRhaWxzIjoiVmlzdWFsaXphciBkZXRhbGhlcyBkYSBlbXByZXNhIiwiQ2FuUmVwcm9jZXNzQ29tcGFueVJlZ2lzdGVyIjoiUmVwcm9jZXNzYXIgY2FkYXN0cm8gZGEgZW1wcmVzYSIsIkNhbkNyZWF0ZUNvbXBhbnlBbmFseXNpcyI6IkNyaWFyIGFuw6FsaXNlIGRlIGVtcHJlc2EiLCJDYW5MaXN0Q29tcGFueUFuYWx5c2lzIjoiTGlzdGFyIGFuw6FsaXNlcyBkYSBlbXByZXNhIiwiQ2FuT3BlbkNvbXBhbnlBbmFseXNpc0RldGFpbHMiOiJWaXp1YWxpemFyIGRldGFsaGVzIGRhIGFuw6FsaXNlIGRhIGVtcHJlc2EiLCJDYW5DcmVhdGVQSkFuYWx5c2lzRGVmYXVsdENvbmZpZ3VyYXRpb24iOiJDcmlhciBjb25maWd1cmHDp8OjbyBkZSBhbsOhbGlzZSBwYWRyw6NvIChQSikiLCJDYW5MaXN0UGF5bWVudEdhdGV3YXlzIjoiTGlzdGFyIGdhdGV3YXlzIGRlIHBhZ2FtZW50b3MiLCJDYW5DcmVhdGVDbGllbnRQYXltZW50R2F0ZXdheSI6IkNyaWFyIGdhdGV3YXkgZGUgcGFnYW1lbnRvIiwiQ2FuUmVtb3ZlQ2xpZW50UGF5bWVudEdhdGV3YXkiOiJSZW1vdmVyIGdhdGV3YXkgZGUgcGFnYW1lbnRvIiwiQ2FuRWRpdENsaWVudFBheW1lbnRHYXRld2F5IjoiRWRpdGFyIGdhdGV3YXkgZGUgcGFnYW1lbnRvIiwiQ2FuTGlzdE90aGVyQW5hbHlzaXMiOiJMaXN0YXIgY29uZmlndXJhw6fDtWVzIGRlIG91dHJhcyBhbsOhbGlzZXMiLCJDYW5FZGl0T3RoZXJBbmFseXNpcyI6IkVkaXRhciBjb25maWd1cmHDp8O1ZXMgZGUgb3V0cmFzIGFuw6FsaXNlcyIsIkNhbkVkaXRUb2tlbkNvbmZpZ3VyYXRpb24iOiJFZGl0YXIgdG9rZW4gZGUgY29uZmlndXJhw6fDtWVzIGRlIG91dHJhcyBhbsOhbGlzZXMiLCJDYW5MaXN0Q29tcGFueVBhcnRuZXJBbmFseXNpcyI6Ikxpc3RhciBhbsOhbGlzZXMgZGUgc8OzY2lvcyIsIkNhbkxpc3RDbGllbnRTdXBwbGllckNyZWRlbnRpYWxzIjoiTGlzdGFyIGNyZWRlbmNpYWlzIGRlIGZvcm5lY2Vkb3JlcyIsIkNhbkNyZWF0ZUNsaWVudFN1cHBsaWVyQ3JlZGVudGlhbHMiOiJDcmlhciBjcmVkZW5jaWFpcyBkZSBmb3JuZWNlZG9yZXMiLCJDYW5SZW1vdmVDbGllbnRTdXBwbGllckNyZWRlbnRpYWxzIjoiUmVtb3ZlciBjcmVkZW5jaWFpcyBkZSBmb3JuZWNlZG9yZXMiLCJDYW5FZGl0Q2xpZW50U3VwcGxpZXJDcmVkZW50aWFscyI6IkVkaXRhciBjcmVkZW5jaWFpcyBkZSBmb3JuZWNlZG9yZXMiLCJDYW5PcGVuQW5hbHlzaXNPcmlnaW5hbERvY3VtZW50IjoiQWJyaXIgZSBiYWl4YXIgZG9jdW1lbnRvcyBvcmlnaW5haXMgZGEgYW7DoWxpc2UiLCJDYW5SZXByb2Nlc3NEb2N1bWVudEFuYWx5emVyIjoiUmVwcm9jZXNzYXIgYW7DoWxpc2UgZGUgZG9jdW1lbnRvIiwiQ2FuUmVtb3ZlQ29tcGFueSI6IlJlbW92ZXIgZW1wcmVzYSIsIkNhbkxpc3RUb2tlbkNhY2hlIjoiTGlzdGFyIHRva2VucyBlbSBhbmRhbWVudG8iLCJDYW5PcGVuVG9rZW5DYWNoZSI6IkFicmlyIGRldGFsaGVzIGRlIHRva2VuIGVtIGFuZGFtZW50byIsIkNhblJlbW92ZVRva2VuQ2FjaGUiOiJSZW1vdmVyIHRva2VuIGVtIGFuZGFtZW50byIsIkNhbkxpc3RBcmNoaXZlZEFuYWx5c2lzIjoiTGlzdGFyIGFuw6FsaXNlcyBhcnF1aXZhZGFzIiwiQ2FuQXJjaGl2ZUFuYWx5c2lzIjoiQXJxdWl2YXIgYW7DoWxpc2UiLCJDYW5PcGVuQXJjaGl2ZWRBbmFseXNpcyI6IlZpc3VhbGl6YXIgYW7DoWxpc2UgYXJxdWl2YWRhIiwiQ2FuQ3JlYXRlUGFyYW1ldGVyUnVsZXMiOiJDcmlhciByZWdyYXMgZGUgcGFyw6JtZXRyb3MiLCJDYW5DcmVhdGVMaXZlbmVzc1Rva2VuIjoiQ3JpYXIgdG9rZW4gZGUgbGl2ZW5lc3MgM2QiLCJDYW5SZW1vdmVQYXJhbWV0ZXJSdWxlcyI6IlJlbW92ZXIgcmVncmEgZGUgcGFyw6JtZXRybyBkZSBjbGllbnRlIiwiQ2FuQ3JlYXRlQ3JlZGl0RW5naW5lIjoiQ3JpYXIgbW90b3IgZGUgY3LDqWRpdG8iLCJDYW5PcGVuV2ViSG9va0xvZyI6Ikxpc3RhciBsb2cgZGUgV2ViSG9vayIsIkNhbkNyZWF0ZUNsaWVudExpdmVuZXNzTGF5b3V0IjoiQ3JpYXIgbGF5b3V0IGRlIGxpdmVuZXNzIiwiQ2FuT3BlbkNsaWVudENvbnN1bXB0aW9uUmVwb3J0IjoiVmlzdWFsaXphciByZWxhdMOzcmlvIGNvbnN1bW8gY2xpZW50ZSIsIkNhbkluc2VydEV4dGVybmFsSWQiOiJJbnNlcmlyIElkIEV4dGVybm8iLCJuYmYiOjE3MDE0NTc2NTcsImV4cCI6MTcwMTU0NDA1NywiaWF0IjoxNzAxNDU3NjU3LCJpc3MiOiJFeGVtcGxvSXNzdWVyIiwiYXVkIjoiRXhlbXBsb0F1ZGllbmNlIn0.Jt6MqN5Mj2gV2pI_Q5nSKHr8KsJPu8AaK7pkmWGcIiI'

# URL da API de Face ID da T-Shield
api_url = 'https://apih.tshield.com.br/api/consultas/face-id'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cadastro_cliente(cpf, nome, genero, endereco, cep, foto_path):
    # Validação dos dados do cliente
    if not cpf or not nome or not genero or not cep or not foto_path:
        logger.error("Dados do cliente incompletos. O cadastro não pode ser concluído.")
        return False

    # Lógica para cadastrar os dados do cliente no banco de dados
    try:
        # Utiliza um ORM para interagir com o banco de dados (SQLite e SQLAlchemy)
        engine = create_engine('sqlite:///cliente.db', echo=True)
        metadata = MetaData()

        # Definindo Tabela de clientes
        clientes = Table('clientes', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('cpf', String, unique=True),
                         Column('nome', String),
                         Column('genero', String),
                         Column('endereco', String),
                         Column('cep', String),
                         Column('foto_path', String),
                         Column('autorizado', Boolean, default=False)
                         )

        # Criando tabela se ela não existir
        metadata.create_all(engine)

        # Inserindo dados na tabela usando um context manager
        with engine.connect() as conn:
            conn.execute(clientes.insert().values(
                cpf=cpf, nome=nome, genero=genero, endereco=endereco, cep=cep, foto_path=foto_path))

        logger.info("Cliente cadastrado com sucesso.")
        return True
    except sqlalchemy.exc.IntegrityError as integrity_err:
        logger.error(f"Erro de integridade ao cadastrar cliente: {integrity_err}")
        return False
    except Exception as e:
        # Tratando erros específicos do banco de dados
        logger.error(f"Erro ao cadastrar cliente no banco de dados: {e}")
        return False

def verificar_face(imagem_path):
    try:
        # Lendo imagem
        with open(imagem_path, 'rb') as img_file:
            # Convertendo a imagem para base64
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        # Parâmetros da requisição
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {'image': encoded_image}

        # Fazendo a requisição para a API de Face ID
        response = requests.post(api_url, headers=headers, json=data)

        # Verificando o status da resposta
        if response.status_code == 200:
            resultado = response.json()

            # Verificando se a face pertence a um usuário autorizado
            if resultado.get('authorized', False):
                return True
            else:
                return False
        else:
            # Tratamento de erros
            print(f"Erro na requisição: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        # Tratamento de erros genéricos na requisição
        print(f"Erro na requisição: {e}")
        return False
    except Exception as e:
        # Tratamento de erros genéricos
        print(f"Erro: {e}")
        return False



# Teste de uso
if verificar_face('teste.jpg'):
    print("Face verificada com sucesso. Usuário autorizado.")
else:
    print("Validação Inconclusiva")
    # Teste de cliente
if cadastro_cliente('12345678901', 'Caio Alexandre', 'M', 'Cond park do gama', '72426-250', 'teste.jpg'):
    print("Cliente cadastrado com sucesso.")
else:
    print("Erro no cadastro do cliente.")
