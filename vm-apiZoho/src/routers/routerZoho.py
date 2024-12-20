from fastapi import APIRouter
from src.service.zoho import Zoho
from src.service.propiedadesService import ZohoWorkProperty
from src.service.serviceFiles import Intital
import asyncio
from asyncio import Semaphore


router = APIRouter()

"""
ruta inical de files 959rm5ac03102cb5041569ebffccf94326c44
"""

@router.get("/")
async def init():
    return {"ok":200}

@router.get("/getMenu/")
async def getMenu():
    ini = Intital()
    access_token =  await ini.getData() 
    zoho = Zoho()
    data = zoho.get_teamfolder_folders(access_token)
    workdrive = ZohoWorkProperty()
    folder_details = workdrive.extract_folder_details(data)
    return folder_details     


"""
@router.post("/getNewToken/{token}")
async def getToke(token):
    zoho = Zoho()
    data = zoho.refreshToken(token)
    return data

"""
#959rm4c69c978101c433b912e48836d90d84f
#959rmc5aa2e98c96f42a0a65b885a64f1d630    autos

@router.post("/get_teamfolder_details")
async def get_teamfolder_details(teamfolder_id: str):
    # Inicializa el token de acceso
    ini = Intital()
    access_token = await ini.getData()

    # Instancias de clases
    zoho = Zoho()
    workdrive = ZohoWorkProperty()

    # Controlar el número de tareas concurrentes
    semaphore = Semaphore(10)  # Ajusta según los límites de Zoho y el servidor

    async def fetch_data_with_limit(func, *args, **kwargs):
        async with semaphore:
            return await asyncio.to_thread(func, *args, **kwargs)

    # Obtén las carpetas principales
    teamfolders_data = await fetch_data_with_limit(
        zoho.get_teamfolder_folders, access_token, teamfolder_id=teamfolder_id
    )
    folder_details = workdrive.extract_folder_details(teamfolders_data)

    async def get_subfolders_recursively(folder_id, folder_name, depth=0, max_depth=3):
        if depth >= max_depth:
            return []

        # Obtener subcarpetas
        subfolders_data = await fetch_data_with_limit(zoho.get_sub_folders, folder_id, access_token)
        subfolders_data_resolved = await subfolders_data
        subfolders_details = workdrive.extract_folder_details(subfolders_data_resolved)

        # Procesa archivos en la carpeta actual
        files_data = await fetch_data_with_limit(zoho.get_private_folder_files, folder_id, access_token)
        files_data_resolved = await files_data
        files_details = workdrive.extract_image_data(files_data_resolved)

        # Si no hay subcarpetas, devolver los archivos y el nombre de la carpeta
        if not subfolders_details:
            return {
                "id": folder_id,
                "name": folder_name,  # Incluye el nombre de la carpeta
                "files": files_details,
                "subfolders": []  # Asegúrate de que subfolders sea una lista vacía si no hay subcarpetas
            }

        # Si hay subcarpetas, procesarlas recursivamente
        tasks = [
            get_subfolders_recursively(subfolder['id'], subfolder['name'], depth + 1, max_depth)
            for subfolder in subfolders_details
        ]
        subfolders_results = await asyncio.gather(*tasks)

        # Asocia los subfolders con sus resultados
        for subfolder, subfolder_subs in zip(subfolders_details, subfolders_results):
            subfolder['subfolders'] = subfolder_subs

        # En el último nivel (sin subcarpetas), asegúrate de incluir los archivos
        if depth == max_depth - 1:
            for subfolder in subfolders_details:
                if 'files' not in subfolder:  # Si no tiene archivos, procesarlos
                    files_data = await fetch_data_with_limit(zoho.get_private_folder_files, subfolder['id'], access_token)
                    files_data_resolved = await files_data
                    files_details = workdrive.extract_image_data(files_data_resolved)
                    subfolder['files'] = files_details

        return {
            "id": folder_id,
            "name": folder_name,  # Incluye el nombre de la carpeta
            "files": files_details,
            "subfolders": subfolders_details
        }

    # Procesar carpetas principales en paralelo, pasando también el nombre de cada carpeta
    tasks = [get_subfolders_recursively(folder['id'], folder['name']) for folder in folder_details]
    folders_with_subfolders = await asyncio.gather(*tasks)

    return folders_with_subfolders


"""
@router.post("/get_teamfolder/auto/anio")
async def get_teamfolder_details(folderId):
    ini = Intital()
    access_token =  await ini.getData() 
    zoho = Zoho()
    data = zoho.get_teamfolder_folders(access_token,teamfolder_id=folderId)
    workdrive = ZohoWorkProperty()
    folder_details = workdrive.extract_folder_details(data)
    print(len(folder_details))
    print(folder_details , "data")
    if len(folder_details) ==1:
        end_drive = folder_details[0]['id']
        files =zoho.get_private_folder_files(end_drive,access_token)
        print("soy files",files)
    elif len(folder_details) ==0:
        files =zoho.get_private_folder_files(folderId,access_token)
        datos = extract_image_data(files)
        return datos

    return folder_details
"""
"Crear una una forma de poder obtenr los id de las carpetas pa poderdetrminar si es vehiculo o propiedad"
"""
1000.9f2945b1a9b34b9563b7216baf8193db.fdb819e7f75448d7b9a174b1e12df1f9
#959rm4c69c978101c433b912e48836d90d84f
#959rmc5aa2e98c96f42a0a65b885a64f1d630    autos

@router.post("/get_subFolders/")
async def get_subFolders( teamfolder_id,access_token):
    zoho = Zoho()
    data = zoho.get_subFolders(teamfolder_id,access_token)
    workdrive = ZohoWorkProperty()
    folder_details = workdrive.extract_folder_details(data)
    print(folder_details)
    return folder_details 
"""

"""
1000.9f2945b1a9b34b9563b7216baf8193db.fdb819e7f75448d7b9a174b1e12df1f9
p1q5l6dc993f5a22d45138c287fa4b42e10f0


@router.post("/getFiles/")
async def getFiles(myfolder_id, access_token):
    zoho = Zoho()
    data = zoho.get_private_folder_files(myfolder_id,access_token)
    workdrive = ZohoWorkProperty()
    folder_details = workdrive.extract_folder_details(data)
    datos = extract_image_data(data)
    return datos

"""

def extract_image_data(json_data):
    """
    Extrae las propiedades necesarias para crear un carrusel de imágenes.
    """
    images = []
    
    for item in json_data.get("data", []):
        if item["type"] == "files" and "attributes" in item:
            attributes = item["attributes"]
            if "thumbnail_url" in attributes:
                images.append({
                    "id": item["id"],
                    "name": attributes.get("name", "Sin título"),
                    "thumbnail_url": attributes["thumbnail_url"],
                    "download_url": attributes.get("download_url", "")
                })
    
    return images
    