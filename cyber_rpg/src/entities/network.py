class NetworkNode:
    def __init__(self, ip, node_type):
        self.ip = ip
        self.node_type = node_type
        self.is_hacked = False
        self.connections = []
        self.data_files = [] # Arquivos que podem ser roubados

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)

    def __repr__(self):
        return f"<Node {self.ip} ({self.node_type})>"
