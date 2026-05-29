class NetworkNode:
    def __init__(self, ip: str, node_type: str):
        self.ip = ip
        self.node_type = node_type
        self.is_hacked = False
        self.is_root = False # Novo: Define se o hacker tem privilégios administrativos
        self.connections = []
        self.data_files = []

    def connect(self, other_node):
        """Cria um link de rede bidirecional sem duplicatas."""
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)

    def __repr__(self):
        status = "ROOT" if self.is_root else "USER" if self.is_hacked else "LOCKED"
        return f"<Node {self.ip} [{status}]>"
