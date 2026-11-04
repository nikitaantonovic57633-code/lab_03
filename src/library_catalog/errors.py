class CatalogError(Exception):
    pass

class InvalidBookError(CatalogError):
    pass

class DuplicateIDError(CatalogError):
    pass

class BookNotFoundError(CatalogError):
    pass

class UnsupportedFormatVersionError(CatalogError):
    pass

class CorruptedFileError(CatalogError):
    pass