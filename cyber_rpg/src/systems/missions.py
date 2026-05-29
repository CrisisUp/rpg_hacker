from systems.loader import get_all_missions

class MissionManager:
    """
    Gerencia o ciclo de vida das missões da história e contratos secundários.
    """
    def __init__(self):
        all_data = get_all_missions()
        self.main_missions = [m for m in all_data if m.get('type') == 'main']
        self.side_missions_pool = [m for m in all_data if m.get('type') == 'side']
        
        self.active_mission = self.main_missions[0] if self.main_missions else None
        self.active_side_missions = []
        self.available_side_missions = self.side_missions_pool[:]
        
        self.is_story_complete = False
        self.pending_choice = False

    def check_objective(self, player_collected_files: list) -> dict:
        """
        Verifica se o jogador coletou o arquivo necessário para a missão principal 
        ou para qualquer missão secundária ativa.
        """
        # 1. Verifica Missões Secundárias Primeiro (podem ser múltiplas)
        for side in list(self.active_side_missions):
            if side.get('required_file') in player_collected_files:
                self.active_side_missions.remove(side)
                return side # Retorna a missão secundária concluída

        # 2. Verifica Missão Principal
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
        """Retorna as opções de ramificação da história principal."""
        if not self.active_mission: return []
        next_ids = self.active_mission.get('next_missions', [])
        return [m for m in self.main_missions if m['id'] in next_ids]

    def select_mission(self, mission_id: str):
        """Define a próxima missão principal ativa."""
        self.active_mission = next((m for m in self.main_missions if m['id'] == mission_id), None)
        self.pending_choice = False
        if not self.active_mission:
            self.is_story_complete = True

    def accept_side_mission(self, mission_id: str) -> bool:
        """Adiciona uma missão secundária à lista de ativos."""
        mission = next((m for m in self.available_side_missions if m['id'] == mission_id), None)
        if mission and mission not in self.active_side_missions:
            self.active_side_missions.append(mission)
            self.available_side_missions.remove(mission)
            return True
        return False

    @property
    def current_title(self) -> str:
        title = self.active_mission['title'] if self.active_mission else "SISTEMA LIVRE"
        if self.active_side_missions:
            title += f" (+{len(self.active_side_missions)} Side)"
        return title

    @property
    def current_description(self) -> str:
        desc = ""
        if self.is_story_complete:
            desc = "Objetivos da OmniCorp neutralizados."
        elif self.active_mission:
            desc = self.active_mission['description']
        
        if self.active_side_missions:
            desc += "\n\n[ATIVOS SECUNDÁRIOS]:"
            for s in self.active_side_missions:
                desc += f"\n- {s['title']}: {s['required_file']}"
        return desc
