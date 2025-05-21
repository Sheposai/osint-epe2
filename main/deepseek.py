import requests
import os
import json
import re
from dotenv import load_dotenv
from pathlib import Path

# Carga .env desde la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
print("🔐 Clave cargada:", DEEPSEEK_API_KEY)

def analyze_osint(data):
    prompt = f"""
Eres un analista experto en ciberseguridad. Analiza el siguiente informe OSINT y responde exclusivamente en formato JSON estructurado con los siguientes campos:

- hallazgos
- recomendaciones
- normativas
- resumen

Solo entrega JSON. Nada más.

{data}
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
                {"role": "system", "content": "Eres un experto en análisis OSINT."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code == 200:
        try:
            content = response.json()["choices"][0]["message"]["content"]

            # 🧼 Limpiar markdown ```json ... ```
            match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
            if match:
                cleaned = match.group(1)
            else:
                cleaned = content.strip()

            return json.loads(cleaned)

        except Exception as e:
            return {
                "error": "La IA no devolvió un JSON válido",
                "respuesta_original": content,
                "detalles": str(e)
            }

    return {
        "error": f"Error en DeepSeek: {response.status_code}",
        "respuesta": response.text
    }
