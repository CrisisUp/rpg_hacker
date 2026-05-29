import json
import os
from entities.script import HackingScript

def load_json(file_path):
    """Carrega dados de um arquivo JSON de forma segura."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    full_path = os.path.join(project_root, file_path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return []

def get_all_scripts() -> list[HackingScript]:
    """Retorna uma lista de objetos HackingScript carregados do JSON."""
    data = load_json("data/scripts.json")
    return [HackingScript.from_dict(item) for item in data]

def get_all_missions() -> list:
    """Retorna a lista de missões da história."""
    return load_json("data/missions.json")

def get_bestiary() -> list:
    """Retorna a lista de inimigos (nós de rede)."""
    return load_json("data/bestiario.json")
