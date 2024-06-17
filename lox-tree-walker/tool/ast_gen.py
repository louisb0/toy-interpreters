import sys

# TODO: Rework this garbage

ast_header = """
from abc import ABC

from lox.lexer import Token
from lox.visitors import Visitor


class Expression(ABC):
    pass
"""

visitor_header = """
from abc import ABC, abstractmethod

import lox.ast as ast
"""


def format_node(class_spec: dict) -> str:
    name, super_class = map(str.strip, class_spec["name"].split(":"))
    attributes = [attr.strip() for attr in class_spec["attributes"]]

    inline_attributes_str = ", ".join(attributes)
    defn_attributes_str = "\n        ".join(
        f"self.{attr.split(':')[0].strip()} = {attr.split(':')[0].strip()}"
        for attr in attributes
    )

    return f"""class {name}({super_class}):
    def __init__(self, {inline_attributes_str}):
        {defn_attributes_str}
        
    def accept(self, visitor: Visitor):
        return visitor.visit{name}{super_class}(self)
    """


def format_visitor_abc(class_specs: list[dict]) -> str:
    res = "class Visitor(ABC):"

    for class_spec in class_specs:
        name, super_class = map(str.strip, class_spec["name"].split(":"))
        res += f"""
    @abstractmethod
    def visit{name}{super_class}(self, expr: ast.{name}):
        pass\n"""

    return res


def generate(spec: list[str]) -> tuple[str, str]:
    res = ""

    attribute_store: list[str] = []
    class_specs: list[dict] = []
    while len(spec):
        if not spec[-1][0].isalpha():
            attribute_store.append(spec.pop().strip())
        else:
            class_spec = {"name": spec.pop().strip(), "attributes": attribute_store}
            res += f"\n\n{format_node(class_spec)}"

            class_specs.append(class_spec)
            attribute_store.clear()

    # ': Any' is not a valid type annotation in native python3.11
    # so we drop it, could deal in format_node() but...........
    ast = (ast_header + res).strip().replace(": Any", "")
    visitor = (visitor_header + "\n\n" + format_visitor_abc(class_specs)).strip()

    return ast, visitor


def main():
    if len(sys.argv) != 2:
        print("Usage: ast_gen.py [spec.yml]")
    else:
        with open(sys.argv[1], "r") as f:
            generated_ast, generated_visitors = generate(f.readlines())

        with open("ast_out.py", "w") as f:
            f.write(generated_ast)

        with open("visitors_out.py", "w") as f:
            f.write(generated_visitors)


if __name__ == "__main__":
    main()
