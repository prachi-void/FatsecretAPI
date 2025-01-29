from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from requests_oauthlib import OAuth2Session
import os
import requests

# FatSecret API credentials
CLIENT_ID = "eb086db6e0c84c2389ab2be189df77ee"
CLIENT_SECRET = "802968b455a4461aa61f9783197ac0d4"
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL = "https://platform.fatsecret.com/rest/server.api"

def get_access_token():
    """Obtain OAuth 2.0 access token from FatSecret API."""
    data = {
        "grant_type": "client_credentials",
        "scope": "basic",
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    response = requests.post(TOKEN_URL, data=data, auth=auth)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

def fetch_food_data(query: str, page: int = 0, max_results: int = 10):
    """Fetch food data from FatSecret API."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "method": "foods.search",
        "format": "json",
        "search_expression": query,
        "page_number": page,
        "max_results": max_results,
    }
    response = requests.get(API_URL, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch food data")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>FatSecret Food Search</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            .navbar { position: fixed; top: 0; width: 100%; background: #333; color: white; padding: 10px; }
            .footer { position: fixed; bottom: 0; width: 100%; background: #333; color: white; padding: 10px; }
            table { width: 80%; margin: 50px auto; border-collapse: collapse; }
            th, td { padding: 10px; border: 1px solid black; }
        </style>
    </head>
    <body>
        <div class="navbar">FatSecret Food Search</div>
        <h1>Search for Food</h1>
        <form action="/search" method="get">
            <input type="text" name="query" required>
            <input type="submit" value="Search">
        </form>
        <div class="footer">© 2024 Food Search App</div>
    </body>
    </html>
    """

@app.get("/search", response_class=HTMLResponse)
def search_food(query: str, page: int = 0, max_results: int = 10):
    data = fetch_food_data(query, page, max_results)
    print(data)  # Debugging output

    foods = data.get("foods", {}).get("food", [])
    print(foods)
    html = f"""
    <html>
    <head>
        <title>Search Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            .navbar {{ position: fixed; top: 0; width: 100%; background: #333; color: white; padding: 10px; }}
            .footer {{ position: fixed; bottom: 0; width: 100%; background: #333; color: white; padding: 10px; }}
            table {{ width: 80%; margin: 50px auto; border-collapse: collapse; }}
            th, td {{ padding: 10px; border: 1px solid black; }}
        </style>
    </head>
    <body>
        <div class="navbar">FatSecret Food Search</div>
                <table><h1>Search Results for '{query}'</h1>
            <tr>
                <th>Food Name</th>
                <th>Brand Name</th>
                <th>Food Type</th>
                <th>Food URL</th>
            </tr>
    """

    for food in foods:
        html += f"""
         
        <tr>

            <td>{food.get("food_name", "N/A")}</td>
            <td>{food.get("brand_name", "N/A")}</td>
            <td>{food.get("food_type", "N/A")}</td>
            <td><a href='{food.get("food_url", "#")}' target='_blank'>View</a></td>
        </tr>
        """
    html += f"""
        </table>
        <div class="pagination">
    """
    if page > 0:
        html += f"""<a href="/search?query={query}&page={page-1}&max_results={max_results}">Previous Page</a> """
    html += f"""
        </table>
        <br>
        <a href="/search?query={query}&page={page+1}&max_results={max_results}">Next Page</a>
        <div class="footer">© 2024 Food Search App</div>
    </body>
    </html>
    """

    return html