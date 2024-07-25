import requests
import json
from utils import SERVER, APLICATIVO
from banco_dados import SelectBD


class GerenciadorApi:

    def __init__(self) -> None:
        pass

    def __get_headers(self) -> dict:
        try:
            token = SelectBD().select_one('SELECT * FROM sessoes ORDER BY session_id DESC LIMIT 1;')
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token["token"]}'
            }
        except Exception as e:
            return {}

    def __response(self, url: str, method: str, data: str | None = None) -> dict:
        try:
            if data is None:
                data = {}

            if method == 'GET':
                response = requests.get(url, headers=self.__get_headers())

            elif method == 'POST':
                response = requests.post(url, headers=self.__get_headers(), data=data)

            elif method == 'PUT':
                response = requests.put(url, headers=self.__get_headers(), data=data)

            else:
                return {}

            if response.status_code == 200 or response.status_code == 201:
                return response.json()['data']
            else:
                return {}

        except requests.exceptions.RequestException as e:
            return {}
        except Exception as e:
            return {}

    def find_all_sessions_user(self, user_id: int) -> dict:
        __url = f'http://{SERVER}/sessoes?user_id={user_id}'
        return self.__response(__url, 'GET')

    def find_all_sesions_by_application_and_user(self, user_id: int) -> dict:
        __url = f'http://{SERVER}/sessoes/{APLICATIVO}?user_id={user_id}'
        return self.__response(__url, 'GET')

    def find_last_session_by_application_and_user(self, user_id: int) -> dict:
        __url = f'http://{SERVER}/sessoes/last/{APLICATIVO}?user_id={user_id}'
        return self.__response(__url, 'GET')

    def find_all_applications_by_application_name(self) -> dict:
        __url = f'http://{SERVER}/aplicativos/system/{APLICATIVO}'
        return self.__response(__url, 'GET')

    def find_by_application_name(self) -> dict:
        __url = f'http://{SERVER}/aplicativos/name/{APLICATIVO}'
        return self.__response(__url, 'GET')

    def get_process(self, server_ip: str) -> dict:
        __url = f'http://{SERVER}/ativador/{APLICATIVO}/{server_ip}'
        return self.__response(__url, 'GET')

    def find_filas_by_application(self, ip_server: str) -> dict:
        __url = f'http://{SERVER}/fila/{APLICATIVO}/{ip_server}'
        return self.__response(__url, 'GET')

    def find_auth_by_application_and_user(self, user_id: int) -> dict:
        __url = f'http://{SERVER}/aplicativos/system/{APLICATIVO}/user?user_id={user_id}'
        return self.__response(__url, 'GET')

    def create_session_by_user(self, payload: str) -> dict:
        __url = f'http://{SERVER}/sessoes/{APLICATIVO}'
        return self.__response(__url, 'POST', payload)

    def create_process(self, payload: str) -> dict:
        __url = f'http://{SERVER}/ativador'
        return self.__response(__url, 'POST', payload)

    def update_fila(self, payload: str) -> dict:
        __url = f'http://{SERVER}/fila/{APLICATIVO}'
        return self.__response(__url, 'PUT', payload)

    def update_password(self, password: str) -> dict:
        __url = f'http://{SERVER}/aplicativos/system/update-password?application={APLICATIVO}&password={password}'
        return self.__response(__url, 'PUT')

    def force_reestart_service(self, server: str, tipo_processo: str) -> dict:
        payload = json.dumps({
            'server': server,
            'application': APLICATIVO,
            'tipoProcesso': tipo_processo,
        })
        __url = f'http://{SERVER}/ativador/reestart'
        return self.__response(__url, 'POST', payload)


