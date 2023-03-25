from googlesearch import search
import json
import re
import requests
from bs4 import BeautifulSoup

def google_search(search_term):
    for url in search(search_term + ' site:moon.vn/*', num_results=1):
        return url


def getlink(q: str):
    result = google_search(q)
    print(result)
    return result


def answer(q):
    link = getlink(q)
    print(link)
    json = get_ld_json(link)
    # print(json)
    mapping = {char: result.group(1) for char in ['A', 'B', 'C', 'D'] if (
        result := re.search(f"{char}\.\s+(.*?)($|\n)", json, re.DOTALL))}
    mapping['D']=re.sub(r'\.\s*\S*$', '.', mapping['D'])
    print(mapping)
    dapan = re.search(r'Đáp án   \s*([ABCD])', json).group(1)
    # print(mapping)
    answer = mapping[dapan]
    print(answer)
    question = re.search(".*(?=Lời giải tham khảo:)", json, re.DOTALL).group(0)
    question = question.replace('\n', '')
    explain = re.search("(?<=Lời giải tham khảo:).*", json,
                        re.DOTALL).group(0).replace('\n', '')
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
    answer = soup.find('div', {'class': 'card'}).text
    print(answer)
    return answer


print(answer("Công của lực điện trường khi một điện tích di chuyển từ điểm M đến điểm N trong điện trường đều là A = |q|Ed. Trong đó d là"))
