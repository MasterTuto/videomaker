import re
from typing import Callable

from PIL import ImageFont
import utilities.config.text as text_config
from utilities.types.languages import SupportedLanguages
from bs4 import BeautifulSoup
from markdown import markdown

def get_char_width(font, char):
    return font.getsize(char)[0] if hasattr(font, 'getsize') else font.getbbox(char)[3]

def calculate_word_length(text: str, font_path: str, font_size: int):
    # Create a font object
    font = ImageFont.truetype(font_path, font_size)

    # Set an initial line width and character count
    line_width = 0
    for char in text:
        # Calculate the width of the character
        char_width = get_char_width(font, char)

        # Add the character width to the line width
        line_width += char_width

    return line_width

def split_word_to_max_width(word: str, font_path: str, font_size: int, max_width: float):
    # Create a font object
    font = ImageFont.truetype(font_path, font_size)

    current_part: str = ''
    parts: list[str] = []

    # Set an initial line width and character count
    line_width = 0
    for char in word:
        # Calculate the width of the character
        char_width = get_char_width(font, char)
            

        # If the line width exceeds the maximum width, break the loop
        if line_width + char_width > max_width:
            parts.append(current_part)
            current_part = ''
            line_width = 0

        # Add the character width to the line width
        current_part += char
        line_width += char_width

    if current_part:
        parts.append(current_part)


    return '\n'.join(parts)

def auto_line_break(text, video_width):
    max_length = video_width * 0.8
    current_line: list[str] = []
    current_line_width: int = 0
    lines: list[str] = []

    words = text.split(" ")

    for word in words:
        length_in_pixels = calculate_word_length(word, text_config.FONT, text_config.FONT_SIZE)

        if current_line_width + length_in_pixels > max_length:
            if current_line_width:
                full_line = ' '.join(current_line)
                lines.append(full_line + " ")
            else:
                splitted_word = split_word_to_max_width(word, text_config.FONT, text_config.FONT_SIZE, video_width * 0.8)
                lines.append(splitted_word)
                continue

            current_line_width = 0
            current_line = []
            max_length = video_width * 0.8

        current_line.append(word)
        current_line_width += length_in_pixels
        max_length -= length_in_pixels

    if current_line:
        full_line = ' '.join(current_line)
        lines.append(full_line + " ")

    new_lines = [f'{lines[x]}\n{lines[y]}' for x,y in zip(range(0, len(lines), 2), range(1, len(lines), 2))]
    if(len(lines) % 2 == 1): new_lines.append(lines[-1])

    return new_lines

