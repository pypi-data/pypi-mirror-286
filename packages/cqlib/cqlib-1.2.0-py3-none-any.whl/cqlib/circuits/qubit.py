# This code is part of cqlib.
#
# Copyright (C) 2024 China Telecom Quantum Group, QuantumCTek Co., Ltd.,
# Center for Excellence in Quantum Information and Quantum Physics.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Quantum bit."""

from __future__ import annotations

import weakref


class Qubit:
    """Quantum bit."""
    __slots__ = ["_index", '_initialized', '_hash', '__weakref__']
    _cache = weakref.WeakValueDictionary[int, 'QuBit']()

    def __new__(cls, index: int) -> Qubit:
        """
        Create a new Qubit instance or return an existing one from
        the cache based on the given index.

        Args:
            index: The logical index of the qubit which must be non-negative.

        Returns:
            An instance of Qubit.
        """
        if index < 0:
            raise ValueError("Qubit index must be non-negative.")
        inst = cls._cache.get(index)
        if inst is None:
            inst = super().__new__(cls)
            inst._index = index
            inst._hash = None
            cls._cache[index] = inst
        return inst

    def __init__(self, index: int):
        """
        Initialize a new Qubit instance.

        Args:
            index: logical index of the qubit
        """
        if not hasattr(self, '_initialized'):
            self._index = index
            self._hash = None
            self._initialized = True

    @property
    def index(self) -> int:
        """Returns the logical index of the qubit."""
        return self._index

    def __repr__(self):
        return f"{self.__class__.__name__}({self.index})"

    def __str__(self):
        return f'Q{self.index}'

    def __copy__(self):
        """
        Returns a reference to the same qubit instance since qubits
        should be unique.
        """
        return self

    def __eq__(self, other: Qubit) -> bool:
        """Check equality with another qubit based on the index."""
        if isinstance(other, Qubit):
            return self.index == other.index
        return False

    def __hash__(self) -> int:
        """
        Return the hash based on the qubit's index, used for collections
        that depend on hashable items.
        """
        if self._hash is None:
            self._hash = hash(self._index)
        return self._hash
