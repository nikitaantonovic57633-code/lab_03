import json
from dataclasses import asdict
from .catalog import Catalog

def save_catalog(catalog: Catalog, path: str):
    data = {
        "format_version": 1,
        "books": []
    }
    for book in catalog:
        data["books"].append(asdict(book))

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)