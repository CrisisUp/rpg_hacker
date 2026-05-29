from dataclasses import dataclass

@dataclass
class HackingScript:
    """Representa uma ferramenta ou exploit do arsenal do hacker."""
    id: str
    name: str
    ram_cost: int
    damage: int
    trace_impact: int
    price: int
    description: str

    @classmethod
    def from_dict(cls, data: dict):
        """Cria uma instância a partir de um dicionário (útil para o JSON)."""
        return cls(**data)
