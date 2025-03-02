import requests

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Example query to find businesses (e.g., restaurants, grocery stores)
overpass_query = """
[out:json];
area[name="Louisiana"];  
(
  node[name="Waffle House"](area);
  way["restaurant"](area);
  relation["restaurant"](area);
);
out body;
"""

# Make the request
response = requests.get(overpass_url, params={'data': overpass_query})

# Check the response
if response.status_code == 200:
    data = response.json()
    print("data: ")
    print(data)  # Process the results
else:
    print(f"Error: {response.status_code}")