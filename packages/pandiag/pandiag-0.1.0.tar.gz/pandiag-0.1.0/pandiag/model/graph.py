from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Edge:
    source: Optional[str]
    dest: Optional[str]

@dataclass
class Subgraph:
    name: str = ''
    edges: list[Edge] = field(default_factory=list)
    subgraphs: list[Subgraph] = field(default_factory=list)

    def merge(self, other: Subgraph):
        self.edges += other.edges
        self.subgraphs += other.subgraphs

@dataclass
class Graph:
    directed: bool = False
    rootgraph: Subgraph = field(default_factory=Subgraph)
