# Imagen base: Python 3.11 slim
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copia solo el requirements.txt de src/ primero (para optimizar cache de Docker)
COPY src/requirements.txt .

# Instala las dependencias usando el de src/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del contenido de src/ (app.py, scaler.pkl, model.pkl, imágenes, etc.)
COPY src/ .

# Expone el puerto de Streamlit
EXPOSE 8501

# Comando para correr la app (app.py ahora en /app/app.py)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]