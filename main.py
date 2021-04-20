# docker build . -t aclabs
# docker run -td --name syneto-lab5 -v "D:\Diverse\3. Syneto\time-machine2":/home/syneto_labs/ aclabs
# docker exec -it syneto-lab5 /bin/sh
# /root/.poetry/bin/poetry shell
# /home/syneto_labs/lab4 # uvicorn fastAPI:app --host 0 --reload

import requests
import json

link = "https://www.boredapi.com/api/activity"

response = requests.get(link)

print(response)

json_response = response.json()


another_json = json.dumps(json_response)
parsed_json = json.loads(another_json)

print(parsed_json)

print(parsed_json["activity"])
