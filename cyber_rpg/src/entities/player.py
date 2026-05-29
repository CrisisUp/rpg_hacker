from core.config import GameConfig
from entities.script import HackingScript

class Player:
    def __init__(self, handle: str):
        self.handle = handle

        # Hardware Resources
        self.max_ram = GameConfig.INITIAL_RAM_GB
        self.current_ram = GameConfig.INITIAL_RAM_GB

        # Integrity & Security
        self.connection_stability = GameConfig.INITIAL_CONNECTION_STABILITY
        self.trace_level = 0

        # Economy & Progression
        self.level = 1
        self.exp = 0
        self.credits = 0
        self.scripts: list[HackingScript] = []
        self.collected_data = []

    def to_dict(self) -> dict:
        """Converte o estado do jogador para um dicionário serializável."""
        return {
            "handle": self.handle,
            "level": self.level,
            "exp": self.exp,
            "credits": self.credits,
            "script_ids": [s.id for s in self.scripts],
            "collected_data": self.collected_data
        }

    def from_dict(self, data: dict, all_available_scripts: list[HackingScript]):
        """Restaura o estado do jogador a partir de um dicionário."""
        self.handle = data.get("handle", self.handle)
        self.level = data.get("level", self.level)
        self.exp = data.get("exp", self.exp)
        self.credits = data.get("credits", self.credits)
        self.collected_data = data.get("collected_data", [])
        
        # Reconecta os objetos de script usando os IDs salvos
        script_ids = data.get("script_ids", [])
        self.scripts = [s for s in all_available_scripts if s.id in script_ids]

    def receive_loot(self, file_name: str, credit_amount: int):
        """Processes collected data and financial rewards."""
        self.collected_data.append(file_name)
        self.add_credits(credit_amount)
        self.add_experience(GameConfig.EXP_GIVEN_PER_FILE_DOWNLOAD)

    def add_credits(self, amount: int):
        self.credits += amount

    def add_experience(self, amount: int):
        self.exp += amount

    def restore_system_resources(self):
        self.current_ram = self.max_ram

    def take_damage(self, amount: int):
        self.connection_stability = max(0, self.connection_stability - amount)

    def use_ram(self, amount: int) -> bool:
        if self.current_ram >= amount:
            self.current_ram -= amount
            return True
        return False

    def increase_trace(self, amount: int):
        self.trace_level = min(GameConfig.TRACE_THRESHOLD_LIMIT, self.trace_level + amount)

    def reduce_trace(self, amount: int):
        self.trace_level = max(0, self.trace_level - amount)

    def __repr__(self):
        return f"[Hacker: {self.handle} | RAM: {self.current_ram}GB | Trace: {self.trace_level}%]"
