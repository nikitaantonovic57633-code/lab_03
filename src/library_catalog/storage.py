import json
from dataclasses import asdict

from .catalog import Catalog
from .errors import UnsupportedFormatVersionError, CorruptedFileError
from .models import Book


def save_catalog(catalog: Catalog, path: str):
    data = {
        "format_version": 1,
        "books": []
    }
    for book in catalog:
        data["books"].append(asdict(book))

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_catalog(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise CorruptedFileError("Файл повреждён") from error

    if not isinstance(data, dict):
        raise CorruptedFileError("Неверная структура JSON")
    if "format_version" not in data:
        raise CorruptedFileError("Отсутствует версия формата")
    if data["format_version"] != 1:
        raise UnsupportedFormatVersionError("Неподдерживаемый формат версии файла")

    if "books" not in data:
        raise CorruptedFileError("Отсутствует список книг")
    if not isinstance(data["books"], list):
        raise CorruptedFileError("Список книг имеет неверный формат")

    catalog = Catalog()
    for item in data["books"]:
        if not isinstance(item, dict):
            raise CorruptedFileError("Неверная структура данных книги")
        try:
            book = Book(
                book_id=item["book_id"],
                name=item["name"],
                category=item["category"],
                year=item["year"],
                author=item["author"],
                pages=item["pages"]
            )
        except KeyError as error:
            raise CorruptedFileError("Отсутствует обязательное поле книги") from error
        catalog.add(book)

    return catalog