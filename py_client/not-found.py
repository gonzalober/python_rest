import requests

endpoint = "http://localhost:8000/api/products/128097103093432/"

get_response = requests.get(endpoint)
print(get_response.json())
