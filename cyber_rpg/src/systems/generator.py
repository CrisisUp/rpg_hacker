import random
from entities.network import NetworkNode

def generate_network(nodes_count=12):
    """
    Gera a rede garantindo que arquivos de missões e loot comum existam.
    """
    if nodes_count < 1:
        return None

    types_pool = ["Web Server", "Email Server", "File Server", "Proxy", "DNS Server"]
    secure_types = ["Firewall", "Database", "Mainframe", "Encrypted Vault"]

    # 1. Ponto de Entrada
    gateway = NetworkNode("192.168.0.1", "Gateway Público")
    all_nodes = [gateway]

    # 2. Lista de arquivos importantes para as missões (conforme missions.json)
    mission_files = ["access_logs.txt", "payroll.xlsx", "project_alpha.pdf"]
    common_files = ["passwords.txt", "config.old", "backup.zip", "key.pem", "private_chat.log"]

    # 3. Gerar nós e distribuir arquivos
    for i in range(1, nodes_count):
        ip = f"10.0.1.{i+1}"
        
        # Diferencia tipo por profundidade
        if i > nodes_count * 0.7:
            ntype = random.choice(secure_types)
        else:
            ntype = random.choice(types_pool)
            
        new_node = NetworkNode(ip, ntype)
        
        # Tenta colocar um arquivo de missão se ainda houver, ou um comum
        if mission_files and random.random() > 0.6:
            new_node.data_files.append(mission_files.pop(0))
        elif random.random() > 0.4:
            new_node.data_files.append(random.choice(common_files))
            
        # Conecta a alguém já existente (Grafo Conexo)
        target_node = random.choice(all_nodes)
        new_node.connect(target_node)
        
        all_nodes.append(new_node)

    # Caso algum arquivo de missão tenha sobrado (azar no random), coloca no último nó
    if mission_files:
        for file in mission_files:
            all_nodes[-1].data_files.append(file)

    return gateway
