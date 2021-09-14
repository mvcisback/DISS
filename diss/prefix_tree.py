from __future__ import annotations

from typing import Any, Sequence

import attr
import networkx as nx

from diss import Path


def valid_prefix_tree(tree: nx.DiGraph):
    """Checks that tree format looks as expected.

    Format:
      1. At least one leaf node should have a "label" attribute.
      2. Each interior node have an label attribute with value
         "ego" or "env".
      3. Edges coming out of "env" edges should define "prob"
         attribute.
      4. `tree` must be acyclic and have a unique root.
    """
    has_root = has_conform = False
    for node in nx.topological_sort(tree):
        is_root = tree.in_degree(node) == 0
        if is_root and has_root:
            raise ValueError('tree must only have a single root.')
        has_root |= is_root

        if tree.out_degree(node) == 0:
            has_conform |= 'label' in tree.nodes[node]
            continue
        
        if tree.nodes[node]['label'] == 'ego':
            continue

        neighbors = tree.neighbors(node)
        if any('prob' not in tree.edges[node, n] for n in neighbors):
            raise ValueError('env nodes must define distribution.')

    if not has_conform:
        raise ValueError('Must have at least one labeled leaf')


@attr.define
class DemoPrefixTree:
    tree: nx.DiGraph = attr.ib(validator=valid_prefix_tree)

    def leaves(self):  # Corresponds to unique demos.
        yield from (n for n in self.tree.nodes if self.tree.out_degree(n) == 0)

    def deviate(self, path: Path) -> Path:
        """Returns path of the same length which deviates from demos."""
        # TODO
        ...

    def can_deviate(self, path: Path) -> bool:
        """Test whether or not this path indexes a leaf or exhaused node."""
        # TODO
        ...

    @staticmethod
    def from_demos(demos: Sequence[Path]) -> DemoPrefixTree:
        # TODO
        ...
