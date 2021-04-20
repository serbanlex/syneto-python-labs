from fastapi import APIRouter
import requests
import json

router = APIRouter(prefix="/nasa")


@router.get("/planetary-news")
async def get_planetary_news(date: str, api_key: str = None):
    url = "https://api.nasa.gov/planetary/apod"
    if not api_key:
        file = open("config.json")
        string = file.read()
        decoded_string = json.loads(string)
        api_key = decoded_string["api_key"]

    dict = {"api_key": api_key, "date": date}

    response = requests.get(url, params=dict)
    print(response.json())

    return {
        "title": response.json()["title"],
        "Description": response.json()["explanation"],
    }
