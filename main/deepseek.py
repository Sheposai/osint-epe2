import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Carga .env desde la raíz
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
print("🔐 Clave cargada:", DEEPSEEK_API_KEY)

def analyze_osint(data):
    prompt = f"""
Eres un analista de ciberseguridad. Analiza el siguiente reporte OSINT con buenas prácticas (OWASP, NIST):

{data}

Proporciona recomendaciones técnicas claras para mitigar riesgos.
    """
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Eres un analista experto en ciberseguridad."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error en DeepSeek: {response.status_code} {response.text}"
