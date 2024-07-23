# SPDX-FileCopyrightText: 2024-present Daniele Rapetti <daniele.rapetti@sissa.it>
#
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Any

    from matplotlib.container import BarContainer
    from numpy import ndarray
    from pandas import DataFrame

from matplotlib.pyplot import Axes


def plot_histo(
    ax: Axes,
    data: "list[dict]|dict[str,DataFrame]",
    row: str,
    barwidth: float = 0.8,
    *,
    normalize_to_cycles: "bool|str" = False,
    x: "ndarray|None" = None,
    colors: "list|None" = None,
    relative_to: "dict[str, DataFrame]| Any" = None,
    relative_to_row: "str|None" = None,
    titles: "list[str]|None" = None,
) -> "list[BarContainer]":
    """
    Plot a histogram based on the provided data for a specified row.

    It can be set up to normalize the data to cycles or relative to another row.
    It can be set up to use a custom x-axis or colors for the bars.
    It can be set up to plot relative to another dataset, dividing the value of each olume by that number.

    Parameters:
        ax (Axes): The matplotlib axes to plot the histogram.
        data (list[dict]|dict[str,DataFrame]): The data to be plotted.
        row (str): The row in the data to be plotted.
        barwidth (float, optional): The width of the bars in the histogram. Defaults to 0.8.
        normalize_to_cycles (bool|str, optional): Flag to normalize data to cycles. Defaults to False.
        x (np.array|None, optional): The x values for plotting. Defaults to None.
        colors (list|None, optional): The colors for the bars in the histogram. Defaults to None.
        relative_to (dict[str, DataFrame]| Any, optional): Data for relative comparison, you can pass a dict contianing the collection of data or the address or index of the desired base in the passed data. Defaults to None.
        relative_to_row (str|None, optional): The row for relative comparison. Defaults to None.

    Returns:
        list: The list of plotted bars.
    """
    if not isinstance(data, list):
        data = [data]

    row_cycles = row
    if isinstance(normalize_to_cycles, str):
        # row_cycles is introduced because usually the TOTALTIME is a "single cycle"
        # and the info on the effective number of steps is in the timer relative to apply or calculate
        row_cycles = normalize_to_cycles
        normalize_to_cycles = True
    divideby = 1
    if relative_to is not None:
        # relative to mode
        if not isinstance(relative_to, dict):
            # in this case relative_to assubed to be the index of the data
            relative_to = data[relative_to]
        if relative_to_row is None:
            relative_to_row = row
        divideby = relative_to[relative_to_row].Total.values
        if normalize_to_cycles:
            divideby = divideby / relative_to[row_cycles].Cycles.values

    ncols = len(data)
    if x is None:
        x = data[0][row].natoms.values
    width = np.min(np.diff(np.sort(x))) * (barwidth / ncols)
    ax.set_xticks(x + width * 0.5 * (ncols - 1), x)
    bars = []
    for multiplier, d in enumerate(data):
        offset = width * multiplier

        toplot = d[row].Total.values
        if normalize_to_cycles:
            toplot = toplot / d[row_cycles].Cycles.values
        toplot = toplot / divideby
        xpos = x
        if len(x) > len(d[row].natoms.values):
            # with this if a natom is missing it does not create errors, this will conflict is x is inpute as not None
            xpos = d[row].natoms.values
        bars.append(
            ax.bar(
                xpos + offset,
                toplot,
                width,
                color=colors[multiplier] if colors else None,
                label=titles[multiplier] if titles else None,
            )
        )
    return bars


def plot_histo_relative(
    ax: Axes,
    data: "list[dict]|dict[str,DataFrame]",
    row: str,
    relative_to: "dict[str, DataFrame]| Any",
    relative_to_row: "str|None" = None,
    barwidth: float = 0.8,
    *,
    normalize_to_cycles: "bool|str" = False,
    x: "ndarray|None" = None,
    colors: "list|None" = None,
) -> "list[BarContainer]":
    """a shortcut to generate a relative histogram, with relative_to options set as positional arguments"""
    return plot_histo(
        ax,
        data,
        row,
        barwidth=barwidth,
        normalize_to_cycles=normalize_to_cycles,
        x=x,
        colors=colors,
        relative_to=relative_to,
        relative_to_row=relative_to_row,
    )
