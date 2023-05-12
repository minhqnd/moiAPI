from duckduckgo_search import ddg
import json
import requests
from bs4 import BeautifulSoup


def duck_search(search_term):
    """

    Searches for a given term on the website khoahoc.vietjack.com using DuckDuckGo search engine and returns the URL of the first search result.

    Args:
        search_term (str): The term to be searched on khoahoc.vietjack.com

    Returns:
        str: The URL of the first search result on khoahoc.vietjack.com

    Example:
        >>> duck_search('python')
        'https://khoahoc.vietjack.com/python/'

    """
    url = ddg(
        search_term + " site:khoahoc.vietjack.com", safesearch="Off", max_results=1
    )[0]["href"]
    return url


def getlink(q: str):
    """
    Returns the URL of the first search result on khoahoc.vietjack.com for a given search term.

    Args:
        q (str): The search term to be searched on khoahoc.vietjack.com

    Returns:
        str: The URL of the first search result on khoahoc.vietjack.com

    Example:
        >>> getlink('python')
        'https://khoahoc.vietjack.com/python/'
    """
    result = duck_search(q)
    return result


def answer(q):
    """
    Returns a dictionary containing the link, question, answer and explanation for a given search term.

    Args:
        q (str): The search term to be searched on khoahoc.vietjack.com

    Returns:
        dict: A dictionary containing the link, question, answer and explanation for the given search term.

    Example:
        >>> answer('python')
        {
            "link": "https://khoahoc.vietjack.com/python/",
            "question": "Tìm hiểu ngôn ngữ lập trình Python",
            "answer": "Python là một ngôn ngữ lập trình thông dịch, hướng đối tượng và được thiết kế để đơn giản hóa việc lập trình cho các nhà phát triển.",
            "explain": "Python là một ngôn ngữ lập trình thông dịch, hướng đối tượng và được thiết kế để đơn giản hóa việc lập trình cho các nhà phát triển. Python được tạo ra bởi Guido van Rossum và được phát hành lần đầu tiên vào năm 1991. Python được sử dụng rộng rãi trong các lĩnh vực như khoa học dữ liệu, trí tuệ nhân tạo, web development, game development, và nhiều lĩnh vực khác."
        }
    """
    link = duck_search(q)
    json = get_ld_json(link)
    question = json["mainEntity"]["text"]
    answer = json["mainEntity"]["acceptedAnswer"]["result"]
    explain = json["mainEntity"]["acceptedAnswer"]["text"]
    result = {"link": link, "question": question, "answer": answer, "explain": explain}
    return result


def get_ld_json(url: str) -> dict:
    """
    Parses the JSON-LD data from the given URL and returns it as a dictionary. If the search result has a correct answer, it replaces the answer in the JSON-LD data with the correct answer.

    Args:
        url (str): The URL to parse the JSON-LD data from.

    Returns:
        dict: A dictionary containing the parsed JSON-LD data from the given URL.

    Example:
        >>> get_ld_json('https://khoahoc.vietjack.com/python/')
        {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": "Tìm hiểu ngôn ngữ lập trình Python",
            "description": "Python là một ngôn ngữ lập trình thông dịch, hướng đối tượng và được thiết kế để đơn giản hóa việc lập trình cho các nhà phát triển.",
            "provider": {
                "@type": "Organization",
                "name": "VietJack"
            },
            "mainEntity": {
                "@type": "Question",
                "name": "Tìm hiểu ngôn ngữ lập trình Python",
                "text": "Python là gì?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Python là một ngôn ngữ lập trình thông dịch, hướng đối tượng và được thiết kế để đơn giản hóa việc lập trình cho các nhà phát triển.",
                    "result": "Python là một ngôn ngữ lập trình thông dịch, hướng đối tượng và được thiết kế để đơn giản hóa việc lập trình cho các nhà phát triển."
                }
            }
        }
    """
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    result = json.loads(
        "".join(soup.find_all("script", {"type": "application/ld+json"})[2].contents)
    )
    if soup.find("div", {"class": "answer-correct"}).text:
        answer = soup.find("div", {"class": "answer-correct"}).text
        dot_index = answer.find(".")
        correct_answer = answer[dot_index + 2 :].strip()
        correct_answer = correct_answer.replace("Đáp án chính xác", "")
        correct_answer = correct_answer.replace("\n", "")
        # print(correct_answer)
        result["mainEntity"]["acceptedAnswer"]["result"] = correct_answer
    return result

    # print(answer("Cho hình chóp S.ABCD có đáy hình vuông ABCD cạnh bằng a và các cạnh bên đều bằng a. Gọi M và N lần lượt là trung điểm của AD và SD. Số đo góc (MN,SC) bằng"))
