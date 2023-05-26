
import requests #dependency

def send(id,token,data):
    url = f"https://discord.com/api/webhooks/{id}/{token}" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return err
    else:
        return "Payload delivered successfully, code {}.".format(result.status_code)
        
# https://discord.com/api/webhooks/1111519350424346624/GRQYnnHGp-XBvPndhf8F67D-tcO_1Xx6T-KdolpRd5VchPYDCz8HjyhoFeQs_trv59jz

# dete = {
#   "content": "<@&1036240075517857842>",
#   "embeds": [
#     {
#       "title": "🟢  SERVER STARTED",
#       "description": "Join with ip: sv.minhquang.xyz:7777\n<@&1036240075517857842>",
#       "color": 5814783,
#       "timestamp": "2023-05-26T06:59:00.000Z"
#     }
#   ],
#   "attachments": []
# }

# send(1111519350424346624,"GRQYnnHGp-XBvPndhf8F67D-tcO_1Xx6T-KdolpRd5VchPYDCz8HjyhoFeQs_trv59jz", dete)