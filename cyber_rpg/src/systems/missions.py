from systems.loader import get_all_missions

class MissionManager:
    """
    Gerencia o ciclo de vida das missões da história.
    Responsável por validar objetivos e prover recompensas.
    """
    def __init__(self):
        self.all_missions = get_all_missions()
        self.active_mission = self.all_missions[0] if self.all_missions else None
        self.is_story_complete = False

    def check_objective(self, player_collected_files: list) -> dict:
        """
        Verifica se o jogador coletou o arquivo necessário.
        Retorna a missão concluída se houver sucesso, senão None.
        """
        if not self.active_mission or self.is_story_complete:
            return None

        target_file = self.active_mission.get('required_file')
        
        if target_file in player_collected_files:
            completed = self.active_mission
            self._advance_to_next()
            return completed
            
        return None

    def _advance_to_next(self):
        """Move o ponteiro da história para a próxima missão."""
        next_id = self.active_mission.get('next_mission')
        
        if next_id:
            self.active_mission = next((m for m in self.all_missions if m['id'] == next_id), None)
        else:
            self.active_mission = None
            self.is_story_complete = True

    @property
    def current_title(self) -> str:
        return self.active_mission['title'] if self.active_mission else "SISTEMA LIVRE"

    @property
    def current_description(self) -> str:
        if self.is_story_complete:
            return "Todos os objetivos da OmniCorp foram neutralizados."
        return self.active_mission['description'] if self.active_mission else "Nenhum objetivo pendente."
