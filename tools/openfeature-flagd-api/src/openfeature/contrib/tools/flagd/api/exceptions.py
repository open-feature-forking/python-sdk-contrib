class FlagStoreError(Exception):
    """Exception raised when flag store operations fail.

    Evaluator implementations should raise this when the underlying flag
    store encounters an unrecoverable error (e.g. corrupt configuration,
    I/O failures during flag loading).
    """


# Backwards-compatible alias
FlagStoreException = FlagStoreError
