import random
from entities.network import NetworkNode

def generate_network(nodes_count=12):
    """Gera a rede incluindo nós de fornecedores externos."""
    types_pool = ["Web Server", "Email Server", "File Server", "Proxy", "DNS Server"]
    secure_types = ["Firewall", "Database", "Mainframe", "Encrypted Vault"]
    external_types = ["Supplier Server", "Partner Gateway"]

    gateway = NetworkNode("192.168.0.1", "Gateway Público")
    all_nodes = [gateway]

    mission_files = ["access_logs.txt", "payroll.xlsx", "project_alpha.pdf"]
    common_files = ["passwords.txt", "config.old", "backup.zip", "key.pem"]

    for i in range(1, nodes_count):
        ip = f"10.0.1.{i+1}"
        
        # Chance de ser um fornecedor externo
        if random.random() < 0.15:
            ntype = random.choice(external_types)
        elif i > nodes_count * 0.7:
            ntype = random.choice(secure_types)
        else:
            ntype = random.choice(types_pool)
            
        new_node = NetworkNode(ip, ntype)
        
        if ntype == "Encrypted Vault" and random.random() < 0.02:
            new_node.data_files.append("ZeroDay_Exploit.zip")
        elif mission_files and random.random() > 0.6:
            new_node.data_files.append(mission_files.pop(0))
        elif random.random() > 0.4:
            new_node.data_files.append(random.choice(common_files))
            
        target_node = random.choice(all_nodes)
        new_node.connect(target_node)
        all_nodes.append(new_node)

    return gateway
