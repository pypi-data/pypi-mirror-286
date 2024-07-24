from typing import Optional
from pandiag.model.graph import Edge, EdgeStyle, Graph, Node, Subgraph
from pandiag.utils import indent

import hashlib
import re

def _sanitize_label(label: str) -> str:
    # TODO: Find a better way to sanitize the label
    return re.sub(r'[()]', '', label.replace('\n', '<br/>')).strip() if label else None

def _format_label(label: Optional[str]) -> str:
    # TODO: Generate more readable node names than SHA1 hashes
    label = _sanitize_label(label)
    return f"{hashlib.sha1(label.encode()).hexdigest()}[{label}]" if label else 'None'

def _format_node(node: Node) -> str:
    return _format_label(node.label)

def _format_arrow(edge: Edge, graph: Graph) -> str:
    if graph.directed:
        match edge.style:
            case EdgeStyle.DASHED:
                return f"{'<-' if edge.source_arrow else '-'}.{'->' if edge.dest_arrow else '-'}"
            case EdgeStyle.SOLID:
                return f"{'<' if edge.source_arrow else '-'}-{'>' if edge.dest_arrow else '-'}"
    else:
        return '---'

def _format_edge(edge: Edge, graph: Graph) -> str:
    return f"{_format_label(edge.source)} {_format_arrow(edge, graph=graph)}{f'|{_sanitize_label(edge.label)}|' if edge.label else ''} {_format_label(edge.dest)}"

def _format_subgraph(subgraph: Subgraph, graph: Graph) -> list[str]:
    return [
        *(_format_node(n) for n in subgraph.nodes),
        *(_format_edge(e, graph=graph) for e in subgraph.edges),
        *(l for g in subgraph.subgraphs for l in [
            f'subgraph {_format_label(g.name)}',
            *indent(_format_subgraph(g, graph)),
            'end',
        ]),
    ]

def _format_graph(graph: Graph) -> list[str]:
    return [
        'flowchart TD',
        *indent(_format_subgraph(graph.rootgraph, graph=graph)),
    ]

def format(graph: Graph) -> str:
    return '\n'.join(_format_graph(graph))

def format_markdown(graph: Graph) -> str:
    return '\n'.join([
        '```mermaid',
        format(graph),
        '```',
    ])
