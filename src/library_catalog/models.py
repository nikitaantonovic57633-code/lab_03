from dataclasses import dataclass
from datetime import date
from .errors import InvalidBookError


@dataclass
class Book:
    book_id: str
    name: str
    category: str
    year: int
    author: str
    pages: int

    def __post_init__(self):
        if not isinstance(self.book_id, str):
            raise InvalidBookError("ID книги должен быть строкой")
        if not isinstance(self.name, str):
            raise InvalidBookError("Название книги должно быть строкой")
        if not isinstance(self.category, str):
            raise InvalidBookError("Категория книги должна быть строкой")
        if type(self.year) is not int:
            raise InvalidBookError("Год издания книги должен быть целым числом")
        if not isinstance(self.author, str):
            raise InvalidBookError("Автор книги должен быть строкой")
        if type(self.pages) is not int:
            raise InvalidBookError("Количество страниц в книге должно быть целым числом")

        if not self.book_id.strip():
            raise InvalidBookError("ID книги не должен быть пустой строкой")
        if not self.name.strip():
            raise InvalidBookError("Название книги не должно быть пустой строкой")
        if not self.category.strip():
            raise InvalidBookError("Категория книги не должна быть пустой строкой")
        if not self.author.strip():
            raise InvalidBookError("Автор книги не должен быть пустой строкой")

        if self.year < 1 or self.year > date.today().year:
            raise InvalidBookError("Некорректный год издания книги")
        if self.pages < 1:
            raise InvalidBookError("Некорректное количество страниц в книге")