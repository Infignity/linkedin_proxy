from fastapi import FastAPI, Response, status
from curl_cffi import requests

from utils import headers, cookies
from linkedin import format_profile, format_company

app = FastAPI()

@app.get("/profile")
def linkedin(username: str, resp: Response):
    "Return formated profile data of username."
    url = f"https://www.linkedin.com/voyager/api/identity/profiles/{username}/profileView"
    res = requests.get(url, headers=headers, cookies=cookies, timeout=200, impersonate="chrome110")
    if res.status_code != 200:
        resp.status_code = res.status_code
        return {'text': res.text}
    
    formatted_profile = format_profile(res.json()['included'])
    return {'text': formatted_profile}

@app.get("/company")
def company(universal_name: str, resp: Response):
    "Return formatted company profile of id."
    params = {
        "decorationId": "com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-12",
        "q": "universalName",
        "universalName": universal_name,
    }
    url = "https://www.linkedin.com/voyager/api/organization/companies"
    res = requests.get(url, params=params, headers=headers, cookies=cookies, impersonate="chrome110")

    if res.status_code != 200:
        resp.status_code = res.status_code
        return {'text': res.text}
    
    formatted_about = format_company(res.json()['included'], universal_name)
    return {'text': formatted_about}