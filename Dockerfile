# Imagen base de Python optimizada
FROM python:3.10-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de desarrollo de Django
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
