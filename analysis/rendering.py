from graphviz import Digraph

def buildGraph(node, graph = None, minCount = 10):
    """
        Creates a graph for the current node
    
        Arguments:
            node {Node} -- Father node
            graph {Digraph}

        Returns:
            Digraph
    """
    if graph is None:
        graph = Digraph()

    if node.count <= minCount:
        return apply_styles(graph) 

    graph.node(str(node.id), label=node.name)
    for child in node.children:
        graph.edge(str(node.id), str(child.id), label=str(child.count))
        graph = buildGraph(child, graph, minCount)
        
    return apply_styles(graph)

def apply_styles(graph):
    styles = {
        'nodes': {
            'fontname': 'Helvetica',
            'shape': 'hexagon',
            'fontcolor': 'white',
            'color': 'black',
            'style': 'filled',
            'fillcolor': '#006699',
        },
        'edges': {
            'style': 'dashed',
            'color': 'black',
            'arrowhead': 'open',
            'fontname': 'Helvetica',
            'fontsize': '12',
            'fontcolor': 'black',
        }
    }

    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph