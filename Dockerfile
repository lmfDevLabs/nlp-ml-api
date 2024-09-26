# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY nlp_processor.py nlp_processor.py
COPY path/to/your/service-account-file.json /app/service-account-file.json

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelos de spaCy
RUN python -m spacy download en_core_web_sm

# Descargar nltk paquetes 
RUN python scripts/download_nltk_data.py

# Exponer el puerto de la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]