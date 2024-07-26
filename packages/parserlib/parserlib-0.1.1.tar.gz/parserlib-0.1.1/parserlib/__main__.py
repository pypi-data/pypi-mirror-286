from parserlib.lexer import Lexer
from parserlib.parser import Rule, ShiftReduceParser
from parserlib.token import Token


class NumberToken(Token):
    name = "NUMBER"
    regex = r"\d+"


class PlusToken(Token):
    name = "PLUS"
    regex = r"\+"


class MinusToken(Token):
    name = "MINUS"
    regex = r"-"


class LeftParenthesisToken(Token):
    name = "LEFT_PARENTHESIS"
    regex = r"\("


class RightParenthesisToken(Token):
    name = "RIGHT_PARENTHESIS"
    regex = r"\)"


class AsteriskToken(Token):
    name = "ASTERISK"
    regex = r"\*"


class SlashToken(Token):
    name = "SLASH"
    regex = r"/"


class Expression(Rule):
    pass


class NumberExpression(Expression):
    def __init__(self, number: NumberToken):
        self.number = number

    @classmethod
    def reduce(cls, number: NumberToken) -> Expression:
        return cls(number)


class ParenthesisExpression(Expression):
    @classmethod
    def reduce(
        cls, _: LeftParenthesisToken, expression: Expression, __: RightParenthesisToken
    ) -> Expression:
        return expression


class PlusExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @classmethod
    def reduce(cls, left: Expression, _: PlusToken, right: Expression) -> Expression:
        return cls(left, right)


class MinusExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @classmethod
    def reduce(cls, left: Expression, _: MinusToken, right: Expression) -> Expression:
        return cls(left, right)


class TimesExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @classmethod
    def reduce(
        cls, left: Expression, _: AsteriskToken, right: Expression
    ) -> Expression:
        return cls(left, right)


class DivideExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @classmethod
    def reduce(cls, left: Expression, _: SlashToken, right: Expression) -> Expression:
        return cls(left, right)


def main() -> None:
    lexer = Lexer(
        tokens=(
            NumberToken,
            PlusToken,
            MinusToken,
            LeftParenthesisToken,
            RightParenthesisToken,
            AsteriskToken,
            SlashToken,
        ),
        ignore_characters=" \t",
    )
    parser = ShiftReduceParser(
        rules=(
            ParenthesisExpression,
            PlusExpression,
            MinusExpression,
            TimesExpression,
            DivideExpression,
            NumberExpression,
        ),
        precedence=(
            (ParenthesisExpression,),
            (TimesExpression, DivideExpression),
            (PlusExpression, MinusExpression),
        ),
    )
    tree = parser.parse(lexer.feed("1 + \n(2) * 3"))
    print(tree)


if __name__ == "__main__":
    main()
