from datetime import date
import pytest

from library_catalog.errors import InvalidBookError
from library_catalog.models import Book

def test_create_valid_book():
    book = Book(
        book_id="book-001",
        name="Преступление и наказание",
        category="Роман",
        year=1866,
        author="Фёдор Достоевский",
        pages=500
    )
    assert book.book_id == "book-001"
    assert book.name == "Преступление и наказание"
    assert book.category == "Роман"
    assert book.year == 1866
    assert book.author == "Фёдор Достоевский"
    assert book.pages == 500


@pytest.mark.parametrize("book_id", ["", "   ", "\t", 123])
def test_create_book_with_invalid_book_id(book_id):
    with pytest.raises(InvalidBookError):
        Book(
            book_id=book_id,
            name="Преступление и наказание",
            category="Роман",
            year=1866,
            author="Фёдор Достоевский",
            pages=500
        )


@pytest.mark.parametrize("name", ["", "   ", "\t", 123])
def test_create_book_with_invalid_name(name):
    with pytest.raises(InvalidBookError):
        Book(
            book_id="book-001",
            name=name,
            category="Роман",
            year=1866,
            author="Фёдор Достоевский",
            pages=500
        )


@pytest.mark.parametrize("category", ["", "   ", "\t", 123])
def test_create_book_with_invalid_category(category):
    with pytest.raises(InvalidBookError):
        Book(
            book_id="book-001",
            name="Преступление и наказание",
            category=category,
            year=1866,
            author="Фёдор Достоевский",
            pages=500
        )


@pytest.mark.parametrize("year", [-1, 0, date.today().year + 1, "123", 123.4, True])
def test_create_book_with_invalid_year(year):
    with pytest.raises(InvalidBookError):
        Book(
            book_id="book-001",
            name="Преступление и наказание",
            category="Роман",
            year=year,
            author="Фёдор Достоевский",
            pages=500
        )


@pytest.mark.parametrize("author", ["", "   ", "\t", 123])
def test_create_book_with_invalid_author(author):
    with pytest.raises(InvalidBookError):
        Book(
            book_id="book-001",
            name="Преступление и наказание",
            category="Роман",
            year=1866,
            author=author,
            pages=500
        )


@pytest.mark.parametrize("pages", [-1000, 0, "123", 123.4, False])
def test_create_book_with_invalid_pages(pages):
    with pytest.raises(InvalidBookError):
        Book(
            book_id="book-001",
            name="Преступление и наказание",
            category="Роман",
            year=1866,
            author="Фёдор Достоевский",
            pages=pages
        )