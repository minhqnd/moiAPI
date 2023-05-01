import requests
import time
def get_download_url(url, format):
    api_url = 'https://loader.to/ajax/download.php'
    params = {'url': url, 'format': format}
    response = requests.get(api_url, params=params)
    json_data = response.json()
    if json_data['success'] == True:
        id = json_data['id']
        download_url = follow_progress(id)
        return download_url
    else:
        return None

def follow_progress(id):
    api_url = 'https://loader.to/ajax/progress.php'
    params = {'id': id}
    while True:
        response = requests.get(api_url, params=params)
        json_data = response.json()
        if json_data['success'] == 1:
            download_url = json_data['download_url']
            return download_url
        else:
            time.sleep(1) # đợi 5 giây trước khi gửi yêu cầu tiếp theo
            continue