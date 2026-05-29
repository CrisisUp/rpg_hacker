import random
from entities.network import NetworkNode

# Constantes para evitar Magic Strings e facilitar a manutenção
TYPES_POOL = ["Web Server", "Email Server", "File Server", "Proxy", "DNS Server"]
SECURE_TYPES = ["Firewall", "Database", "Mainframe", "Encrypted Vault"]
EXTERNAL_TYPES = ["Software Supplier", "IT Partner"]

MISSION_FILES = [
    "access_logs.txt", 
    "lista_contatos.db", 
    "contas_offshore.enc", 
    "token_acesso_admin.key", 
    "project_alpha.pdf"
]

LORE_FILES = [
    "email_estagiario.txt", 
    "aviso_ti.txt", 
    "passwords.txt", 
    "config.old", 
    "architect_legacy.log", 
    "alpha_true_purpose.pdf", 
    "warning_from_past.txt"
]

COMMON_FILES = ["backup.zip", "key.pem", "notes.txt"]


def generate_network(nodes_count=18):
    """Gera a rede orquestrando a criação de nós, distribuição de itens e conexões."""
    gateway = NetworkNode("192.168.0.1", "Gateway Público")
    all_nodes = [gateway]
    
    _place_initial_mission_file(gateway) # Gateway sempre recebe access_logs se disponível
    
    # Cópias locais para podermos dar "pop" durante a geração
    available_mission_files = MISSION_FILES.copy()
    if available_mission_files and available_mission_files[0] == "access_logs.txt":
        available_mission_files.pop(0) # Já colocado no gateway
        
    available_lore_files = LORE_FILES.copy()

    for i in range(1, nodes_count):
        ip = f"10.0.1.{i+1}"
        ntype = _determine_node_type(i, nodes_count)
        new_node = NetworkNode(ip, ntype)
        
        _distribute_mission_files(new_node, i, nodes_count, available_mission_files)
        _distribute_lore_and_loot(new_node, available_lore_files)
        
        # Conecta a um nó existente
        target_node = random.choice(all_nodes)
        new_node.connect(target_node)
        all_nodes.append(new_node)

    _inject_secret_vault(all_nodes)
    _create_supplier_backdoors(all_nodes, gateway)

    return gateway

# --- Funções Auxiliares (SRP) ---

def _determine_node_type(index: int, total_nodes: int) -> str:
    """Determina o tipo do nó baseado na progressão da rede."""
    if index == 1:
        return "Software Supplier"
    elif random.random() < 0.15:
        return random.choice(EXTERNAL_TYPES)
    elif index > total_nodes * 0.7:
        return random.choice(SECURE_TYPES)
    return random.choice(TYPES_POOL)

def _place_initial_mission_file(gateway: NetworkNode):
    """O gateway sempre inicia com o log de acessos."""
    gateway.data_files.append("access_logs.txt")

def _distribute_mission_files(node: NetworkNode, index: int, total_nodes: int, available_missions: list):
    """Lógica de distribuição condicional para arquivos da campanha principal."""
    if not available_missions:
        return

    current_file = available_missions[0]
    should_place = False
    
    # Regras de negócio para colocar arquivos chave
    if current_file == "lista_contatos.db" and "Server" in node.node_type:
        should_place = random.random() < 0.3
    elif current_file == "contas_offshore.enc" and node.node_type == "Database":
        should_place = True
    elif current_file == "token_acesso_admin.key" and index > total_nodes * 0.5:
        should_place = random.random() < 0.4
    elif current_file == "project_alpha.pdf" and node.node_type == "Mainframe":
        should_place = True
        
    if should_place:
        node.data_files.append(available_missions.pop(0))

def _distribute_lore_and_loot(node: NetworkNode, available_lore: list):
    """Espalha arquivos de história, fragmentos e arquivos comuns."""
    # Lore
    if available_lore and random.random() < 0.4:
        lore_idx = random.randint(0, len(available_lore)-1)
        node.data_files.append(available_lore.pop(lore_idx))

    # Fragmentos e Exploits
    if node.node_type == "Encrypted Vault":
        if random.random() < 0.10:
            node.data_files.append("ZeroDay_Exploit.zip")
        else:
            node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
    elif node.node_type in SECURE_TYPES and random.random() < 0.40:
        node.data_files.append(f"vulnerability_fragment_{random.randint(100,999)}.bin")
    
    # Lixo comum / arquivos para vender
    if random.random() > 0.6:
        node.data_files.append(random.choice(COMMON_FILES))

def _inject_secret_vault(all_nodes: list):
    """Cria e anexa o cofre secreto mencionado nos logs narrativos."""
    secret_vault = NetworkNode("10.0.1.254", "Secret Vault")
    secret_vault.data_files.append("ZeroDay_Exploit.zip")
    secret_vault.data_files.append("omnicorp_secrets.db")
    
    secure_nodes = [n for n in all_nodes if n.node_type in SECURE_TYPES]
    if secure_nodes:
        random.choice(secure_nodes).connect(secret_vault)
        all_nodes.append(secret_vault)

def _create_supplier_backdoors(all_nodes: list, gateway: NetworkNode):
    """Garante que fornecedores externos tenham conexões privilegiadas para dentro da rede."""
    suppliers = [n for n in all_nodes if "Supplier" in n.node_type]
    omnicorp_nodes = [n for n in all_nodes if "Supplier" not in n.node_type and n != gateway]
    
    for supplier in suppliers:
        if omnicorp_nodes:
            targets = random.sample(omnicorp_nodes, min(2, len(omnicorp_nodes)))
            for t in targets:
                supplier.connect(t)
