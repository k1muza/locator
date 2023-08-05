import os
from fastapi import HTTPException, Request
import requests


TOKEN = os.getenv('IPAPI_TOKEN')
FALLBACK_ENABLED = os.getenv('FALL_BACK_ENABLED', False)


def get_ip_from_request(request: Request):
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip:
        ip = client_ip.split(",")[0]  # the header can contain multiple IP addresses, we take the first one
    else:
        ip = request.client.host  # fallback to the immediate client IP
    return ip


def get_location_from_api(ip_address: str):
    if not FALLBACK_ENABLED:
        raise HTTPException(status_code=404, detail="IP address not found")
    
    try:
        res = requests.get(f'http://api.ipapi.com/api/{ip_address}?access_key=${TOKEN}')
        return res.json().get('country_code')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
