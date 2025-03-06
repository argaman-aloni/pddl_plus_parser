"""Contains some tests for the functionality in the PDDL domain class."""
import networkx as nx

from pddl_plus_parser.models import PDDLType
from pddl_plus_parser.models.pddl_type import create_type_hierarchy_graph

t1 = PDDLType("object")
t2 = PDDLType("vehicle", t1)
t3 = PDDLType("car", t2)
t4 = PDDLType("truck", t2)
t5 = PDDLType("sedan", t3)
t6 = PDDLType("hatchback", t3)
t7 = PDDLType("pickup", t4)
t8 = PDDLType("bus", t2)


def find_root_nodes(G: nx.DiGraph) -> str:
    """
    Finds the root nodes of the directed graph (nodes with in-degree 0).
    """
    return [node for node in G.nodes if G.in_degree(node) == 0][0]


def test_create_type_hierarchy_graph_creates_correct_graph_from_input_data():
    # Dictionary of types
    types_dict = {
        "object": t1,
        "vehicle": t2,
        "car": t3,
        "truck": t4,
        "sedan": t5
    }

    # Create the graph
    type_hierarchy_graph = create_type_hierarchy_graph(types_dict)
    hierarchy_bfs = list(nx.bfs_tree(type_hierarchy_graph, find_root_nodes(type_hierarchy_graph)).nodes())
    assert hierarchy_bfs == ["object", "vehicle", "car", "truck", "sedan"]



def test_create_type_hierarchy_graph_creates_correct_graph_from_input_data_when_more_complex_hierarchy_introduced():
    # Dictionary of types
    types_dict = {
        "object": t1,
        "vehicle": t2,
        "car": t3,
        "truck": t4,
        "sedan": t5,
        "hatchback": t6,
        "pickup": t7,
        "bus": t8
    }

    # Create the graph
    type_hierarchy_graph = create_type_hierarchy_graph(types_dict)
    hierarchy_bfs = list(nx.bfs_tree(type_hierarchy_graph, find_root_nodes(type_hierarchy_graph)).nodes())
    assert hierarchy_bfs == ["object", "vehicle", "car", "truck", "bus", "sedan", "hatchback", "pickup"]


def test_create_type_hierarchy_graph_creates_correct_graph_from_input_data_also_returns_parents():
    # Dictionary of types
    types_dict = {
        "object": t1,
        "vehicle": t2,
        "car": t3,
        "truck": t4,
        "sedan": t5,
        "hatchback": t6,
        "pickup": t7,
        "bus": t8
    }

    # Create the graph
    type_hierarchy_graph = create_type_hierarchy_graph(types_dict)
    root = find_root_nodes(type_hierarchy_graph)
    hierarchy_with_parents = [(child, parent) for parent, child in nx.bfs_edges(type_hierarchy_graph, root)]
    print(hierarchy_with_parents)