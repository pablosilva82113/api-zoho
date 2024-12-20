# Base image
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /vm-apiZoho

# Copiar el archivo de requisitos al contenedor desde la carpeta vmapizoho
COPY vm-apiZoho/requirements.txt ./requirements.txt

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de la carpeta vmapizoho al contenedor
COPY vm-apiZoho/ .

# Exponer el puerto 80 (definido en tu archivo main.py)
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
