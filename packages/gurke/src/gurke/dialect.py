from __future__ import annotations

import io
import json
import os
from typing import Dict, List, Optional

DIALECT_FILE_PATH = os.path.join(os.path.dirname(__file__), "gherkin-languages.json")

with io.open(DIALECT_FILE_PATH, "r", encoding="utf-8") as file:
    DIALECTS = json.load(file)


class Dialect(object):
    @classmethod
    def for_name(cls, name: str) -> Optional[Dialect]:
        return cls(DIALECTS[name]) if name in DIALECTS else None

    def __init__(self, spec: Dict[str, List[str]]) -> None:
        self.spec = spec

    @property
    def feature_keywords(self) -> List[str]:
        return self.spec["feature"]

    @property
    def rule_keywords(self) -> List[str]:
        return self.spec["rule"]

    @property
    def scenario_keywords(self) -> List[str]:
        return self.spec["scenario"]

    @property
    def scenario_outline_keywords(self) -> List[str]:
        return self.spec["scenarioOutline"]

    @property
    def background_keywords(self) -> List[str]:
        return self.spec["background"]

    @property
    def examples_keywords(self) -> List[str]:
        return self.spec["examples"]

    @property
    def given_keywords(self) -> List[str]:
        return self.spec["given"]

    @property
    def when_keywords(self) -> List[str]:
        return self.spec["when"]

    @property
    def then_keywords(self) -> List[str]:
        return self.spec["then"]

    @property
    def and_keywords(self) -> List[str]:
        return self.spec["and"]

    @property
    def but_keywords(self) -> List[str]:
        return self.spec["but"]
