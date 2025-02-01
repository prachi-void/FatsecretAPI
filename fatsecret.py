from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import requests
import base64

app = FastAPI()

# Mount static files (for CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# FatSecret API credentials
CLIENT_ID = "eb086db6e0c84c2389ab2be189df77ee"
CLIENT_SECRET = "802968b455a4461aa61f9783197ac0d4"
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL = "https://platform.fatsecret.com/doc/foods/search/v3"

# Function to get OAuth 2.0 access token
def get_access_token():
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "grant_type": "client_credentials",
        "scope": "basic",
    }
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")
    
    return response.json().get("access_token")

# Function to fetch food data from FatSecret API
def fetch_food_data(search_expression: str, page_number: int = 0, max_results: int = 10):
    access_token = get_access_token()
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "search_expression": search_expression,
        "page_number": page_number,
        "max_results": max_results,
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch food data")
    
    return response.json()

# Home route with search functionality
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, search: Optional[str] = None, page: int = 0):
    max_results = 10  # Results per page
    if search:
        data = fetch_food_data(search, page_number=page, max_results=max_results)
        foods = data.get("foods", {}).get("food", [])
        total_results = data.get("foods", {}).get("total_results", 0)
    else:
        foods = []
        total_results = 0

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "foods": foods,
            "search": search,
            "page": page,
            "total_results": total_results,
            "max_results": max_results,
        },
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
