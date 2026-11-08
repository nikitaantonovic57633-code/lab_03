import json
import pytest

from library_catalog.catalog import Catalog
from library_catalog.models import Book
from library_catalog.storage import save_catalog, load_catalog
from library_catalog.errors import CorruptedFileError, UnsupportedFormatVersionError, InvalidBookError, DuplicateIDError


def test_save_catalog(tmp_path):
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
    path = tmp_path / "books.json"
    save_catalog(catalog, path)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["format_version"] == 1
    assert len(data["books"]) == 1
    assert data["books"][0]["book_id"] == "book-001"
    assert data["books"][0]["name"] == "Преступление и наказание"
    assert data["books"][0]["category"] == "Роман"
    assert data["books"][0]["year"] == 1866
    assert data["books"][0]["author"] == "Фёдор Достоевский"
    assert data["books"][0]["pages"] == 500


def test_save_empty_catalog(tmp_path):
    catalog = Catalog()
    path = tmp_path / "empty.json"
    save_catalog(catalog, path)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["format_version"] == 1
    assert data["books"] == []


def test_load_catalog(tmp_path):
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
    path = tmp_path / "books.json"
    save_catalog(catalog, path)
    loaded_catalog = load_catalog(path)
    assert len(loaded_catalog) == 2
    assert loaded_catalog.get("book-001").book_id == "book-001"
    assert loaded_catalog.get("book-001").category == "Роман"
    assert loaded_catalog.get("book-001").author == "Фёдор Достоевский"

    assert loaded_catalog.get("book-002").name == "Горе от ума"
    assert loaded_catalog.get("book-002").year == 1825
    assert loaded_catalog.get("book-002").pages == 140


def test_load_empty_catalog(tmp_path):
    catalog = Catalog()
    path = tmp_path / "empty.json"
    save_catalog(catalog, path)
    loaded_catalog = load_catalog(path)
    assert len(loaded_catalog) == 0


def test_load_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text('{"format_version": 1, "books": [}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_unsupported_format_version(tmp_path):
    path = tmp_path / "unsupported_format_version.json"
    path.write_text('{"format_version": 2, "books": []}', encoding="utf-8")
    with pytest.raises(UnsupportedFormatVersionError):
        load_catalog(path)


def test_load_missing_format_version(tmp_path):
    path = tmp_path / "missing_format_version.json"
    path.write_text('{"books": []}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_invalid_root(tmp_path):
    path = tmp_path / "invalid_root.json"
    path.write_text('[]', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_missing_books(tmp_path):
    path = tmp_path / "missing_books.json"
    path.write_text('{"format_version": 1}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_invalid_books_type(tmp_path):
    path = tmp_path / "invalid_books_type.json"
    path.write_text('{"format_version": 1, "books": {}}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_invalid_book_type(tmp_path):
    path = tmp_path / "invalid_book_type.json"
    path.write_text('{"format_version": 1, "books": [123]}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_missing_book_field(tmp_path):
    path = tmp_path / "missing_book_field.json"
    path.write_text('{"format_version": 1, "books": [{}]}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_invalid_book(tmp_path):
    path = tmp_path / "invalid_book.json"
    data = {
        "format_version": 1,
        "books": [{
            "book_id": "book-001",
            "name": "Преступление и наказание",
            "category": "Роман",
            "year": 1866,
            "author": "Фёдор Достоевский",
            "pages": -500
        }]
    }
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(InvalidBookError):
        load_catalog(path)


def test_load_duplicate_book_id(tmp_path):
    path = tmp_path / "duplicate_book_id.json"
    data = {
        "format_version": 1,
        "books": [{
            "book_id": "book-001",
            "name": "Преступление и наказание",
            "category": "Роман",
            "year": 1866,
            "author": "Фёдор Достоевский",
            "pages": 500
        }, {
            "book_id": "book-001",
            "name": "Горе от ума",
            "category": "Пьеса",
            "year": 1825,
            "author": "Александр Грибоедов",
            "pages": 140
        }]
    }
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(DuplicateIDError):
        load_catalog(path)


def test_load_no_partial_changes(tmp_path):
    catalog = Catalog()
    book = Book(
        book_id="correct",
        name="Война и мир",
        category="Роман",
        year=1868,
        author="Лев Толстой",
        pages=1300
    )
    catalog.add(book)
    path = tmp_path / "no_partial_changes.json"
    data = {
        "format_version": 1,
        "books": [{
            "book_id": "book-001",
            "name": "Преступление и наказание",
            "category": "Роман",
            "year": 1866,
            "author": "Фёдор Достоевский",
            "pages": 500
        }, {
            "book_id": "book-002",
            "name": "Горе от ума",
            "category": "Пьеса",
            "year": 1825,
            "author": "Александр Грибоедов",
            "pages": -140
        }]
    }
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(InvalidBookError):
        catalog = load_catalog(path)
    assert "correct" in catalog
    assert len(catalog) == 1