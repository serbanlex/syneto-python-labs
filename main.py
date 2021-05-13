# docker build . -t aclabs
# docker run -td --name syneto-lab -v "D:\Diverse\3. Syneto\git\syneto-python-labs":/home/syneto_labs/ -p 8000:8000 aclabs
# docker run -td --name syneto-lab -v "C:\Users\alexandru-b.serban\PycharmProjects\syneto-python-labs":/home/syneto_labs -p 8000:8000 aclabs
# docker exec -it syneto-lab /bin/bash
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
