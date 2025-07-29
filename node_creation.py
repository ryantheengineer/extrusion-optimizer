import networkx as nx
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
import random

@dataclass
class MedialNode:
    id: int
    position: Tuple[float, float]
    radius: float
    node_type: str  # 'endpoint', 'junction', 'regular'
    constraints: dict = None  # Angle constraints, fixed position, etc.

class MedialAxisGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = {}  # id -> MedialNode
        self.edge_properties = {}  # (id1, id2) -> properties
        
    def add_node(self, node: MedialNode):
        self.nodes[node.id] = node
        self.graph.add_node(node.id, 
                           pos=node.position, 
                           radius=node.radius,
                           type=node.node_type)
    
    def add_edge(self, node1_id: int, node2_id: int, 
                 edge_type: str = 'regular', 
                 angle_constraint: Optional[float] = None):
        self.graph.add_edge(node1_id, node2_id)
        self.edge_properties[(node1_id, node2_id)] = {
            'type': edge_type,
            'angle_constraint': angle_constraint
        }
    
    def get_branches_at_node(self, node_id: int) -> List[int]:
        """Get all connected nodes (branches) at a junction"""
        return list(self.graph.neighbors(node_id))
    
    def validate_topology(self) -> bool:
        """Check if topology is valid for beam structure"""
        # Check for cycles that might cause intersection issues
        cycles = list(nx.simple_cycles(self.graph))
        
        # Validate junction angles
        for node_id in self.graph.nodes():
            if self.nodes[node_id].node_type == 'junction':
                if not self._validate_junction_angles(node_id):
                    return False
        return True
    
    def show_graph(self):
        plt.figure(dpi=300)
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()
        
    
if __name__ == "__main__":
    n = 10
    mindim = -5
    maxdim = 5
    radius = 1
    
    G = MedialAxisGraph()
    # Add nodes
    for i in range(n):
        node = MedialNode(i, [random.randint(mindim, maxdim)], radius, 'regular')
        G.add_node(node)
    
    max_edges = n*3
    n_edges = random.randint(n*2, max_edges)
    for i in range(n_edges):
        node1_id, node2_id = random.sample(sorted(G.nodes),2)
        G.add_edge(node1_id, node2_id)
        
    G.show_graph()