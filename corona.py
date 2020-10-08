import requests
import json

def stateRequest(state):
    url = f"https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/{state.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return "" 
    else:
        response = json.loads(response.content)
        cases = response["cases"]
        state = response["state"]
        return f"<i>Atualmente, {state} tem um total de {cases} casos de corona :(</i>"