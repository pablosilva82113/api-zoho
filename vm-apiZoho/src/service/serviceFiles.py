from database.tables.tokenTable import Token
from .zoho import Zoho
from datetime import datetime, timedelta
import json
from .propiedadesService import ZohoWorkProperty

class Intital:
    def __init__(self):
        self.token = Token()
        self.zoho = Zoho()
        self.work = ZohoWorkProperty()

    async def getData(self):
        # Obtener el token más reciente
        token_data = self.token.firtsOrDefault(
            f"id = 1",
            "ORDER BY id DESC LIMIT 1",
        )
        if not token_data:
            print("No se encontró un token.")
            return None
        tok = token_data['new_token']

        # Validar si ha pasado 50 minutos
        token_time = token_data['time']  # Ya es un objeto datetime
        now = datetime.now()
        time_difference = now - token_time

        if time_difference >= timedelta(minutes=50):
            # Si ha pasado más de 50 minutos, obtener nuevos datos del token
            data = self.zoho.refreshToken(tok)
            print("El token tiene más de 50 minutos.")

            # Extraer el nuevo access_token de los datos obtenidos
            new_access_token = str(data)  # Ajusta según la estructura de la respuesta

            # Actualizar la tabla con el nuevo access_token y la fecha de actualización
            set_values = "acces_token = %s, time = now()"
            where_condition = "id = %s"
            params = (new_access_token, token_data['id'])
            
            # Actualiza el campo 'acces_token' en la tabla usando el método Update
            self.token.Update(set_values, where_condition, params)

            # Verifica si `acces_token` es un objeto de tipo bytes, si lo es, lo decodifica a str
            token_str = token_data['acces_token']
            if isinstance(token_str, bytes):
                token_str = token_str.decode('utf-8')  # Decodifica los bytes a una cadena

            # Ahora puedes hacer la operación .replace() de manera segura
            raw_string = token_str.replace("'", '"')
            data = json.loads(raw_string)
            token = data.get('access_token', '')
            return token
        else:
            # Si el token es válido (no ha pasado 50 minutos), simplemente usamos el token actual
            token_str = token_data['acces_token']
            if isinstance(token_str, bytes):
                token_str = token_str.decode('utf-8')  # Decodifica los bytes a una cadena

            # Realiza la operación .replace() de manera segura
            raw_string = token_str.replace("'", '"')
            data = json.loads(raw_string)
            token = data.get('access_token', '')
            return token
