from typing import Any, Iterable, Protocol, Optional


class DiGraph:
    nodes: dict[Any, dict[str, Any]]
    edges: dict[tuple[Any, Any], dict[str, Any]]

    def __init__(self, graph: Optional[DiGraph]): ...
    def in_degree(self, node: Any) -> int: ...
    def out_degree(self, node: Any) -> int: ...
    def neighbors(self, node: Any) -> Iterable[Any]: ...
    def predecessors(self, node: Any) -> Iterable[Any]: ...
    

def topological_sort(dag: DiGraph) -> Iterable[Any]: ...
def prefix_tree(paths: Iterable[Any]) -> DiGraph: ...