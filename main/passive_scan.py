import socket
import requests
import whois

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        return f"Error: {e}"

def get_http_headers(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return dict(response.headers)
    except Exception as e:
        return {"error": str(e)}

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": str(w.domain_name),
            "registrar": str(w.registrar),
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "emails": str(w.emails),
            "name_servers": w.name_servers,
        }
    except Exception as e:
        return {"error": str(e)}

def get_ip_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def passive_osint(domain):
    ip = get_ip(domain)
    headers = get_http_headers(domain)
    whois_info = get_whois_info(domain)
    geo = get_ip_geolocation(ip if isinstance(ip, str) else "")

    return {
        "ip": ip,
        "http_headers": headers,
        "whois_info": whois_info,
        "ip_geolocation": geo
    }
