from typing import Literal

import pkg_resources
from lark import Lark
from lark.visitors import merge_transformers

from .transformers import (
    LEDES1998BTransformer,
    LineItemTransformer,
)

SUPPORTED_SPECS = frozenset(["1998B"])
LEDES_SPECS = frozenset(
    ["1998B", "1998BI", "1998BIV2", "2000", "2020", "XML20", "XML21"]
)
SupportedSpecs = Literal["1998B"]


class UnrecognizedLEDESVersionError(ValueError):
    pass


class UnsupportedLEDESVersionError(NotImplementedError):
    pass


def get_parser(spec: SupportedSpecs, ast_only: bool = False) -> Lark:
    """
    @returns A parser that can read ledes text in the given ledes spec (e.g., 1998B, 1998BI, etc...).
    @param ast_only: Whether the parser should return just the abstract syntax tree, instead of mapping the tokens to a dict.
    """
    if spec not in LEDES_SPECS:
        raise UnrecognizedLEDESVersionError(
            f"Cannot produce a parser. '{spec}' is not a known LEDES specification. Recognized specifications are: {LEDES_SPECS}."
        )

    if spec not in SUPPORTED_SPECS:
        raise UnsupportedLEDESVersionError(
            f"Cannot produce a parser. The grammar for LEDES {spec} has not been written yet. Supported specifications are: {SUPPORTED_SPECS}."
        )

    # By convention, the grammar for a spec is in: grammars/spec_<the-spec>/main_grammar.lark
    main_grammar_file = f"grammars/spec_{spec.upper()}/main_grammar.lark"
    path_to_grammar = pkg_resources.resource_filename(__name__, main_grammar_file)
    import_paths = pkg_resources.resource_filename(
        __name__, f"grammars/spec_{spec.upper()}"
    )
    # For now, hard-coded to 98B.
    transformer = (
        merge_transformers(
            base_transformer=LEDES1998BTransformer(), line_item=LineItemTransformer()
        )
        if not ast_only
        else None
    )

    return Lark.open(
        path_to_grammar,
        start="start",
        parser="lalr",
        import_paths=[import_paths],
        transformer=transformer,
    )
