import config as config
import requests , time
from database.tables.tokenTable import Token
import json
import aiohttp
import asyncio

class Zoho:
    def __init__(self):
        self.zoho_client_id = config.ZOHO_CLIENT_ID
        self.zoho_client_secret = config.ZOHO_CLIENT_SECRET
        self.tokens = Token()
        self.redirect_uri= config.Redirect_uri
        pass

    def refreshToken(self, token_refresh):
        url = f"https://accounts.zoho.com/oauth/v2/token?refresh_token={token_refresh}&client_id={self.zoho_client_id}&client_secret={self.zoho_client_secret}&redirect_uri={self.redirect_uri}&grant_type=refresh_token"
        try:
            response = requests.post(url)
            response_data = response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            return None
        except ValueError as e:
            return None
        
    def get_access_token(refresh_token, client_id, client_secret):
    # URL del endpoint OAuth2 de Zoho
        url = "https://accounts.zoho.com/oauth/v2/token"
        
        # Parámetros requeridos por OAuth2
        payload = {"scope":["WorkDrive.files.ALL"],"expiry_time":1733500953722,"client_id":"1000.XDJXDA2VEU844Z6VOESIUHMPBLBDQJ","client_secret":"08c7e019d0e962bbe38fb0499c570b9bf195c25767","code":"1000.25855398aac7a5c4cd93aa58dbc11514.90037b5c4657252c0804c67b26375c87","grant_type":"authorization_code"}
        # Encabezado necesario para enviar los datos como x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        

            # Realizar la solicitud POST
        response = requests.post(url, data=payload, headers=headers)
        
        data = response.json()
        print(json.dumps(data, indent=4))
            
            # Manejo de la respuesta
        return data
    


    def get_folders(self,access_token):
        url = "https://workdrive.zoho.com/api/v1/teamfolders"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error obteniendo los folders: ", response.json())
        
    
    def get_user_info(self,access_token):
        url = "https://www.zohoapis.com/workdrive/api/v1/users/me"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error obteniendo información del usuario: {response.json()}")
        
    def get_user_teams(self,zuid, access_token):
        url = f"https://www.zohoapis.com/workdrive/api/v1/users/{zuid}/teams"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener los equipos del usuario {zuid}: {response.json()}")
        
    def get_teamfolder_folders(self, access_token, limit=200, offset=0,teamfolder_id="959rm5ac03102cb5041569ebffccf94326c44",):
        # Construir la URL con el ID de la carpeta de equipo y los parámetros de paginación
        url = f"https://www.zohoapis.com/workdrive/api/v1/teamfolders/{teamfolder_id}/folders?page%5Blimit%5D={limit}&page%5Boffset%5D={offset}"
        
        # Encabezados con el token de acceso OAuth
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        
        # Realizar la solicitud GET
        response = requests.get(url, headers=headers)
        
        # Verificar el código de estado y manejar la respuesta
        if response.status_code == 200:
            # Si la solicitud es exitosa, devolver la respuesta en formato JSON
            return response.json()
        else:
            # Si hay un error, lanzar una excepción con el mensaje de error
            raise Exception(f"Error al obtener las carpetas del teamfolder {teamfolder_id}: {response.json()}")

    async def get_sub_folders(self, teamfolder_id, access_token, limit=200, offset=0):
        if not teamfolder_id or not access_token:
            raise ValueError("El ID del teamfolder y el token de acceso son obligatorios.")
        
        url = f"https://www.zohoapis.com/workdrive/api/v1/teamfolders/{teamfolder_id}/folders?page[limit]={limit}&page[offset]={offset}"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_details = await response.json()
                        raise Exception(f"Error al obtener carpetas: {error_details}")
            except aiohttp.ClientError as e:
                raise Exception(f"Error en la solicitud al obtener carpetas: {e}")
            
    def getFiles(self,resource_id,access_token):
        url =f"https://www.zohoapis.com/workdrive/api/v1/resourceproperty/{resource_id}"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Si la solicitud es exitosa, devolver la respuesta en formato JSON
            return response.json()
        else:
            # Si hay un error, lanzar una excepción con el mensaje de error
            raise Exception(f"Error al obtener las carpetas del teamfolder {resource_id}: {response.json()}")
        
    def getFileUrl(self,teamfolder_id,access_token):
        url = f"https://www.zohoapis.com/workdrive/api/v1/teamfolders/{teamfolder_id}/folders?page%5Blimit%5D=50&page%5Boffset%5D=0"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Si la solicitud es exitosa, devolver la respuesta en formato JSON
            return response.json()
        

    async def get_private_folder_files(self, resource_id, access_token):
        base_url = f"https://www.zohoapis.com/workdrive/api/v1/teamfolders/{resource_id}/files"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }

        async def fetch_page(session, offset, semaphore):
            url = f"{base_url}?page%5Blimit%5D=200&page%5Boffset%5D={offset}"
            async with semaphore:
                async with session.get(url) as response:
                    if response.status == 200:
                        try:
                            return await response.json()
                        except Exception as e:
                            raise Exception(f"Error parsing JSON response for folder {resource_id}: {e}")
                    else:
                        try:
                            error_details = await response.json()
                        except Exception:
                            error_details = {"error": "Invalid response format", "status_code": response.status}
                        raise Exception(f"Error fetching files for folder {resource_id}: {error_details}")

        async with aiohttp.ClientSession(headers=headers) as session:
            semaphore = asyncio.Semaphore(5)  # Limita a 5 solicitudes concurrentes
            offset = 0
            all_files = []

            # Fetch initial page to determine total files
            initial_data = await fetch_page(session, offset, semaphore)

            # Verificar si 'data' es una lista o un diccionario
            if isinstance(initial_data, dict) and "data" in initial_data:
                total_files = initial_data.get("info", {}).get("count", 0)
                all_files.extend(initial_data.get("data", []))
            elif isinstance(initial_data, list):
                total_files = len(initial_data)
                all_files.extend(initial_data)
            else:
                raise Exception(f"Unexpected response format: {initial_data}")

            # Schedule tasks for remaining pages
            tasks = [
                fetch_page(session, offset, semaphore)
                for offset in range(50, total_files, 50)
            ]

            # Introduce delay between batches of tasks
            results = []
            for i in range(0, len(tasks), 5):  # Procesa en lotes de 5 tareas
                batch = tasks[i:i+5]
                batch_results = await asyncio.gather(*batch, return_exceptions=True)
                results.extend(batch_results)
                await asyncio.sleep(1)  # Introduce un retraso de 1 segundo entre lotes

            for result in results:
                if isinstance(result, Exception):
                    # Log or handle the exception (opcional)
                    continue
                if isinstance(result, dict) and "data" in result:
                    all_files.extend(result.get("data", []))
                elif isinstance(result, list):
                    all_files.extend(result)

            return all_files