import json
import os

def _get_path(relative_path):
    """Retorna o caminho absoluto para um arquivo dentro da pasta cyber_rpg."""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

def get_all_missions():
    path = _get_path("data/missions.json")
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_scripts():
    path = _get_path("data/scripts.json")
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        from entities.script import HackingScript
        return [HackingScript.from_dict(s) for s in json.load(f)]

def get_lore_data():
    """Carrega as informações de lore (logs e e-mails)."""
    path = _get_path("data/lore.json")
    if not os.path.exists(path): return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_emails():
    """Carrega os e-mails do contratante."""
    path = _get_path("data/emails.json")
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
