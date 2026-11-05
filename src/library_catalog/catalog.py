from .models import Book
from .errors import InvalidBookError, DuplicateIDError


class Catalog:
    def __init__(self):
        self._books = {}
    def add(self, item: Book) -> None:
        if not isinstance(item, Book):
            raise InvalidBookError("Книга введена неверно")
        if item.book_id in self._books:
            raise DuplicateIDError("Такая книга уже есть в каталоге")
        self._books[item.book_id] = item