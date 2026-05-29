import random
from entities.network import NetworkNode

def generate_network(nodes_count=18):
    """Gera a rede garantindo a presença de arquivos necessários para a nova campanha."""
    types_pool = ["Web Server", "Email Server", "File Server", "Proxy", "DNS Server"]
    secure_types = ["Firewall", "Database", "Mainframe", "Encrypted Vault"]
    external_types = ["Software Supplier", "IT Partner"]

    gateway = NetworkNode("192.168.0.1", "Gateway Público")
    all_nodes = [gateway]

    # Arquivos obrigatórios da missão na ordem da campanha
    mission_files = [
        "access_logs.txt", 
        "lista_contatos.db", 
        "contas_offshore.enc", 
        "token_acesso_admin.key", 
        "project_alpha.pdf"
    ]
    common_files = ["passwords.txt", "config.old", "backup.zip", "key.pem"]

    for i in range(1, nodes_count):
        ip = f"10.0.1.{i+1}"
        
        # Lógica de tipos de nó
        if i == 1:
            ntype = "Software Supplier"
        elif random.random() < 0.15:
            ntype = random.choice(external_types)
        elif i > nodes_count * 0.7:
            ntype = random.choice(secure_types)
        else:
            ntype = random.choice(types_pool)
            
        new_node = NetworkNode(ip, ntype)
        
        # Distribuição de arquivos de missão específicos para certos tipos de nó
        if mission_files:
            current_target_file = mission_files[0]
            
            # Regras de posicionamento inteligente
            should_place = False
            if current_target_file == "access_logs.txt" and ntype == "Gateway Público":
                should_place = True
            elif current_target_file == "lista_contatos.db" and "Server" in ntype:
                should_place = random.random() < 0.3
            elif current_target_file == "contas_offshore.enc" and ntype == "Database":
                should_place = True
            elif current_target_file == "token_acesso_admin.key" and i > nodes_count * 0.5:
                should_place = random.random() < 0.4
            elif current_target_file == "project_alpha.pdf" and ntype == "Mainframe":
                should_place = True
            
            if should_place:
                new_node.data_files.append(mission_files.pop(0))

        # Distribuição de Fragmentos de Zero-Day e Exploits
        if ntype == "Encrypted Vault":
            if random.random() < 0.10:
                new_node.data_files.append("ZeroDay_Exploit.zip")
            else:
                new_node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
        elif ntype in secure_types and random.random() < 0.40:
            new_node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
        
        # Arquivos comuns
        if random.random() > 0.6:
            new_node.data_files.append(random.choice(common_files))
            
        target_node = random.choice(all_nodes)
        new_node.connect(target_node)
        all_nodes.append(new_node)
        
    # Garante conectividade estratégica para Supply Chain
    suppliers = [n for n in all_nodes if "Supplier" in n.node_type]
    omnicorp_nodes = [n for n in all_nodes if "Supplier" not in n.node_type and n != gateway]
    
    for s in suppliers:
        if omnicorp_nodes:
            targets = random.sample(omnicorp_nodes, min(2, len(omnicorp_nodes)))
            for t in targets:
                s.connect(t)

    return gateway
