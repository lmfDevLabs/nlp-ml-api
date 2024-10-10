# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de credenciales de Google Cloud dentro del contenedor
COPY ./gcp_service_accounts/sensebuy-e8add-c83b372813c1.json /app/service-account-file.json

# Establecer la variable de entorno para que las bibliotecas de Google Cloud sepan dónde está el archivo de credenciales
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-file.json"

# Copiar el archivo de requerimientos y otros archivos de la aplicación
COPY requirements.txt requirements.txt
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelos de spaCy necesarios
RUN python -m spacy download en_core_web_sm

# Descargar paquetes necesarios de nltk
RUN python -m nltk.downloader punkt stopwords wordnet

# Exponer el puerto 8080
EXPOSE 8080

# Comando para ejecutar la aplicación Flask
CMD ["python", "run.py"]