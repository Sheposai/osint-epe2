import os
from dotenv import load_dotenv

load_dotenv()  # intenta cargar el .env desde la raíz

print("✅ Clave detectada:", os.getenv("DEEPSEEK_API_KEY"))
