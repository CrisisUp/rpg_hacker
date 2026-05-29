import random
from entities.network import NetworkNode

def generate_network(nodes_count=15):
    """Gera a rede incluindo nós de fornecedores externos, alvos OmniCorp e fragmentos de Zero-Day."""
    types_pool = ["Web Server", "Email Server", "File Server", "Proxy", "DNS Server"]
    secure_types = ["Firewall", "Database", "Mainframe", "Encrypted Vault"]
    external_types = ["Software Supplier", "IT Partner"]

    gateway = NetworkNode("192.168.0.1", "Gateway Público")
    all_nodes = [gateway]

    mission_files = ["access_logs.txt", "payroll.xlsx", "project_alpha.pdf"]
    common_files = ["passwords.txt", "config.old", "backup.zip", "key.pem"]

    for i in range(1, nodes_count):
        ip = f"10.0.1.{i+1}"
        
        # Garantir pelo menos um Software Supplier
        if i == 1:
            ntype = "Software Supplier"
        elif random.random() < 0.15:
            ntype = random.choice(external_types)
        elif i > nodes_count * 0.7:
            ntype = random.choice(secure_types)
        else:
            ntype = random.choice(types_pool)
            
        new_node = NetworkNode(ip, ntype)
        
        # Distribuição de Fragmentos de Zero-Day e Exploits
        if ntype == "Encrypted Vault":
            if random.random() < 0.10: # 10% de chance de Zero-Day completo em Vaults
                new_node.data_files.append("ZeroDay_Exploit.zip")
            else:
                new_node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
        elif ntype in secure_types and random.random() < 0.40: # 40% em outros nós seguros
            new_node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
        
        if mission_files and random.random() > 0.6:
            new_node.data_files.append(mission_files.pop(0))
        elif random.random() > 0.4:
            new_node.data_files.append(random.choice(common_files))
            
        target_node = random.choice(all_nodes)
        new_node.connect(target_node)
        all_nodes.append(new_node)
        
    suppliers = [n for n in all_nodes if "Supplier" in n.node_type]
    omnicorp_nodes = [n for n in all_nodes if "Supplier" not in n.node_type and n != gateway]
    
    for s in suppliers:
        if omnicorp_nodes:
            targets = random.sample(omnicorp_nodes, min(2, len(omnicorp_nodes)))
            for t in targets:
                s.connect(t)

    return gateway
