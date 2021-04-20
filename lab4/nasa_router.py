from fastapi import APIRouter
import requests
import json

router = APIRouter(prefix="/nasa")


@router.get("/planetary-news")
# date format: YYYY - MM - DD; api_key can be specified or not (-> then goes with the default one)
async def get_planetary_news(date: str, api_key: str = None):
    url = "https://api.nasa.gov/planetary/apod"
    if not api_key:
        file = open("config.json")
        string = file.read()
        decoded_string = json.loads(string)
        api_key = decoded_string["api_key"]

    request_dict = {"api_key": api_key, "date": date}

    response = requests.get(url, params=request_dict)
    print(response.json())

    return {
        "title": response.json()["title"],
        "Description": response.json()["explanation"],
    }


# GET api endpoint to retrieve the API key
@router.get("/api-key")
async def get_api_key():
    file = open("config.json")
    file_content = file.read()
    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]
    return api_key


# PUT api endpoint to modify the API key, will raise an exception if there is no API key
@router.put("/modify-api-key")
async def modify_api_key(new_key: str):
    file = open("config.json")
    file_content = file.read()
    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]

    if not api_key:
        raise Exception("No api key found in config.json")

    file.close()

    file = open("config.json", "w")
    data = {"api_key": new_key}
    json.dump(data, file)

    return "API key modified successfully!"


# DELETE api endpoint to remove the API key, the value becomes null in the json
@router.delete("/delete-api-key")
async def delete_api_key():
    file = open("config.json", "w")
    data = {"api_key": None}
    json.dump(data, file)

    return "API key deleted successfully!"


# POST api endpoint to add an API key, if there is already one it will raise an exception
@router.post("/add-api-key")
async def add_api_key(new_key: str):
    file = open("config.json")
    file_content = file.read()
    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]

    if api_key:
        raise Exception("There already exists an API key")

    file.close()

    file = open("config.json", "w")
    data = {"api_key": new_key}
    json.dump(data, file)

    return "API key added successfully!"
