class NetworkNode:
    def __init__(self, ip: str, node_type: str):
        self.ip = ip
        self.node_type = node_type
        self.is_hacked = False
        self.is_root = False
        self.is_sniffing = False
        self.is_xss_active = False
        self.is_corrupted = False
        self.ransomware_timer = 0 # Novo: Contador para destruição total se infectado
        self.connections = []
        self.data_files = []

    @property
    def is_under_ransomware(self) -> bool:
        return self.ransomware_timer > 0

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)

    def __repr__(self):
        if self.is_corrupted: return f"<Node {self.ip} [DEAD]>"
        if self.is_under_ransomware: return f"<Node {self.ip} [RANSOMWARE: {self.ransomware_timer}]>"
        status = "XSS" if self.is_xss_active else "MITM" if self.is_sniffing else "ROOT" if self.is_root else "USER" if self.is_hacked else "LOCKED"
        return f"<Node {self.ip} [{status}]>"
