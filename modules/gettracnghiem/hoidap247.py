from duckduckgo_search import ddg
import json
import re
import requests
from bs4 import BeautifulSoup

def duck_search(search_term):
    url = ddg(search_term + ' site:hoc247.net',
              safesearch='Off', max_results=1)[0]['href']
    return url


def answer(q):
    link = duck_search(q)
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
