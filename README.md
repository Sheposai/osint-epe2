# 🛡️ Proyecto EPE2 - Análisis OSINT Automatizado con IA Generativa

Este proyecto implementa una API REST con Django que automatiza el análisis de datos OSINT mediante la inteligencia artificial generativa DeepSeek. Está diseñado para apoyar procesos de evaluación de seguridad informática en organizaciones de cualquier rubro.

---

## 🚀 Funcionalidad

- ✅ API: `POST /deepseek/`
- ✅ Entrada: JSON con dominio, puertos y datos WHOIS
- ✅ Salida: Respuesta generada por IA con recomendaciones técnicas de ciberseguridad
- ✅ Conexión con la API oficial de [DeepSeek](https://platform.deepseek.com)
- ✅ Despliegue con Docker y Docker Compose

---

## 🧪 Ejemplos de uso

### 🔹 Request (JSON):
```json
{
  "domain": "acme-corp.com",
  "ports": [80, 443],
  "whois": "Registrar: GoDaddy\nExpiración: 2030\nContacto: IT Dept"
}
