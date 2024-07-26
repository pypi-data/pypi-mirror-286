from typing import Any, Iterable, Union, get_type_hints
from parserlib.token import Token

__all__ = ("Rule", "Parser", "ShiftReduceParser")


class Rule:
    @classmethod
    def reduce(cls, *tokens: Union[Token, "Rule"]) -> "Rule":
        raise NotImplementedError

    @classmethod
    def syntax(cls) -> tuple[type[Union[Token, "Rule"]], ...]:
        argument_types = get_type_hints(cls.reduce)
        if "return" in argument_types:
            argument_types.pop("return")
        return tuple(argument_types.values())

    @classmethod
    def size(cls) -> int:
        return len(cls.syntax())

    @classmethod
    def match(cls, tokens: list[Token]) -> bool:
        if len(syntax := cls.syntax()) != len(tokens):
            return False
        for argument_type, token in zip(syntax, tokens):
            if not isinstance(token, argument_type):
                return False
        return True


class Parser:
    def __init__(
        self,
        rules: Iterable[Rule],
        precedence: Iterable[Iterable[Rule]] | None = None,
    ) -> None:
        self.rules = list(rules)
        if precedence is None:
            _precedence = [self.rules]
        else:
            _precedence = list(precedence) + [
                tuple(
                    rule
                    for rule in self.rules
                    if not any(rule in level for level in precedence)
                )
            ]
        self._precedence: list[list[Rule]] = _precedence

    def parse(self, tokens: Iterable[Token]) -> Any:
        raise NotImplementedError


class Stack:
    def __init__(self, tokens: Iterable[Token]) -> None:
        self._tokens: list[Union[Token, Rule]] = list(tokens)
        self._index = 0

    def look_ahead(self, size: int) -> list[Union[Token, Rule]]:
        return self._tokens[self._index : self._index + size]

    def consume(self, size: int) -> list[Union[Token, Rule]]:
        tokens = self.look_ahead(size)
        self._tokens[self._index : self._index + size] = []
        return tokens

    def push(self, obj: Union[Token, Rule]) -> None:
        self._tokens.insert(self._index, obj)

    def step(self) -> None:
        self._index += 1

    def reset(self) -> None:
        self._index = 0

    def exhausted(self) -> bool:
        return self._index >= len(self._tokens)


class ShiftReduceParser(Parser):
    MAX_EMPTY_PASS_COUNT = 1000

    def __init__(
        self,
        rules: Iterable[Rule],
        precedence: Iterable[Iterable[Rule]] | None = None,
    ) -> None:
        super().__init__(rules, precedence)
        self.stack: Stack = Stack([])

    def parse(self, tokens: Iterable[Token]) -> Any:
        self.stack = Stack(tokens)
        empty_pass_count = 0
        while True:
            for size in range(1, max(rule.size() for rule in self.rules) + 1):
                if self._pass(size):
                    break  # Break out of the for loop
                self.stack.reset()
            else:
                break  # Break out of the while loop
            empty_pass_count += 1
            if empty_pass_count > self.MAX_EMPTY_PASS_COUNT:
                raise RuntimeError(
                    "Possible infinite loop detected. "
                    "If this is not the case, increase MAX_EMPTY_PASS_COUNT."
                )
        return self.stack._tokens

    def _pass(self, size: int) -> None:
        for level in self._precedence:
            while not self.stack.exhausted():
                for rule in level:
                    buffer = self.stack.look_ahead(size)
                    if rule.match(buffer):
                        self.stack.push(rule.reduce(*self.stack.consume(size)))
                        return True
                self.stack.step()
            self.stack.reset()
        return False
