import io
import os
from typing import Union

from .gherkin_line import GherkinLine
from .location import Location
from .token import Token


class TokenScanner(object):
    def __init__(self, path_or_str: Union[os.PathLike[str], str]) -> None:
        if isinstance(path_or_str, os.PathLike):
            self.io = io.open(path_or_str, "r", encoding="utf8")
        else:
            self.io = io.StringIO(path_or_str)
        self.line_number = 0

    def read(self) -> Token:
        self.line_number += 1
        line = self.io.readline()
        return Token(GherkinLine(line, self.line_number), Location(self.line_number, None))

    def __del__(self) -> None:
        try:
            self.io.close()
        except AttributeError:
            pass
