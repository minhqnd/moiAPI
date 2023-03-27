from duckduckgo_search import ddg
import json
import re
import requests
from bs4 import BeautifulSoup


def duck_search(search_term):
    url = ddg(search_term + ' site:moon.vn',
              safesearch='Off', max_results=1)[0]['href']
    return url


def answer(q):
    link = duck_search(q)
    json = get_ld_json(link)
    mapping = {char: result.group(1) for char in ['A', 'B', 'C', 'D'] if (
        result := re.search(f"{char}\.\s+(.*?)($|\n)", json, re.DOTALL))}
    mapping['D'] = re.sub(r'\.\s*\S*$', '.', mapping['D'])
    dapan = re.search(r'Đáp án   \s*([ABCD])', json).group(1)
    answer = mapping[dapan]
    question = re.search(".*(?=Đáp án)", json, re.DOTALL).group(0)
    question = question.replace('\n', '')
    explain = re.search("(?<=Đáp án).*", json,
                        re.DOTALL).group(0).replace('\n', '')
    if len(explain)>100:
        explain=''
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
    return answer


# print(answer("Cho hình lập phương ABCD.A'B'C'D' Đường thẳng AB vuông góc với đường thẳng nào dưới đây?"))
