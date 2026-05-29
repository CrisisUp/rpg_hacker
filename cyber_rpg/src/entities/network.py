class NetworkNode:
    def __init__(self, ip: str, node_type: str):
        self.ip = ip
        self.node_type = node_type
        self.is_hacked = False
        self.is_root = False
        self.is_sniffing = False
        self.is_xss_active = False
        self.is_corrupted = False
        self.is_supply_chain_infected = False # Novo: Indica se o fornecedor foi comprometido
        self.ransomware_timer = 0
        self.backdoor_timer = 0 # Novo: Contador para ativação do backdoor
        self.connections = []
        self.data_files = []

    @property
    def is_under_ransomware(self) -> bool:
        return self.ransomware_timer > 0

    @property
    def has_active_backdoor(self) -> bool:
        return self.backdoor_timer > 0

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)

    def __repr__(self):
        if self.is_corrupted: return f"<Node {self.ip} [DEAD]>"
        if self.is_supply_chain_infected: return f"<Node {self.ip} [INFECTED SUPPLIER]>"
        if self.is_under_ransomware: return f"<Node {self.ip} [RANSOMWARE: {self.ransomware_timer}]>"
        if self.has_active_backdoor: return f"<Node {self.ip} [BACKDOOR: {self.backdoor_timer}]>"
        status = "XSS" if self.is_xss_active else "MITM" if self.is_sniffing else "ROOT" if self.is_root else "USER" if self.is_hacked else "LOCKED"
        return f"<Node {self.ip} [{status}]>"
