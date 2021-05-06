import click
import requests


@click.command()
@click.option('--data', default=None, help='Seeing stuff from one date')
@click.option('--title', is_flag=True, help='If you wanna only see the title, from the known date')
def call_nasa_api(data, title):
    url = "https://api.nasa.gov/planetary/apod"
    api_key = "7jPB6D3v9ACZEkVuPv0iMge0i15WlZGhLoff1Key"
    if data:
        request_dict = {"api_key": api_key, "date": data}
    else:
        request_dict = {"api_key": api_key}

    response = requests.get(url, params=request_dict)
    if title:
        click.echo(response.json()["title"])
    else:
        click.echo(response.json())


@click.option('--api_key', help='API key')
def add_API_key(api_key: str):
    requests.post(url="http://127.0.0.1:8000/nasa/api-key", params={"api_key": api_key})


if __name__ == '__main__':
    # call_nasa_api()
    add_API_key("lmao")
