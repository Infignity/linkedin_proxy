from fastapi import FastAPI, Response, status
from curl_cffi import requests

from utils import headers, cookies
from linkedin import format_profile

app = FastAPI()

@app.get("/profile")
def linkedin(username: str, resp: Response):
    "Return formated linkedin profile data of username."
    url = f"https://www.linkedin.com/voyager/api/identity/profiles/{username}/profileView"
    res = requests.get(url, headers=headers, cookies=cookies, impersonate="chrome110")
    if res.status_code != 200:
        resp.status_code = res.status_code
        return {'text': res.text}
    
    formatted_profile = format_profile(res.json()['included'])
    return {'text': formatted_profile}

@app.get("/company")
def company(id: str, resp: Response):
    "Return formatted linkedin company profile of id."
    pass