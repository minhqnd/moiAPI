from . import hoidap247
from . import moon
from . import vietjack


# def dapan(q):
#     output = {}
#     output["hoidap247"] = duck_search(q)
#     return output

# def hello():
#     return 'hellloooo'

# from duckduckgo_search import ddg


def dapan(q):
    output = {}
    try:
        output["hoidap247"] = hoidap247.answer(q)
    except Exception as e:
        output["hoidap247"] = {
            "link": '',
            "question": '',
            "answer": '',
            "explain": ''
        }

    try:
        output["moon"] = moon.answer(q)
    except Exception as e:
        output["moon"] = {
            "link": '',
            "question": '',
            "answer": '',
            "explain": ''
        }

    try:
        output["vietjack"] = vietjack.answer(q)
    except Exception as e:
        output["vietjack"] = {
            "link": '',
            "question": '',
            "answer": '',
            "explain": ''
        }

    return output
