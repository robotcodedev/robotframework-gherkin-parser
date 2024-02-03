from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Optional, cast

from gurke.token import Token


class AstNode:
    def __init__(self, rule_type: str) -> None:
        self.rule_type = rule_type
        self._sub_items: Dict[Optional[str], List[Any]] = defaultdict(list)

    def add(self, rule_type: Optional[str], obj: Any) -> None:
        self._sub_items[rule_type].append(obj)

    def get_single(self, rule_type: str, default_value: Any = None) -> AstNode:
        return cast(AstNode, self._sub_items[rule_type][0] if self._sub_items[rule_type] else default_value)

    def get_items(self, rule_type: str) -> List[Any]:
        return self._sub_items[rule_type]

    def get_token(self, token_type: str) -> Token:
        return cast(Token, self.get_single(token_type))

    def get_tokens(self, token_type: str) -> List[Token]:
        return [v for v in self._sub_items[token_type] if isinstance(v, Token)]
