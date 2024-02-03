from typing import Any, List, Optional

from .gherkin_line import GherkinLine
from .location import Location


class Token:
    def __init__(self, gherkin_line: GherkinLine, location: Location):
        self.line = gherkin_line
        self.location = location

        # TODO: check types
        self.matched_text: str = ""
        self.matched_type: str = ""
        self.matched_items: List[Any] = []
        self.matched_keyword: Optional[str] = None
        self.matched_keyword_type: Optional[str] = None
        self.matched_indent: int = -1
        self.matched_gherkin_dialect: Optional[str] = None

    def eof(self) -> bool:
        return not self.line

    def detach(self) -> None:
        pass  # TODO: detach line - is this needed?

    def token_value(self) -> str:
        return "EOF" if self.eof() or not self.line else self.line.get_line_text()
