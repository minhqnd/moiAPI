import requests
import time


def get_download_url(url, format):
    api_url = 'https://loader.to/ajax/download.php'
    headers = {
        'Accept': '*/*',
        'Origin': 'https://en.loader.to',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Host': 'loader.to',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
        'Referer': 'https://en.loader.to/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    api_url = f'{api_url}?url={url}&format={format}'
    response = requests.request("GET", api_url, headers=headers)
    json_data = response.text
    return json_data
    if json_data['success'] == True:
        id = json_data['id']
        download_url = follow_progress(id)
        return download_url
    else:
        return None


def follow_progress(id):
    api_url = 'https://loader.to/ajax/progress.php'
    headers = {
        'Accept': '*/*',
        'Origin': 'https://en.loader.to',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Host': 'loader.to',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
        'Referer': 'https://en.loader.to/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    api_url = f'{api_url}?id={id}'
    while True:
        response = requests.request("GET", api_url, headers=headers)
        json_data = response.json()
        if json_data['success'] == 1:
            download_url = json_data['download_url']
            return download_url
        else:
            time.sleep(1)  # đợi 5 giây trước khi gửi yêu cầu tiếp theo
            continue

# TODO làm hệ thông check id
