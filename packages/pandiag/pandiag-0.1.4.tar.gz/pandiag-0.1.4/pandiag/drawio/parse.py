from __future__ import annotations
from dataclasses import dataclass, field
from pandiag.model.graph import Edge, EdgeStyle, Graph, Node, Subgraph

import base64
import re
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

@dataclass
class _Cell:
    element: ET.Element
    childs: list[_Cell] = field(default_factory=list)

def _strip_html(raw: str) -> str:
    # TODO: Be cleverer about this, perhaps use a proper HTML parser
    raw = raw.replace('<br>', '\n')
    raw = re.sub(f'<[^>]+>', '', raw)
    return raw

def _construct_subgraph(cells: list[_Cell], cells_by_id: dict[str, _Cell]) -> Subgraph:
    subgraph = Subgraph()

    # TODO: Perhaps support ids so we don't have to write the full labels into each edge?
    for cell in cells:
        label = _strip_html(cell.element.get('value')) if 'value' in cell.element.attrib else None

        style = {
            kv[0]: kv[1] if len(kv) > 1 else None
            for raw in cell.element.get('style').split(';')
            for kv in [raw.split('=')]
            if raw
        } if 'style' in cell.element.attrib else None

        if cell.element.attrib.get('edge') == '1':
            source = cells_by_id[cell.element.attrib['source']] if 'source' in cell.element.attrib else None
            target = cells_by_id[cell.element.attrib['target']] if 'target' in cell.element.attrib else None

            subgraph.edges.append(Edge(
                source=_strip_html(source.element.get('value')) if source else None,
                dest=_strip_html(target.element.get('value')) if target else None,
                source_arrow=style['startArrow'] != 'none' if 'startArrow' in style else False,
                dest_arrow=style['endArrow'] != 'none' if 'endArrow' in style else True,
                style=EdgeStyle.DASHED if style.get('dashed') == '1' else EdgeStyle.SOLID,
                label=label,
            ))
        elif label:
            subgraph.nodes.append(Node(label))

        if len(cell.childs) > 0:
            subsubgraph = _construct_subgraph(
                cells=cell.childs,
                cells_by_id=cells_by_id,
            )
            subsubgraph.name = label
            if subsubgraph.name:
                subgraph.subgraphs.append(subsubgraph)
            else:
                # Flatten the structure if the subgraph has no name
                subgraph.merge(subsubgraph)
    
    return subgraph

def _parse_mxgraphmodel(element: ET.Element) -> Graph:
    cells_by_id = {cell.attrib['id']: _Cell(cell) for cell in element.findall('.//mxCell')}
    root_cells: list[_Cell] = []

    # Construct tree
    for id, cell in list(cells_by_id.items()):
        if parent := cell.element.attrib.get('parent'):
            cells_by_id[parent].childs.append(cell)
        else:
            root_cells.append(cell)

    return Graph(
        directed=True,
        rootgraph=_construct_subgraph(
            cells=root_cells,
            cells_by_id=cells_by_id
        ),
    )

def _parse_diagram(element: ET.Element) -> Graph:
    compressed = base64.b64decode(element.text)
    decompressed = zlib.decompress(compressed, wbits=-15)
    xml = urllib.parse.unquote(decompressed)
    element = ET.fromstring(xml)
    return _parse_mxgraphmodel(element)

def parse(raw: str) -> list[Graph]:
    element = ET.fromstring(raw)
    return [_parse_diagram(e) for e in element.findall('diagram')]
