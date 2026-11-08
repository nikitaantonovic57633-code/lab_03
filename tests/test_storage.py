import json
from library_catalog.catalog import Catalog
from library_catalog.models import Book
from library_catalog.storage import save_catalog


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