def remove_abbreviation(text: str, lang: SupportedLanguages):
    abbreviations: dict[SupportedLanguages, dict[str, str]] = {
        'en-us': {
            'BYOB': 'bring your own beer',
            'DOA': 'dead on arrival',
            'DOB': 'date of birth',
            'AD': 'Anno Domini',
            'BC': 'Before Christ',
            'CE': 'Common Era',
            'BCE': 'Before Common Era',
            'AKA': 'also known as',
            'ASAP': 'as soon as possible',
            'AWOL': 'absent without leave',
            'BO': 'body odour',
            'BRB': 'be right back',
            'BTW': 'by the way',
            'DIY': 'do-it-yourself',
            'EFL': 'English as a Foreign Language',
            'ELT': 'English Language Teaching',
            'ESL': 'English as a Second Language',
            'BA': 'Bachelor of Arts',
            'MA': 'Master of Arts',
            'BSC': 'Bachelor of Science',
            'MSC': 'Master of Science',
            'PhD': 'Doctor of Philosophy',
            'CC': 'carbon copy',
            'BCC': 'blind carbon copy',
            'ETA': 'estimated time of arrival',
            'FAQ': 'frequently asked questions',
            'FYI': 'for your information',
            'IMO': 'in my opinion',
            'IMHO': 'in my humble opinion',
            'BLT': 'bacon, lettuce, and tomato',
            'EDM': 'electronic dance music',
            'LOL': 'laugh(ing) out loud',
            'NEET': 'not in education, employment, or training',
            'OMG': 'oh my god',
            'PTO': 'please turn over',
            'RIP': 'rest in peace',
            'TBA': 'to be announced',
            'TBC': 'to be confirmed',
            'VIP': 'very important person',
            'TGIF': 'thank god it\'s Friday',
            'YOLO': 'you only live once',
            'FOMO': 'fear of missing out',
            'TL;DR': 'too long; didn\'t read',
            'AFAIK': 'As Far As I Know',
            'AMA': 'Ask Me Anything',
            'CMV': 'Change My View',
            'DAE': 'Does Anyone Else',
            'ELI5': 'Explain Like I\'m 5 (years old)',
            'FTFY': 'Fixed That For You',
            'IAMA': 'I Am A',
            'IANAD': 'I Am Not A Doctor',
            'IANAL': 'I Am Not A Lawyer',
            'IIRC': 'If I Recall Correctly',
            'IMO': 'In My Opinion',
            'IMHO': 'In My Honest Opinion',
            'ITT': 'In This Thread',
            'MRW': 'My Reaction When',
            'MFW': 'My Face When',
            'NSFL': 'Not Safe For Life',
            'NSFW': 'Not Safe For Work',
            'OP': 'Original Poster',
            'PSA': 'Public Service Announcement',
            'TIL': 'Today I Learned',
            'YSK': 'You Should Know'
        },
        'pt-br': {
            'ASAP': 'O mais rápido possível',
            "AJD": "ajuda",
            "ATT": "ah tá",
            "BLZ": "beleza",
            "GNT": "gente",
            "MN": "mano",
            "PDC": "pode crer",
            "PLMDDS": "Pelo amor de Deus",
            "TM": "estamos",
            "MDDC": "meu deus do céu",
            "MLR": "melhor",
            "NGC": "negócio",
            "PV": "privado",
            "PLMNS": "pelo menos",
            "SDDS": "saudades",
            "SQN": "só que não",
            "SLK": "cê é louco",
            "TLGD": "Tá ligado",
            "TB": "também",
            "OQ": "o que",
            "HJ": "hoje",
            "VDD": "verdade",
            "VC": "você",
            "FZR": "fazer",
            "DPS": "depois",
            "FT": "foto",
            "FML": "família",
            "RLX": "relaxa",
            "FUT": "futebol",
            "BJ": "beijo",
            "PLS": "please",
            "OBG": "obrigada",
            "PQ": "porque",
            "VLW": "valeu",
            "HRS": "horas",
            "ND": "nada",
            "PFV": "por favor",
            "MSM": "mesmo",
            "MSG": "mensagem",
            "ADD": "adicionar",
            "AMG": "amigo",
            "CMG": "comigo",
            "GLR": "galera",
            "PPRT": "Papo reto",
            "CVS": "conversar",
            "SS": "sim",
            "QT": "quanto",
            "NN": "não",
            "CLR": "celular",
            "SLA": "Sei lá",
            "QRIA": "queria",
            "QSER": "quiser",
            "PFT": "perfeito",
            "DNV": "de novo",
            "SM": "sem",
            "CM": "com",
            "VMS": "vamos",
            "FLW": "falou",
            "TRD": "tarde",
            "AQ": "aqui",
            "BNT": "bonito",
            "NGM": "ninguém",
            'LOL': 'Rindo Alto',
            'BJS': 'Beijos',
            'AFF': 'Ah, que saco!',
            'BBQ': 'Churrasco',
            'BRINKS': 'Brincadeira',
            'ADD': 'Adicionar',
            'WTF': 'Que porcaria é essa?!',
            'PQP': 'pita q pariu',
            'FDP': 'filho da pita',
            'CTZ': 'Certeza',
            'MSM': 'Mesmo',
            'N': 'Não',
            'NSFW': 'Não recomendado para o trabalho',
            'VDD': 'Verdade',
            'SQN': 'Só que não',
            'OMG': 'Ai Meu Deus!',
            'MSG': 'Mensagem',
            'PLMDDS': 'Pelo amor de Deus!',
            'PFVR': 'Por favor',
            'BTW': 'A propósito',
            'VLW': 'Valeu',
            'BFF': 'Melhores amigos para sempre',
            'TBT': 'Lembrança do passado',
            'PQ': 'Por que',
            'SDV': 'Segue de volta',
            'DIY': 'Faça você mesmo',
            'OBG': 'Obrigado',
            'SDDS': 'Saudades',
            'AKA': 'Também conhecido como',
            'DM': 'Mensagem direta',
            'TDB': 'Tudo de bom'
        },
    }

    regex_abbrev = '|'.join(abbreviations[lang])


    translator = lambda m: abbreviations[lang][m.group(0).upper()]

    pattern = rf'\b({regex_abbrev})\b'
    return re.sub(pattern, translator, text, flags=re.IGNORECASE)

def remove_markdown(text: str, _: str) -> str:
    html = markdown(text)
    return ''.join(BeautifulSoup(html).findAll(text=True))

def remove_urls(text: str, _: str) -> str:
    return re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)

def remove_readable_ponctuation(text: str, _: str) -> str:
    ponctuations: list[str] = ["*", "-", "~", "^", "`", "#", "/", "\\"]

    for ponctuation in ponctuations:
        text = text.replace(ponctuation, "")
    
    return text


def sanitize(text: str, lang: SupportedLanguages, pipes: list[Callable[[str, SupportedLanguages], str]]):
    for pipe in pipes:
        text = pipe(text, lang)

    return text

