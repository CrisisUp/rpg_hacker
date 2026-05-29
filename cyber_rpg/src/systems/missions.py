from systems.loader import get_all_missions

class MissionManager:
    """
    Gerencia o ciclo de vida das missões da história.
    Suporta ramificações e escolhas narrativas.
    """
    def __init__(self):
        self.all_missions = get_all_missions()
        self.active_mission = self.all_missions[0] if self.all_missions else None
        self.is_story_complete = False
        self.pending_choice = False

    def check_objective(self, player_collected_files: list) -> dict:
        """
        Verifica se o jogador coletou o arquivo necessário.
        Se houver ramificação, marca como pendente de escolha.
        """
        if not self.active_mission or self.is_story_complete or self.pending_choice:
            return None

        target_file = self.active_mission.get('required_file')
        
        if target_file in player_collected_files:
            completed = self.active_mission
            next_ids = self.active_mission.get('next_missions', [])
            
            if len(next_ids) > 1:
                self.pending_choice = True
            elif len(next_ids) == 1:
                self.select_mission(next_ids[0])
            else:
                self.active_mission = None
                self.is_story_complete = True
                
            return completed
            
        return None

    def get_available_choices(self) -> list:
        """Retorna os objetos das missões disponíveis para escolha."""
        if not self.active_mission: return []
        next_ids = self.active_mission.get('next_missions', [])
        return [m for m in self.all_missions if m['id'] in next_ids]

    def select_mission(self, mission_id: str):
        """Define a próxima missão ativa a partir da escolha do jogador."""
        self.active_mission = next((m for m in self.all_missions if m['id'] == mission_id), None)
        self.pending_choice = False
        if not self.active_mission:
            self.is_story_complete = True

    @property
    def current_title(self) -> str:
        return self.active_mission['title'] if self.active_mission else "SISTEMA LIVRE"

    @property
    def current_description(self) -> str:
        if self.is_story_complete:
            return "Todos os objetivos da OmniCorp foram neutralizados."
        return self.active_mission['description'] if self.active_mission else "Nenhum objetivo pendente."
