import pytest
from gurke.errors import ParserError
from gurke.location import Location
from gurke.parser import Parser
from gurke.token_matcher import TokenMatcher
from gurke.token_scanner import TokenScanner


def test_parser() -> None:
    parser = Parser()
    feature_file = parser.parse(TokenScanner("Feature: Foo"))
    expected = {
        "comments": [],
        "feature": {
            "keyword": "Feature",
            "language": "en",
            "location": Location(line=1, column=1),
            "name": "Foo",
            "description": "",
            "children": [],
            "tags": [],
        },
    }

    assert expected == feature_file


def test_parse_multiple_features() -> None:
    parser = Parser()
    ff1 = parser.parse(TokenScanner("Feature: 1"))
    ff2 = parser.parse(TokenScanner("Feature: 2"))

    assert "1" == ff1["feature"]["name"]
    assert "2" == ff2["feature"]["name"]


def test_parse_feature_after_parser_error() -> None:
    parser = Parser()
    with pytest.raises(ParserError):
        parser.parse(
            TokenScanner(
                "# a comment\n"
                "Feature: Foo\n"
                "  Scenario: Bar\n"
                "    Given x\n"
                "      ```\n"
                "      unclosed docstring\n"
            )
        )
    feature_file = parser.parse(
        TokenScanner(
            "Feature: Foo\n" + "  Scenario: Bar\n" + "    Given x\n"
            '      """\n'
            "      closed docstring\n"
            '      """\n'
        )
    )
    expected = [
        {
            "scenario": {
                "id": "1",
                "name": "Bar",
                "description": "",
                "keyword": "Scenario",
                "tags": [],
                "steps": [
                    {
                        "id": "0",
                        "text": "x",
                        "location": Location(column=5, line=3),
                        "keyword": "Given ",
                        "keywordType": "Context",
                        "docString": {
                            "content": "closed docstring",
                            "delimiter": '"""',
                            "location": Location(column=7, line=4),
                        },
                    }
                ],
                "location": Location(column=3, line=2),
                "examples": [],
            }
        }
    ]

    assert expected == feature_file["feature"]["children"]


def test_change_the_default_language() -> None:
    parser = Parser()
    matcher = TokenMatcher("no")
    feature_file = parser.parse(TokenScanner("Egenskap: i18n support - åæø"), matcher)
    expected = {
        "comments": [],
        "feature": {
            "keyword": "Egenskap",
            "language": "no",
            "location": Location(column=1, line=1),
            "name": "i18n support - åæø",
            "description": "",
            "children": [],
            "tags": [],
        },
    }

    assert expected == feature_file
