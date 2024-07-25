from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union

try:
    from functools import singledispatchmethod
except:
    from singledispatchmethod import singledispatchmethod

if TYPE_CHECKING:
    from quantagonia.qubo.term import QuboTerm
    from quantagonia.qubo.variable import QuboVariable


class QuboExpression(object):
    def __init__(self):
        super().__init__()

        # hash -> (term with coefficient)
        self.terms = {}

    def _clone(self) -> QuboExpression:
        q = QuboExpression()
        for k in self.terms:
            q.terms[k] = self.terms[k]._clone()

        return q

    ###
    # ADDITION + SUBTRACTION
    ###

    # join clones of term dictionaries
    def _join_terms(
        self, terms0: Dict[str, QuboTerm], terms1: Dict[str, QuboTerm], op_coefficient: float
    ) -> Dict[str, QuboTerm]:
        joint_terms = {}
        for key, term in terms0.items():
            joint_terms[key] = term._clone()
        for k in terms1:
            if k in joint_terms:
                joint_terms[k].coefficient += op_coefficient * terms1[k].coefficient
            else:
                joint_terms[k] = terms1[k]._clone()

        return joint_terms

    # join second dictionary into first
    def _left_join_terms(
        self, terms0: Dict[str, QuboTerm], terms1: Dict[str, QuboTerm], op_coefficient: float
    ) -> Dict[str, QuboTerm]:
        for k in terms1:
            if k in terms0:
                terms0[k].coefficient += op_coefficient * terms1[k].coefficient
            else:
                terms0[k] = terms1[k]._clone()

        return terms0

    @singledispatchmethod
    def __iadd__(self, other):  # noqa ANN001, ANN201
        return NotImplemented

    @singledispatchmethod
    def __isub__(self, other):  # noqa ANN001, ANN201
        return NotImplemented

    def __add__(self, other: Union[int, float, QuboVariable, QuboTerm, QuboExpression]):
        q = self._clone()
        return q.__iadd__(other)

    def __sub__(self, other: Union[int, float, QuboVariable, QuboTerm, QuboExpression]):
        q = self._clone()
        return q.__isub__(other)

    @singledispatchmethod
    def __radd__(self, other):  # noqa ANN001, ANN201
        return NotImplemented

    @singledispatchmethod
    def __rsub__(self, other):  # noqa ANN001, ANN201
        return NotImplemented

    @singledispatchmethod
    def __imul__(self, other):  # noqa ANN001, ANN201
        return NotImplemented

    def __mul__(self, other: Union[int, float, QuboVariable, QuboTerm, QuboExpression]):
        q = self._clone()
        q *= other
        return q

    def __rmul__(self, other: Union[int, float]):
        q = self._clone()
        for _, term in q.terms.items():
            term *= other
        return q

    def eval(self, shift: float = 0) -> float:
        evaluation = shift

        for term in self.terms:
            evaluation += self.terms[term].eval()

        return evaluation

    def is_valid(self) -> bool:
        valid = True

        for _, term in self.terms.items():
            valid &= term.is_valid()

        return valid

    def __str__(self):
        s = " ".join([str(self.terms[t]) for t in self.terms])

        return s
