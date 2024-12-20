import html

class ZohoWorkProperty:
    def __init__(self):
        pass

    def extract_folder_details(self, json_data):
        # Lista para almacenar los detalles (nombre y id) de las carpetas
        folder_details = []

        # Verificar que la clave "data" existe en el JSON
        if "data" in json_data:
            # Iterar sobre los elementos de la lista "data"
            for item in json_data["data"]:
                # Verificar que "display_attr_name" y "id" existen
                if "attributes" in item and "display_attr_name" in item["attributes"] and "id" in item:
                    # Decodificar las entidades HTML en el nombre
                    name = html.unescape(item["attributes"]["display_attr_name"])
                    # Agregar los detalles de la carpeta a la lista
                    folder_details.append({
                        "id": item["id"],
                        "name": name
                    })

        # Devolver la lista de detalles de las carpetas
        return folder_details
    
    def extract_image_data(self, json_data):
        """
        Extrae las propiedades necesarias para crear un carrusel de imágenes.
        """
        images = []
        
        # Verificar si json_data es un diccionario con clave "data"
        if isinstance(json_data, dict):
            data = json_data.get("data", [])
        elif isinstance(json_data, list):
            data = json_data
        else:
            raise ValueError(f"Formato inesperado de json_data: {type(json_data)}")
        
        # Procesar los elementos en "data"
        for item in data:
            if item.get("type") == "files" and "attributes" in item:
                attributes = item["attributes"]
                if "thumbnail_url" in attributes:
                    images.append({
                        "id": item["id"],
                        "name": attributes.get("name", "Sin título"),
                        "thumbnail_url": attributes["thumbnail_url"],
                        "download_url": attributes.get("download_url", "")
                    })
        
        return images

        
