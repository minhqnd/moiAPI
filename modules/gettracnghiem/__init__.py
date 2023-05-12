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
    """

    This function takes a question as input and returns a dictionary containing answers from three different sources: hoidap247, moon, and vietjack. If any of the sources fail to provide an answer, the corresponding dictionary value will contain empty strings. The dictionary keys are the names of the sources.

    """
    output = {}
    try:
        output["hoidap247"] = hoidap247.answer(q)
    except Exception:
        output["hoidap247"] = {"link": "", "question": "", "answer": "", "explain": ""}

    try:
        output["moon"] = moon.answer(q)
    except Exception:
        output["moon"] = {"link": "", "question": "", "answer": "", "explain": ""}

    try:
        output["vietjack"] = vietjack.answer(q)
    except Exception:
        output["vietjack"] = {"link": "", "question": "", "answer": "", "explain": ""}

    return output
