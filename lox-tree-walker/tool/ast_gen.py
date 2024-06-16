import sys

# TODO: Rework this garbage

header = """
from abc import ABC, abstractmethod

from lox.lexer import Token


class Expression(ABC):
    pass
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
        
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit{name}{super_class}(self)
    """


def format_visitor_abc(class_specs: list[dict]) -> str:
    res = "class ExpressionVisitor(ABC):"

    for class_spec in class_specs:
        name, super_class = map(str.strip, class_spec["name"].split(":"))
        res += f"""
    @abstractmethod
    def visit{name}{super_class}(self, expr: "{name}"):
        pass\n"""

    return res


def generate(spec: list[str]) -> str:
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

    res = "\n\n" + format_visitor_abc(class_specs) + res

    # ': Any' is not a valid type annotation in native python3.11
    # so we drop it, could deal in format_node() but...........
    return (header + res).strip().replace(": Any", "")


def main():
    if len(sys.argv) != 2:
        print("Usage: ast_gen.py [spec.yml]")
    else:
        with open(sys.argv[1], "r") as f:
            generated_ast = generate(f.readlines())

        with open("ast_out.py", "w") as f:
            f.write(generated_ast)


if __name__ == "__main__":
    main()
