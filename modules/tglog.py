import requests,json

def send(text):
  url = "https://api.telegram.org/bot6660710160:AAEOulo2iv4liwZGc21vtLRwfpeGWetfEwM/sendMessage"

  payload = json.dumps({
    "chat_id": "2110348005",
    "text": text,
    "disable_notification": True
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return response.status_code


