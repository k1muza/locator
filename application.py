from functools import lru_cache
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

from utils.methods import get_location_from_api, get_ip_from_request

app = FastAPI()

origins = [
    os.getenv('TEST_URL'),
    os.getenv('LIVE_URL'),  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

reader = None  # Will hold our MaxMind DB reader

@app.on_event("startup")
def startup_event():
    global reader
    reader = Reader('ip_database.mmdb')

@app.on_event("shutdown")
def shutdown_event():
    global reader
    if reader is not None:
        reader.close()

@lru_cache(maxsize=1024)
def get_country_code(ip_address: str):
    try:
        # Use the reader to get the country information for the IP address
        response = reader.country(ip_address)
        country_code = response.country.iso_code
        return country_code
    except AddressNotFoundError:
        return get_location_from_api(ip_address)
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@app.get("/location/{ip}")
def get_ip_location(ip: str):
    return {"countryCode": get_country_code(ip)}

@app.get("/location/")
def get_location(request: Request):
    client_ip = get_ip_from_request(request)
    return {"countryCode": get_country_code(client_ip)}

@app.get("/ip/")
def get_location(request: Request):
    client_ip = get_ip_from_request(request)
    return {"ipAddress": client_ip}
