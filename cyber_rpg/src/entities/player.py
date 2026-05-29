from core.config import GameConfig
from entities.script import HackingScript

class Player:
    def __init__(self, handle: str):
        self.handle = handle
        self.max_ram = GameConfig.INITIAL_RAM_GB
        self.current_ram = GameConfig.INITIAL_RAM_GB
        self.connection_stability = GameConfig.INITIAL_CONNECTION_STABILITY
        self.trace_level = 0
        self.level = 1
        self.exp = 0
        self.credits = 0
        self.vulnerability_fragments = 0 # Novo: Fragmentos para compilar Zero-Day
        self.scripts: list[HackingScript] = []
        self.collected_data = []

    def to_dict(self) -> dict:
        return {
            "handle": self.handle,
            "level": self.level,
            "exp": self.exp,
            "credits": self.credits,
            "vulnerability_fragments": self.vulnerability_fragments,
            "script_ids": [s.id for s in self.scripts],
            "collected_data": self.collected_data
        }

    def from_dict(self, data: dict, all_available_scripts: list[HackingScript]):
        self.handle = data.get("handle", self.handle)
        self.level = data.get("level", self.level)
        self.exp = data.get("exp", self.exp)
        self.credits = data.get("credits", self.credits)
        self.vulnerability_fragments = data.get("vulnerability_fragments", 0)
        self.collected_data = data.get("collected_data", [])
        script_ids = data.get("script_ids", [])
        self.scripts = [s for s in all_available_scripts if s.id in script_ids]

    def receive_loot(self, file_name: str, credit_amount: int):
        self.collected_data.append(file_name)
        self.add_credits(credit_amount)
        self.exp += GameConfig.EXP_GIVEN_PER_FILE_DOWNLOAD

    def add_script(self, script: HackingScript):
        """Adiciona um novo script ao arsenal se ele ainda não existir."""
        if script.id not in [s.id for s in self.scripts]:
            self.scripts.append(script)

    def remove_script(self, script_id: str):
        """Remove um script do arsenal (usado para consumíveis como Zero-Day)."""
        self.scripts = [s for s in self.scripts if s.id != script_id]

    def add_credits(self, amount: int):
        self.credits += amount

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
        return f"[Hacker: {self.handle} | RAM: {self.current_ram}GB | Trace: {self.trace_level}% | Fragments: {self.vulnerability_fragments}/5]"
