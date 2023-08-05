from functools import lru_cache
from fastapi import FastAPI, HTTPException, Request
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

app = FastAPI()

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
        raise HTTPException(status_code=404, detail="IP address not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@app.get("/location/{ip}")
def get_ip_location(ip: str):
    return {"countryCode": get_country_code(ip)}

@app.get("/location/")
def get_location(request: Request):
    ip = request.client.host
    return {"countryCode": get_country_code(ip)}
