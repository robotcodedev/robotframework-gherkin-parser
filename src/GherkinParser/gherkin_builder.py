import ast
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import robot.running
from gurke.errors import CompositeParserException
from gurke.parser import Parser
from gurke.pickles.compiler import Compiler
from gurke.token_matcher import TokenMatcher
from gurke.token_matcher_markdown import GherkinInMarkdownTokenMatcher
from robot.api import SuiteVisitor
from robot.parsing.lexer import Token
from robot.parsing.model.blocks import CommentSection, File, SettingSection, TestCase, TestCaseSection
from robot.parsing.model.statements import (
    Documentation,
    Error,
    KeywordCall,
    KeywordName,
    LibraryImport,
    Metadata,
    ResourceImport,
    SectionHeader,
    Tags,
    TestTags,
)
from robot.utils.filereader import FileReader

from .glob_path import iter_files


def find_ast_node_id(
    node: Any, id: str, parent: Any = None
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    if isinstance(node, dict) and "id" in node and node["id"] == id:
        return node, parent

    if isinstance(node, dict):
        for v in node.values():
            n, p = find_ast_node_id(v, id, node)
            if n is not None:
                return n, p

    elif isinstance(node, list):
        for v in node:
            n, p = find_ast_node_id(v, id, parent)
            if n is not None:
                return n, p

    return None, None


def build_gherkin_model(source: PathLike[str], content: Optional[str] = None) -> Tuple[ast.AST, Optional[str]]:
    try:
        path = Path(source).resolve()

        if content is None:
            with FileReader(path) as reader:
                content = reader.read()

        parser = Parser()

        gherkin_document = parser.parse(
            content,
            token_matcher=GherkinInMarkdownTokenMatcher() if path.suffix == ".md" else TokenMatcher(),
        )

        gherkin_document["uri"] = path
        pickles = Compiler().compile(gherkin_document)

        feature_tags = gherkin_document["feature"]["tags"]

        test_cases = []

        for pickle in pickles:
            testcase_body = []

            tags = [r["name"][1:] for r in pickle["tags"] if not any(f["id"] == r["astNodeId"] for f in feature_tags)]

            if tags:
                testcase_body.append(Tags.from_params(tags))

            for step in pickle["steps"]:
                node, _parent = find_ast_node_id(gherkin_document, step["astNodeIds"][0])
                if node is None:
                    continue

                datatable = node.get("dataTable")
                args: Tuple[str, ...] = ()

                if datatable:
                    rows = [[v.get("value") for v in r.get("cells")] for r in datatable["rows"]]
                    args = (f"${{{{{rows!r}}}}}",)

                keyword_call = KeywordCall.from_params(
                    f"{node['keyword'] if step['type']!='Unknown' else ''}{step['text']}", args=args
                )

                if node is not None and "location" in node:
                    location = node["location"]

                    column = 0
                    for t in keyword_call.tokens:
                        t.lineno = location.line

                        if t.type == Token.KEYWORD:
                            t.col_offset = location.column - 1

                            column = t.end_col_offset
                        else:
                            t.col_offset = column

                testcase_body.append(keyword_call)

            node, _parent = find_ast_node_id(gherkin_document, pickle["astNodeIds"][0])

            test_case_name = pickle["name"]
            if len(pickle["astNodeIds"]) > 1:
                e_node, e_parent = find_ast_node_id(gherkin_document, pickle["astNodeIds"][1])
                if e_node and "cells" in e_node and e_parent is not None and e_parent["keyword"] == "Examples":
                    for i, s in enumerate(e_node["cells"]):
                        test_case_name += f" {e_parent['tableHeader']['cells'][i]['value']} = {s['value']}"

            test_case = TestCase(KeywordName.from_params(test_case_name), body=testcase_body)

            if node is not None and "location" in node:
                location = node["location"]

                test_case.header.tokens[0].lineno = location.line
                test_case.header.tokens[0].col_offset = location.column - 1
            test_cases.append(test_case)

        resources = [f for f in iter_files(path.parent, "**/*.resource") if not f.stem.startswith(("_", "."))]

        doc = gherkin_document["feature"]["description"].strip()
        settings = [
            *([Documentation.from_params(doc)] if doc else []),
            LibraryImport.from_params("GherkinParser.Library"),
            *[
                ResourceImport.from_params(f)
                for f in sorted((str(r.relative_to(path.parent).as_posix()) for r in resources), key=str)
            ],
            *(
                [
                    Metadata.from_params("Tags", ", ".join((r["name"][1:] for r in feature_tags))),
                    TestTags.from_params((r["name"][1:] for r in feature_tags)),
                ]
                if feature_tags
                else []
            ),
        ]

        file = File(
            [
                SettingSection(
                    SectionHeader.from_params(Token.SETTING_HEADER),
                    body=settings,
                ),
                TestCaseSection(
                    SectionHeader.from_params(Token.TESTCASE_HEADER),
                    body=test_cases,
                ),
            ],
            source=str(path),
        )

        # file.save(path.with_suffix(".robot").with_stem("_" + path.name))

        return file, gherkin_document["feature"]["name"]
    except (SystemExit, KeyboardInterrupt):
        raise
    except BaseException as ex:
        errors = []

        if isinstance(ex, CompositeParserException):
            for e in ex.errors:
                token = Token(
                    Token.ERROR,
                    "",
                    e.location.line,
                    e.location.column - 1 if e.location is not None else 0,
                    str(e),
                )
                errors.append(Error.from_tokens([token]))
        else:
            token = Token(Token.ERROR, "", 1, 0, f"{type(ex).__qualname__}: {ex}")
            errors.append(Error.from_tokens([token]))

        return (
            File(
                [
                    CommentSection(
                        SectionHeader.from_params(Token.COMMENT_HEADER),
                        body=errors,
                    ),
                ],
                source=str(path),
            ),
            None,
        )


def collect_gherkin_suites(path: Path) -> List[robot.running.TestSuite]:
    feature_files = [f for f in iter_files(path, "**/*.{feature,feature.md}")]

    return [build_gherkin_model(f) for f in feature_files]


class GherkinRunner(SuiteVisitor):
    def __init__(self, *included: str) -> None:
        super().__init__()
        self.included = included

    def start_suite(self, suite: robot.running.TestSuite) -> None:
        if suite.source and Path(suite.source).is_dir():
            suite.suites = [*suite.suites, *collect_gherkin_suites(Path(suite.source))]

    def end_suite(self, suite: robot.running.TestSuite) -> None:
        pass
