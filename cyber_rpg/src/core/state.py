import json
import os
from ui import console

class StateManager:
    """Gerencia a persistência do progresso do jogador em disco."""
    
    SAVE_FILE = "data/savegame.json"

    @classmethod
    def save_exists(cls) -> bool:
        """Verifica se existe um arquivo de save."""
        return os.path.exists(cls.SAVE_FILE)

    @classmethod
    def save_game(cls, player_data: dict):
        """Salva os dados do jogador em um arquivo JSON."""
        try:
            # Garante que a pasta data existe
            os.makedirs(os.path.dirname(cls.SAVE_FILE), exist_ok=True)
            
            with open(cls.SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, indent=4)
            console.system("Progresso sincronizado com o storage local.")
        except Exception as e:
            console.error(f"Falha ao salvar progresso: {e}")

    @classmethod
    def load_game(cls) -> dict:
        """Carrega os dados do arquivo de save."""
        if not cls.save_exists():
            return None
        
        try:
            with open(cls.SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.error(f"Erro ao ler arquivo de save: {e}")
            return None

    @classmethod
    def delete_save(cls):
        """Remove o arquivo de save (útil para Game Over definitivo)."""
        if cls.save_exists():
            os.remove(cls.SAVE_FILE)
