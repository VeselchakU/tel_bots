import os
import sys

BOOK_PATH = 'book/Bredberi_Marsianskie-hroniki.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    result_string = text[start : start + size + 1]
    flag = True

    if size + 1 <= len(text[start:]):
        while result_string[-1] in ",.!:;?":
            result_string = result_string[:-1]
            flag = False

        if flag:
            result_string = result_string[:-1]

        while result_string[-1] not in ",.!:;?":
            result_string = result_string[:-1]

    return result_string, len(result_string)

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
