import os
import sys

BOOK_PATH = 'book/Bredberi_Marsianskie-hroniki.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    CHAR_LST = ',.!:;?'
    text = text[start:]
    for i in range(1, 300):
        if text[:size][-i] in CHAR_LST and text[:size + 1][-i] not in CHAR_LST:
            text = text[:size - i + 1]
            break
    return text, len(text)

# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open (path, 'r', encoding='utf-8-sig') as f:
        text = f.read()

        i = 1
        while text:
            i_text, i_start = _get_part_text(text, start=0, size=PAGE_SIZE)
            book[i] = i_text.lstrip()
            text = text[i_start:]
            i += 1

# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
