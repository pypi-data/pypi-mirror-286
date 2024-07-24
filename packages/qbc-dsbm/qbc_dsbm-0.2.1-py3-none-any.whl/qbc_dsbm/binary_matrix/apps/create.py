"""Application module for binary matrix creation."""

import ast
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
import typer
from sklearn.impute import KNNImputer

from qbc_dsbm.binary_matrix import BinMatrix, NotABinaryMatrixError

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s [%(levelname)s] %(message)s",
)
console_handler.setFormatter(formatter)
_LOGGER.addHandler(console_handler)


APP = typer.Typer()


@dataclass
class CommonArgs:
    """Common args and opts."""

    ARG_INPUT_MATRIX = typer.Argument(
        help="Path to the non-binary matrix",
    )

    ARG_OUTPUT_MATRIX = typer.Argument(
        help="Path to the output binary matrix",
    )


@dataclass
class CustomArgs:
    """Custom args and opts."""

    ARG_VALUE_REPLACED = typer.Argument(
        help=('Value to replace as a python dict in a string, e.g. "{-1: 1, -2: 0}"'),
    )


@dataclass
class KNNArgs:
    """KNN args and opts."""

    OPT_NUMBER_OF_NEIGHBOURS_DEF = 10
    OPT_NUMBER_OF_NEIGHBOURS = typer.Option(
        default=OPT_NUMBER_OF_NEIGHBOURS_DEF,
        help="Number of nearest neighbours",
    )

    OPT_THRESHOLD_DEF = 0.3
    OPT_THRESHOLD = typer.Option(
        default=OPT_THRESHOLD_DEF,
        help=(
            "Threshold confident interval:"
            " if 0 <= values < threshold, then value -> 0,"
            " else if 1 - threshold < values <= 1, then value -> 1,"
            " else value -> undefined"
        ),
    )

    OPT_UNDEFINED_VALUE_DEF = 0
    OPT_UNDEFINED_VALUE = typer.Option(
        default=OPT_UNDEFINED_VALUE_DEF,
        help="Undefined value for measure out of the threshold interval",
    )


@APP.command()
def custom(
    input_matrix: Path = CommonArgs.ARG_INPUT_MATRIX,
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
    value_replaced: str = CustomArgs.ARG_VALUE_REPLACED,
) -> None:
    """Transform non-binary matrix to binary matrix with custom replacement."""
    try:
        value_replaced_dict = ast.literal_eval(value_replaced)
    except SyntaxError:
        _LOGGER.critical("Invalid value_replaced: %s", value_replaced_dict)
        sys.exit(1)
    if not isinstance(value_replaced_dict, dict):
        _LOGGER.critical("Invalid value_replaced: %s", value_replaced_dict)
        sys.exit(1)

    try:
        bin_matrix = BinMatrix.from_csv(
            input_matrix,
            replace_value_map=cast(dict, value_replaced),
        )
    except NotABinaryMatrixError as err:
        _LOGGER.critical("Output matrix is not a binary matrix:")
        _LOGGER.critical(err)
        sys.exit(1)

    bin_matrix.to_csv(output_matrix)


@APP.command()
def random(
    input_matrix: Path = CommonArgs.ARG_INPUT_MATRIX,
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
) -> None:
    """Transform non-binary matrix to binary matrix with random replacement."""
    df: pd.DataFrame = pd.read_csv(input_matrix, header=0, index_col=0)

    rng = np.random.default_rng()
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i, j] not in (0, 1):
                df.iloc[i, j] = rng.choice([0, 1], 1)

    BinMatrix.new_unsafe(df).to_csv(output_matrix)


@APP.command()
def knn(
    input_matrix: Path = CommonArgs.ARG_INPUT_MATRIX,
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
    number_of_neighbours: int = KNNArgs.OPT_NUMBER_OF_NEIGHBOURS,
    threshold: float = KNNArgs.OPT_THRESHOLD,
    undefined_value: int = KNNArgs.OPT_UNDEFINED_VALUE,
) -> None:
    """Transform non-binary matrix to binary matrix with KNN replacement."""
    _LOGGER.info("KNN replacement")
    _LOGGER.info("Input matrix: %s", input_matrix)
    _LOGGER.info("Output matrix: %s", output_matrix)
    _LOGGER.info("Number of neighbours: %s", number_of_neighbours)
    _LOGGER.info(
        "Threshold: %s (confidence intervals: [0, %f[ and ]%f, 1])",
        threshold,
        threshold,
        1 - threshold,
    )
    _LOGGER.info("Undefined value: %s", undefined_value)
    df: pd.DataFrame = pd.read_csv(input_matrix, header=0, index_col=0)
    m, n = df.shape

    if m > 1 and n > 1:
        imputer = KNNImputer(n_neighbors=number_of_neighbours)
        matrix = imputer.fit_transform(df)
        matrix[(matrix > 1 - threshold)] = 1
        matrix[(matrix < threshold)] = 0
        matrix[(matrix <= 1 - threshold) * (matrix >= threshold)] = (
            undefined_value  # XXX TAM replaces them by -1
        )
        matrix = pd.DataFrame(matrix, index=df.index, columns=df.columns)
    else:
        matrix = df

    try:
        bin_matrix = BinMatrix(matrix)
    except NotABinaryMatrixError as err:
        _LOGGER.critical("Output matrix is not a binary matrix:")
        _LOGGER.critical(err)
        sys.exit(1)

    bin_matrix.to_csv(output_matrix)


if __name__ == "__main__":
    APP()
