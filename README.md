<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
</head>
<body>

<h1>FatSecret Food Search App</h1>

<p>
    The FatSecret Food Search App is a web application built using FastAPI that allows users to search for food items using the FatSecret API. 
    Users can enter a search query to find detailed information about various food products, including their names, brands, types, and links to more information.
</p>

<h2>Features</h2>
<ul>
    <li>Search for food items by name.</li>
    <li>View detailed information about each food item, including brand and type.</li>
    <li>Navigate through search results with pagination.</li>
</ul>

<h2>Prerequisites</h2>
<ul>
    <li>Python 3.7 or higher</li>
    <li>FastAPI</li>
    <li>Requests</li>
    <li>Requests-OAuthlib</li>
</ul>

<h2>Installation</h2>
<pre>
Clone the repository:
<code>git clone &lt;repository-url&gt;</code>
<code>cd fatsecret-food-search</code>

Create a virtual environment (optional but recommended):
<code>python -m venv venv</code>
<code>source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code>

Install the required packages:
<code>pip install fastapi requests requests-oauthlib</code>
</pre>

<h2>Configuration</h2>
<p>
    Before running the application, you need to set your FatSecret API credentials:
</p>
<pre>
Replace <code>CLIENT_ID</code> and <code>CLIENT_SECRET</code> in the code with your FatSecret API credentials.
<code>CLIENT_ID = "your_client_id"</code>
<code>CLIENT_SECRET = "your_client_secret"</code>
</pre>

<h2>Running the Application</h2>
<p>
    To run the FastAPI application, execute the following command:
</p>
<pre>
<code>uvicorn fatsecret:app --reload</code>
</pre>
<p>
    Open your browser and navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> to access the home page.
</p>

<h2>API Endpoints</h2>
<ul>
    <li><code>GET /</code>: Home page with a search form.</li>
    <li>
        <code>GET /search</code>: Endpoint for searching food items. Accepts the following query parameters:
        <ul>
            <li><code>query</code>: The search term for food items (required).</li>
            <li><code>page</code>: The page number for pagination (optional, default is 0).</li>
            <li><code>max_results</code>: The maximum number of results per page (optional, default is 10).</li>
        </ul>
    </li>
</ul>

<h2>Example Usage</h2>
<ol>
    <li>Enter a food item name in the search form on the home page.</li>
    <li>Click the "Search" button to view the results.</li>
    <li>Use the pagination links to navigate through multiple pages of results.</li>
</ol>

<h2>License</h2>
<p>
    This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.
</p>

</body>
</html>
