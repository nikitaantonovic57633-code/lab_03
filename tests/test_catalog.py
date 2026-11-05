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
    assert len(catalog) == 1


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
    assert len(catalog) == 1


def test_add_invalid_object():
    catalog = Catalog()
    book = "book-001"
    with pytest.raises(InvalidBookError):
        catalog.add(book)
    assert len(catalog) == 0


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


def test_remove_existing_book():
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
    catalog.remove("book-001")
    assert len(catalog) == 0


def test_remove_nonexisting_book():
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
        catalog.remove("book-000")
    assert len(catalog) == 1


def test_find_by_category():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    book3 = Book(
        book_id="book-003",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book1)
    catalog.add(book2)
    catalog.add(book3)
    result = catalog.find_by_category("Роман")
    assert result == [book1, book3]


def test_find_by_category_no_matches():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    book3 = Book(
        book_id="book-003",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book1)
    catalog.add(book2)
    catalog.add(book3)
    result = catalog.find_by_category("Комедия")
    assert result == []


def test_find_by_category_independence():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    book3 = Book(
        book_id="book-003",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book1)
    catalog.add(book2)
    catalog.add(book3)
    result = catalog.find_by_category("Роман")
    result.clear()
    assert len(catalog) == 3


def test_find_by_name():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    catalog.add(book2)
    result = catalog.find_by_name("Горе от ума")
    assert result == [book2]


def test_find_by_name_register():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    catalog.add(book2)
    result = catalog.find_by_name("ГОРЕ ОТ УМА")
    assert result == [book2]


def test_find_by_name_no_matches():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    catalog.add(book2)
    result = catalog.find_by_name("Вельд")
    assert result == []


def test_find_by_name_independence():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    catalog.add(book2)
    result = catalog.find_by_name("Горе от ума")
    result.clear()
    assert len(catalog) == 2


def test_catalog_length():
    catalog = Catalog()
    assert len(catalog) == 0
    book1 = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    book2 = Book(
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    catalog.add(book1)
    catalog.add(book2)
    assert len(catalog) == 2
    catalog.remove("book-001")
    assert len(catalog) == 1


def test_catalog_iteration_order():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    book3 = Book(
        book_id="book-003",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book2)
    catalog.add(book1)
    catalog.add(book3)
    result = []
    for book in catalog:
        result.append(book)
    assert result == [book2, book1, book3]


def test_catalog_contains():
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
        book_id="book-002",
        name="Горе от ума",
        category="Пьеса",
        year=1825,
        author="Александр Грибоедов",
        pages=140
    )
    book3 = Book(
        book_id="book-003",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book1)
    catalog.add(book2)
    catalog.add(book3)
    assert "book-001" in catalog
    assert "book-000" not in catalog
    catalog.remove("book-003")
    assert "book-003" not in catalog