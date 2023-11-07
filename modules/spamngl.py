import requests, urllib.parse, uuid

def spamngl(username, question):
    deviceId = uuid.uuid4()
    print(deviceId)
    url = "https://ngl.link/api/submit"
    payload = "username="+username+"&question="+urllib.parse.quote(question)+"&deviceId="+str(deviceId)+"&gameSlug=&referrer="
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Host': 'ngl.link',
    'Origin': 'https://ngl.link',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code