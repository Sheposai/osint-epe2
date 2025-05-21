import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINTBot/1.0; +https://example.com/bot)"
}

# Lista de dorks comunes que puedes expandir
DEFAULT_DORKS = [
    'inurl:admin',
    'intitle:"index of"',
    'filetype:pdf',
    'site:{domain} ext:sql | ext:conf | ext:log',
    'site:{domain} intext:"password"',
]

def search_dorks(domain, max_results=3):
    results = []
    for pattern in DEFAULT_DORKS:
        query = pattern.format(domain=domain)
        url = f"https://www.google.com/search?q=site:{domain}+{query}"

        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select("a")
            urls = set()

            for link in links:
                href = link.get("href")
                if href and "url?q=" in href:
                    real_url = href.split("url?q=")[1].split("&")[0]
                    urls.add(real_url)

            results.append({
                "dork": query,
                "matches": list(urls)[:max_results]
            })

            time.sleep(2)  # Evitar bloqueo de Google

        except Exception as e:
            results.append({
                "dork": query,
                "error": str(e)
            })

    return results
