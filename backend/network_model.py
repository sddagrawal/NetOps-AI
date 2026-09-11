import networkx as nx

class NetworkGraph:
    """
    Maintains a Graph-based Digital Twin representation of the physical network topology.
    Utilizes NetworkX for dependency mapping and shortest-path analysis.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_topology()

    def _build_topology(self):
        # Nodes with attributes
        nodes = [
            ("srv-db", {"label": "DB-Server-Prod", "type": "server", "criticality": "CRITICAL", "capacity": 800}),
            ("core-01", {"label": "Core-Router-01", "type": "core", "criticality": "CRITICAL", "capacity": 1000}),
            ("dist-01", {"label": "Dist-Router-01", "type": "distribution", "criticality": "HIGH", "capacity": 500}),
            ("dist-02", {"label": "Dist-Router-02", "type": "distribution", "criticality": "HIGH", "capacity": 500}),
            ("edge-01", {"label": "Edge-Router-01", "type": "edge", "criticality": "MEDIUM", "capacity": 200}),
            ("edge-02", {"label": "Edge-Router-02", "type": "edge", "criticality": "MEDIUM", "capacity": 200}),
            ("host-01", {"label": "Host-01 (Staff)", "type": "host", "criticality": "LOW", "capacity": 100}),
            ("host-unreg", {"label": "Host-03 (Unregistered)", "type": "host", "criticality": "LOW", "capacity": 100}),
        ]
        
        for node_id, attrs in nodes:
            self.graph.add_node(node_id, **attrs)

        # Edges (Bidirectional infrastructure connections)
        edges = [
            ("srv-db", "core-01", {"bandwidth": 10000}),
            ("core-01", "dist-01", {"bandwidth": 5000}),
            ("core-01", "dist-02", {"bandwidth": 5000}),
            ("dist-01", "edge-01", {"bandwidth": 1000}),
            ("dist-02", "edge-02", {"bandwidth": 1000}),
            ("edge-01", "host-01", {"bandwidth": 1000}),
            ("edge-02", "host-unreg", {"bandwidth": 1000}),
        ]
        
        for u, v, attrs in edges:
            self.graph.add_edge(u, v, **attrs)
            self.graph.add_edge(v, u, **attrs)

    def get_topology_dict(self):
        nodes_data = []
        for n, d in self.graph.nodes(data=True):
            nodes_data.append({"id": n, **d})
        
        edges_data = []
        for u, v, d in self.graph.edges(data=True):
            if u < v: # Avoid visual duplicates in undirected view
                edges_data.append({"from": u, "to": v, **d})
                
        return {"nodes": nodes_data, "edges": edges_data}

    def get_downstream_dependents(self, source_node):
        """Returns all nodes dependent on the given node using directed graph traversal."""
        if source_node not in self.graph:
            return []
        return list(nx.descendants(self.graph, source_node))