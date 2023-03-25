from googlesearch import search
import json
import re
import requests
from bs4 import BeautifulSoup

def google_search(search_term):
    for url in search(search_term + ' site:hoc247.net/cau-hoi-*', num_results=1):
        return url


def getlink(q: str):
    result = google_search(q)
    return result


def answer(q):
    link = getlink(q)
    print(link)
    json = get_ld_json(link)
    mapping = {char: result.group(1) for char in ['A', 'B', 'C', 'D'] if (
        result := re.search(f"{char}\.\n(.*?)\n+", json, re.DOTALL))}
    dapan = re.search(r'Đáp án đúng:\s*([ABCD])', json)
    answer = mapping[dapan.group(1)]
    question = re.search(".*(?=Lời giải tham khảo:)", json, re.DOTALL).group(0)
    question = question.replace('\n', '')
    explain = re.search("(?<=Lời giải tham khảo:).*", json,
                        re.DOTALL).group(0).replace('\n', '')
    explain = explain.replace('ADSENSE','')
    output = {
        "link": link,
        "question": question,
        "answer": answer,
        "explain": explain
    }
    return output


def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    answer = soup.find('div', {'id': 'cauhoi'}).text
    return answer


print(answer("Di chuyển một điện tích q từ điểm M đến điểm N trong một điện trường. Công AMN của lực điện sẽ càng lớn nếu"))
