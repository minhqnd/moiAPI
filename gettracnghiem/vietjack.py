from duckduckgo_search import ddg
import json
import requests
from bs4 import BeautifulSoup

def duck_search(search_term):
    url = ddg(search_term + ' site:khoahoc.vietjack.com', safesearch='Off', max_results=1)[0]['href']
    return url


def getlink(q: str):
    result = duck_search(q)
    return result


def answer(q):
    link = duck_search(q)
    json = get_ld_json(link)
    question = json['mainEntity']['text']
    answer = json['mainEntity']['acceptedAnswer']['result']
    explain = json['mainEntity']['acceptedAnswer']['text']
    result = {
        "link": link,
        "question": question,
        "answer": answer,
        "explain": explain
    }
    return result


def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    result = json.loads("".join(soup.find_all(
        "script", {"type": "application/ld+json"})[2].contents))
    if (soup.find('div', {'class': 'answer-correct'}).text):
        answer = soup.find('div', {'class': 'answer-correct'}).text
        dot_index = answer.find(".")
        correct_answer = answer[dot_index+2:].strip()
        correct_answer = correct_answer.replace("Đáp án chính xác", "")
        correct_answer = correct_answer.replace("\n", "")
        # print(correct_answer)
        result['mainEntity']['acceptedAnswer']['result'] = correct_answer
    return result


# print(answer("Cho hình chóp S.ABCD có đáy hình vuông ABCD cạnh bằng a và các cạnh bên đều bằng a. Gọi M và N lần lượt là trung điểm của AD và SD. Số đo góc (MN,SC) bằng"))
