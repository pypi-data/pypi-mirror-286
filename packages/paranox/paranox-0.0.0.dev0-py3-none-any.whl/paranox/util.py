# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Miscellaneous utility functions for neural network parameters.
"""

from __future__ import annotations

from typing import Any, Tuple, Union

import jax
import numpy as np
from numpyro.distributions import Distribution as Distr

# TODO: replace with jaxtyping or similar at some point
Tensor = Union[jax.Array, np.ndarray]
PyTree = Any
Distribution = Distr


def where_weight(model: PyTree) -> Tensor:
    return model.weight


def argsort(seq):
    # Sources:
    # (1) https://stackoverflow.com/questions/3382352/ ...
    #     equivalent-of-numpy-argsort-in-basic-python
    # (2) http://stackoverflow.com/questions/3071415/ ...
    #     efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)


# TODO: Determine if there's already something that handles this in jax
def axis_complement(
    ndim: int,
    axis: Union[int, Tuple[int, ...]],
) -> Tuple[int, ...]:
    """
    Return the complement of the axis or axes for a tensor of dimension ndim.
    """
    if isinstance(axis, int):
        axis = (axis,)
    ax = [True for _ in range(ndim)]
    for a in axis:
        ax[a] = False
    ax = [i for i, a in enumerate(ax) if a]
    return tuple(ax)


# TODO: determine if we can replace this with one of the canonicalise axis
# functions from jax
# We can use this from numpy:
# https://numpy.org/devdocs/reference/generated/ ...
# numpy.lib.array_utils.normalize_axis_tuple.html
# However, the way to import this varies across numpy versions.
def standard_axis_number(axis: int, ndim: int) -> int:
    """
    Convert an axis number to a standard axis number.
    """
    if axis < 0 and axis >= -ndim:
        axis += ndim
    elif axis < -ndim or axis >= ndim:
        return None
    return axis
