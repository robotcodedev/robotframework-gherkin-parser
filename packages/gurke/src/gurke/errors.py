from typing import List, Optional, Sequence

from .location import Location
from .token import Token


class ParserError(Exception):
    pass


class ParserException(ParserError):  # noqa: N818
    def __init__(self, message: str, location: Optional[Location] = None) -> None:
        self.location = location
        super(ParserException, self).__init__(
            (f"({location.line}:{location.column or 0}): " if location is not None else "") + message
        )


class NoSuchLanguageException(ParserException):
    def __init__(self, language: str, location: Optional[Location] = None) -> None:
        super().__init__("Language not supported: " + language, location)


class AstBuilderException(ParserException):
    pass


class UnexpectedEOFException(ParserException):
    def __init__(self, received_token: Token, expected_token_types: Sequence[str]) -> None:
        message = "unexpected end of file, expected: " + ", ".join(expected_token_types)
        super().__init__(message, received_token.location)


class UnexpectedTokenException(ParserException):
    def __init__(self, received_token: Token, expected_token_types: Sequence[str]) -> None:
        message = (
            "expected: " + ", ".join(expected_token_types) + ", got '" + received_token.token_value().strip() + "'"
        )
        column = received_token.location.column
        location = (
            received_token.location
            if column
            else Location(received_token.location.line, received_token.line.indent + 1)
        )
        super().__init__(message, location)


class CompositeParserException(ParserError):  # noqa: N818
    def __init__(self, errors: List[BaseException]) -> None:
        self.errors = errors
        super().__init__("Parser errors:\n" + "\n".join([error.args[0] for error in errors]))
