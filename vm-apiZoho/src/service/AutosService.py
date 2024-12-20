class ZohoWorkDrive:
    def __init__(self, json_data):
        self.json_data = json_data
    
    def extract_folder_details(self):
        # Lista para almacenar los detalles (nombre y id) de las carpetas
        folder_details = []
        
        # Verificar que la clave "data" existe en el JSON
        if "data" in self.json_data:
            # Iterar sobre los elementos de la lista "data"
            for item in self.json_data["data"]:
                # Verificar que "display_attr_name" y "id" existen
                if "display_attr_name" in item["attributes"] and "id" in item:
                    # Agregar los detalles de la carpeta a la lista (nombre y id)
                    folder_details.append({
                        "id": item["id"],
                        "name": item["attributes"]["display_attr_name"]
                    })
        
        # Devolver la lista de detalles de las carpetas
        return folder_details
    
    def extract_Subfolder_details(self):
            # Lista para almacenar los detalles (nombre y id) de las carpetas
            folder_details = []
            
            # Verificar que la clave "data" existe en el JSON
            if "data" in self.json_data:
                # Iterar sobre los elementos de la lista "data"
                for item in self.json_data["data"]:
                    # Verificar que "display_attr_name" y "id" existen
                    if "display_attr_name" in item["attributes"] and "id" in item:
                        # Agregar los detalles de la carpeta a la lista (nombre y id)
                        folder_details.append({
                            "id": item["id"],
                            "name": item["attributes"]["display_attr_name"]
                        })
            
            # Devolver la lista de detalles de las carpetas
            return folder_details