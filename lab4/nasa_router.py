from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import json

router = APIRouter(prefix="/nasa")


@router.get("/planetary-news")
# date format: YYYY - MM - DD; api_key can be specified or not (-> then goes with the default one)
async def get_planetary_news(date: str, api_key: str = None):
    url = "https://api.nasa.gov/planetary/apod"
    if not api_key:
        # opening the file, verifying that it exists
        try:
            with open("config.json") as f:
                file_content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("config.json not found!")

        # decoding the json, making sure the config.json content is an actual json
        try:
            decoded_string = json.loads(file_content)
        except ValueError as exc:
            return JSONResponse(status_code=404, content=str(exc))

        api_key = decoded_string["api_key"]

        # making sure there is an api key so that we can access the api
        if not api_key:
            raise Exception("There is no api key in config.json")

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
    try:
        with open("config.json") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found!")

    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]

    if not api_key:
        raise Exception("There is no api key in config.json")

    return api_key


# PUT api endpoint to modify the API key, will raise an exception if there is no API key
@router.put("/api-key")
async def modify_api_key(new_key: str):
    try:
        with open("config.json") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found!")

    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]

    if not api_key:
        raise Exception("No api key found in config.json")

    file = open("config.json", "w")
    data = {"api_key": new_key}
    json.dump(data, file)

    return "API key modified successfully!"


# DELETE api endpoint to remove the API key, the value becomes null in the json
@router.delete("/api-key")
async def delete_api_key():
    try:
        with open("config.json") as file:
            data = {"api_key": None}
            json.dump(data, file)
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found!")

    return "API key deleted successfully!"


# POST api endpoint to add an API key, if there is already one it will raise an exception
@router.post("/api-key")
async def add_api_key(new_key: str):
    try:
        with open("config.json") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found!")

    decoded_content = json.loads(file_content)
    api_key = decoded_content["api_key"]

    if api_key:
        raise Exception("There already exists an API key")

    file = open("config.json", "w")
    data = {"api_key": new_key}
    json.dump(data, file)

    return "API key added successfully!"

