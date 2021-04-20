import requests
import json
import pprint

url = "https://api.nasa.gov/planetary/apod"

config_file = open("config.json")

config_json = config_file.read()

config_decoded = json.loads(config_json)

api_key = config_decoded["api_key"]

config_decoded["date"] = "2019-05-09"

response = requests.get(url, params=config_decoded)

response_json = response.json()

pprint.pprint(response_json["title"])
