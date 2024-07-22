from typing import Literal

import pkg_resources
from lark import Lark, Transformer
from lark.visitors import merge_transformers

from .transformers import (
    LEDES1998BTransformer,
    LineItemTransformer,
)

SUPPORTED_SPECS = frozenset(["LEDES98B"])
LEDES_SPECS = frozenset(
    ["LEDES98B", "LEDES98BI", "LEDES98BIV2", "LEDES2000", "LEDESXML20", "LEDESXML21"]
)
SupportedSpecs = Literal["LEDES98B"]


class UnrecognizedLEDESVersionError(ValueError):
    pass


class UnsupportedLEDESVersionError(NotImplementedError):
    pass


def get_transformer(spec: SupportedSpecs) -> Transformer:
    if spec == "LEDES98B":
        return merge_transformers(
            base_transformer=LEDES1998BTransformer(), line_item=LineItemTransformer()
        )
    else:
        return None


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
            f"Cannot produce a parser. The grammar for {spec} has not been written yet. Supported specifications are: {SUPPORTED_SPECS}."
        )

    # By convention, the grammar for a spec is in: grammars/<the-spec>/main_grammar.lark
    grammar_directory = f"grammars/{spec.upper()}"
    main_grammar_file = f"{grammar_directory}/main_grammar.lark"
    path_to_grammar = pkg_resources.resource_filename(__name__, main_grammar_file)
    import_paths = pkg_resources.resource_filename(__name__, grammar_directory)
    transformer = get_transformer(spec) if not ast_only else None

    return Lark.open(
        path_to_grammar,
        start="start",
        parser="lalr",
        import_paths=[import_paths],
        transformer=transformer,
    )
