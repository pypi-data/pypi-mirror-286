# SPDX-FileCopyrightText: 2024-present Daniele Rapetti <daniele.rapetti@sissa.it>
#
# SPDX-License-Identifier: MIT

# for py3.8
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import re


@dataclass
class BenchmarkRow:
    # name: str
    cycles: int
    total: float
    average: float
    minimum: float
    maximum: float

    def as_list(self) -> list:
        return [self.cycles, self.total, self.average, self.minimum, self.maximum]

    @staticmethod
    def from_re_match(result: re.Match) -> BenchmarkRow:
        """
        A method to create a BenchmarkRow instance from a regex match result.

        Args:
            result (re.Match): The regex match result containing the required groups.

        Returns:
            BenchmarkRow: A BenchmarkRow instance initialized with the extracted data.
        """
        return BenchmarkRow(
            cycles=int(result.group("Cycles")),
            total=float(result.group("Total")),
            average=float(result.group("Average")),
            minimum=float(result.group("Minimum")),
            maximum=float(result.group("Maximum")),
        )

    @staticmethod
    def from_dict(data: dict) -> BenchmarkRow:
        """
        Creates a new instance of the BenchmarkRow class from a dictionary containing the necessary data.

        Args:
            data (dict): A dictionary with the following keys: "Cycles", "Total", "Average", "Minimum", and "Maximum".

        Returns:
            BenchmarkRow: A new instance of the BenchmarkRow class initialized with the data from the dictionary.
        """

        return BenchmarkRow(
            cycles=data["Cycles"],
            total=data["Total"],
            average=data["Average"],
            minimum=data["Minimum"],
            maximum=data["Maximum"],
        )


@dataclass
class KernelBenchmark:
    kernel: str = ""
    input: str = ""
    compare: dict = field(default_factory=dict)
    rows: dict = field(default_factory=dict)

    def has_data(self) -> bool:
        return len(self.rows) > 0 or len(self.compare) > 0 or self.input != "" or self.kernel != ""


@dataclass
class BenchmarkSettings:
    kernels: list = field(default_factory=list)
    inputs: list = field(default_factory=list)
    steps: int = -1
    atoms: int = -1
    maxtime: float = -1.0
    sleep: float = 0.0
    atom_distribution: str = "line"
    shuffled: bool = False
    domain_decomposition: bool = False


@dataclass
class BenchmarkRun:
    settings: BenchmarkSettings = field(default_factory=BenchmarkSettings)
    runs: dict[str, KernelBenchmark] = field(default_factory=dict)

    def extract_rows(self, rows: list) -> dict[str, dict[str, list]]:
        """
        Extracts the specified rows from the given data dictionary.
        Works with the results of plumed_bench_pp.parser.parse_benchmark_output

        Args:
            rows (list): The list of rows to extract.

        Returns:
            dict[str, dict[str,list]]: A dictionary of the simulations.
        """
        df = {}
        for key in self.runs:
            tmp = {}
            for row in rows:
                tmp[row] = self.runs[key].rows[row].as_list()
            df[key] = tmp

        return df
