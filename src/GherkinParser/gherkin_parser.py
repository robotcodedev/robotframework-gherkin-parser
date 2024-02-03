from pathlib import Path
from typing import ClassVar, Sequence, Union

from robot.api.interfaces import Parser
from robot.running import TestDefaults, TestSuite
from robot.running.builder.settings import FileSettings
from robot.running.builder.transformers import SuiteBuilder

from .gherkin_builder import build_gherkin_model


class GherkinParser(Parser):
    extension: ClassVar[Union[str, Sequence[str]]] = [
        ".feature",
        ".feature.md",
        #    ".md",
    ]

    def parse(self, source: Path, defaults: TestDefaults) -> TestSuite:
        model, name = build_gherkin_model(source)
        suite = TestSuite(name=name or "", source=source)
        SuiteBuilder(suite, FileSettings(defaults)).build(model)

        return suite
