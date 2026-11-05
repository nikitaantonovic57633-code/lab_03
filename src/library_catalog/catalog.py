from .models import Book
from .errors import InvalidBookError, DuplicateIDError, BookNotFoundError


class Catalog:
    def __init__(self):
        self._books = {}

    def add(self, item: Book) -> None:
        if not isinstance(item, Book):
            raise InvalidBookError("Книга введена неверно")
        if item.book_id in self._books:
            raise DuplicateIDError("Такая книга уже есть в каталоге")
        self._books[item.book_id] = item

    def get(self, item_id: str):
        if item_id not in self._books:
            raise BookNotFoundError("Книга не найдена")
        return self._books[item_id]

    def remove(self, item_id: str):
        if item_id not in self._books:
            raise BookNotFoundError("Книга не найдена")
        del self._books[item_id]

    def find_by_category(self, category: str):
        result = []
        for book in self._books.values():
            if book.category == category:
                result.append(book)
        return result

    def find_by_name(self, query: str):
        result = []
        for book in self._books.values():
            if book.name.lower() == query.lower():
                result.append(book)
        return result