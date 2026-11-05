import pytest

from library_catalog.catalog import Catalog
from library_catalog.models import Book
from library_catalog.errors import DuplicateIDError, InvalidBookError, BookNotFoundError


def test_add_book():
    catalog = Catalog()
    book = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    catalog.add(book)
    assert len(catalog._books) == 1


def test_add_book_with_duplicate_id():
    catalog = Catalog()
    book1 = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    book2 = Book(
        book_id="book-001",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    with pytest.raises(DuplicateIDError):
        catalog.add(book2)
    assert len(catalog._books) == 1


def test_add_invalid_object():
    catalog = Catalog()
    book = "book-001"
    with pytest.raises(InvalidBookError):
        catalog.add(book)
    assert len(catalog._books) == 0


def test_get_existing_book():
    catalog = Catalog()
    book = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    catalog.add(book)
    assert catalog.get("book-001") is book


def test_get_nonexisting_book():
    catalog = Catalog()
    book = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    catalog.add(book)
    with pytest.raises(BookNotFoundError):
        catalog.get("book-000")