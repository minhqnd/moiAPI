from unidecode import unidecode

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
}


def encode(text):
    """

    Encodes the given text into Morse code.

    Args:
        text (str): The text to be encoded.

    Returns:
        str: The encoded Morse code.


    """
    text = unidecode(text)
    morse_code = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        else:
            morse_code.append(" ")
    return " ".join(morse_code)


def decode(morse_code):
    """
    Decodes the given Morse code into text.

    Args:
        morse_code (str): The Morse code to be decoded.

    Returns:
        str: The decoded text.
    """
    inverted_dict = {value: key for key, value in MORSE_CODE_DICT.items()}
    decoded_text = []
    morse_code = morse_code.replace("   ", " _ ")
    for code in morse_code.split():
        if code in inverted_dict:
            decoded_text.append(inverted_dict[code])
        else:
            decoded_text.append(" ")
    return "".join(decoded_text)
