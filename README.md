### FastAPI GeoLocation Service
This service is a simple IP geolocation API built using FastAPI and MaxMind's GeoIP2 database.

### Getting Started
#### Prerequisites
To run this project, you will need:

* Python 3.7 or higher
* FastAPI
* uvicorn (to serve the API)
* geoip2
These can be installed with pip:

```bash
pip install fastapi uvicorn geoip2
```
You will also need to download the GeoLite2 Country database in MMDB format from MaxMind's website. After downloading and extracting the database, put the .mmdb file in the same directory as your FastAPI application.

### Running the API
To start the FastAPI application, use uvicorn:

```bash
uvicorn main:app --reload
```
### API Endpoints
***GET /location/{ip}**: Returns the country code for the given IP address. If the IP address is not found in the database, a 404 error will be returned.

***GET /location/**: Returns the country code for the IP address of the request. If the IP address is not found in the database, a 404 error will be returned.

### Caching
The API uses Python's built-in functools.lru_cache for caching. This means that if an IP address's geolocation information has been requested before, it will be retrieved from cache, which is significantly faster than querying the database.

### License
#### MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this code and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
