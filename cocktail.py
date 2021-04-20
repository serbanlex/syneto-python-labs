import requests

url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"

fetched = requests.get(url, params={"s": "margarita"})

json_response = fetched.json()

cocktail = json_response["drinks"][0]

for key, value in cocktail.items():
    if ("strIngredient" in key) and value:
        print(value)
