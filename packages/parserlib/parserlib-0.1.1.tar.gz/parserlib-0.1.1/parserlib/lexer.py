import itertools
import re
from typing import Generator, Iterable, Type
from parserlib.token import Token


__all__ = "Lexer"


class Lexer:
    def __init__(
        self,
        tokens: Iterable[Type[Token]],
        ignore_characters: str = "",
        newline_characters: str = "\n",
        flags: int = 0,
    ) -> None:
        self.tokens = tuple(tokens)
        self.ignore_characters = tuple(ignore_characters)
        self.newline_characters = tuple(newline_characters)
        self.flags = flags

    def feed(self, data: str) -> Generator[Token, None, None]:
        yield from self._process(data, current_position=(0, 0))

    def _process(
        self, data: str, current_position: tuple[int, int]
    ) -> Generator[Token, None, None]:
        if not data:
            return
        elif result := self._find_token_match(data, current_position):
            new_position, token = result
            yield token
            yield from self._process(
                data[len(token.body) :],
                current_position=new_position,
            )
        elif data.startswith(self.newline_characters):
            yield from self._process(
                data[1:],
                current_position=(current_position[0] + 1, 0),
            )
        elif data.startswith(self.ignore_characters):
            yield from self._process(
                data[1:],
                current_position=(current_position[0], current_position[1] + 1),
            )
        else:
            raise SyntaxError(f"Unexpected sequence: {data.split()[0]!r}")

    def _find_token_match(
        self, data: str, current_position: tuple[int, int]
    ) -> tuple[int, tuple[int, int], Token] | None:
        for stack in itertools.accumulate(data):
            for token in self.tokens:
                if match := re.match(token.regex, stack, flags=self.flags):
                    lines_jumped = stack.count("\n")
                    columns_jumped = len(stack.split("\n")[-1])
                    return (
                        current_position[0] + lines_jumped,
                        current_position[1] + columns_jumped,
                    ), token(match, position=current_position)
        return None
