import graphviz
from abc import ABC, abstractmethod

from src.token import Token


class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass


class Statement(Node, ABC):
    pass


class Expression(Node, ABC):
    pass


class Program(Node):
    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        res = ""
        for statement in self.statements:
            res += f"{str(statement)}"
        return res


class LetStatement(Statement):
    def __init__(self, token: Token):
        self.token = token

        self.name: Identifier = None
        self.value: Expression = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"{self.token_literal()} {str(self.name)} = {str(self.value) if self.value else ''};"


class Identifier(Expression):
    def __init__(self, token: Token, literal: str):
        self.token = token
        self.value = literal

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return self.value


class ReturnStatement(Statement):
    def __init__(self, token: Token):
        self.token = token

        self.return_value: Expression = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"{self.token_literal()} {str(self.return_value) if self.return_value else ''};"


class ExpressionStatement(Statement):
    """Since the Program node contains only statements, we must wrap
    expressions in statements to have `5+5` be a valid program."""

    def __init__(self, token: Token):
        self.token = token

        self.expression: Expression = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return str(self.expression) if self.expression else ""


class IntegerLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token

        self.value: int = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return self.token_literal()


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str):
        self.token = token
        self.operator = operator

        self.right: Expression = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"({self.operator}{self.right})"


class InfixExpression(Expression):
    def __init__(self, token: Token, operator: str, left: Expression):
        self.token = token
        self.operator = operator
        self.left = left

        self.right: Expression = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"


class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class BlockStatement(Statement):
    def __init__(self, token: Token):
        self.token = token

        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        res = ""
        for statement in self.statements:
            res += f"{str(statement)}"
        return res


class IfExpression(Expression):
    def __init__(self, token: Token):
        self.token = token

        self.condition: Expression = None
        self.consequence: BlockStatement = None
        self.alternative: BlockStatement = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        result = f"if {self.condition} {{{self.consequence}}}"
        if self.alternative:
            result += f" else {{{self.alternative}}}"
        return result


class FunctionLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token

        self.parameters: list[Identifier] = []
        self.body: BlockStatement = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"fn({', '.join(str(p) for p in self.parameters)}) {{{str(self.body)}}}"


class CallExpression(Expression):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression: Expression = expression

        self.arguments: list[Expression] = []

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{str(self.expression)}({', '.join([str(a) for a in self.arguments])})"


def ast_to_dot(node: Node) -> graphviz.Digraph:
    # gpt generated mess
    dot = graphviz.Digraph()

    def add_node(graph, node: Node, parent_id=None):
        node_id = id(node)
        label = node.__class__.__name__

        if isinstance(node, Identifier):
            label = f"{label}: {node.value}"
        elif isinstance(node, IntegerLiteral):
            label = f"{label}: {node.value}"
        elif isinstance(node, Boolean):
            label = f"{label}: {node.value}"
        elif isinstance(node, InfixExpression):
            label = f"{label}: {node.operator}"
        elif isinstance(node, PrefixExpression):
            label = f"{label}: {node.operator}"

        graph.node(str(node_id), label)

        if parent_id is not None:
            graph.edge(str(parent_id), str(node_id))

        if isinstance(node, Program):
            for statement in node.statements:
                add_node(graph, statement, node_id)
        elif isinstance(node, LetStatement):
            add_node(graph, node.name, node_id)
            add_node(graph, node.value, node_id)
        elif isinstance(node, ReturnStatement):
            add_node(graph, node.return_value, node_id)
        elif isinstance(node, ExpressionStatement):
            add_node(graph, node.expression, node_id)
        elif isinstance(node, BlockStatement):
            for statement in node.statements:
                add_node(graph, statement, node_id)
        elif isinstance(node, IfExpression):
            add_node(graph, node.condition, node_id)
            add_node(graph, node.consequence, node_id)
            if node.alternative:
                add_node(graph, node.alternative, node_id)
        elif isinstance(node, FunctionLiteral):
            for param in node.parameters:
                add_node(graph, param, node_id)
            add_node(graph, node.body, node_id)
        elif isinstance(node, CallExpression):
            add_node(graph, node.expression, node_id)
            for arg in node.arguments:
                add_node(graph, arg, node_id)
        elif isinstance(node, PrefixExpression):
            add_node(graph, node.right, node_id)
        elif isinstance(node, InfixExpression):
            add_node(graph, node.left, node_id)
            add_node(graph, node.right, node_id)

    add_node(dot, node)
    return dot
