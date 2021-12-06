from typing import Any, Optional, Sequence

import attr
import funcy as fn
import dfa
import numpy as np
from dfa import DFA
from dfa.utils import find_subset_counterexample, find_equiv_counterexample
from dfa_identify import find_dfa, find_dfas

from diss import LabeledExamples, ConceptIdException
from diss.concept_classes.dfa_concept import DFAConcept


__all__ = ['to_concept', 'ignore_white']


def transition(s, c):
    if c == 'red':
        return s | 0b01
    elif c == 'yellow':
        return s | 0b10
    return s


ALPHABET = frozenset({'red', 'yellow', 'blue', 'green'})


PARTIAL_DFA =  DFA(
    start=0b00,
    inputs=ALPHABET,
    label=lambda s: s == 0b10,
    transition=transition
)


def ignore_white(path):
    return tuple(x for x in path if x != 'white')


def subset_check_wrapper(dfa_candidate):
    partial = partial_dfa(dfa_candidate.inputs)
    return find_subset_counterexample(dfa_candidate, partial) is None



BASE_EXAMPLES = LabeledExamples(
    positive=[
        ('yellow',),
        ('yellow', 'yellow'),
    ],
    negative=[
        (), ('red',), ('red', 'red'),
        ('red', 'yellow'), ('yellow', 'red'),
        ('yellow', 'red', 'yellow'),
        ('yellow', 'yellow', 'red'),
    ]
)


@attr.define
class PartialDFAIdentifier:
    partial: DFAConcept = attr.ib(converter=DFAConcept.from_dfa)
    base_examples: LabeledExamples = LabeledExamples()

    def partial_dfa(self, inputs) -> DFA:
        assert inputs <= self.partial.dfa.inputs
        return attr.evolve(self.partial.dfa, inputs=inputs)

    def subset_ce(self, candidate: DFA) -> Optional[Sequence[Any]]:
        partial = self.partial_dfa(candidate.inputs)
        return find_subset_counterexample(candidate, partial)

    def is_subset(self, candidate: DFA) -> Optional[Sequence[Any]]:
        return self.subset_ce(candidate) is None

    def __call__(self, data: LabeledExamples) -> DFAConcept:
        data = data.map(ignore_white)
        data @= self.base_examples
        for i in range(20):
            mydfa = find_dfa(data.positive, data.negative, order_by_stutter=True) 
            if mydfa is None:
                raise ConceptIdException
            ce = self.subset_ce(mydfa)
            if ce is None:
                break
            self.base_examples @= LabeledExamples(negative=[ce])
            data @= LabeledExamples(negative=[ce])
   
        concept = DFAConcept.from_examples(
            data=data,
            filter_pred=self.is_subset,
            alphabet=self.partial.dfa.inputs,
        ) 
        # Adjust size to account for subset information.
        return attr.evolve(concept, size=concept.size - self.partial.size)
