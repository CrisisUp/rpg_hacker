import random
import json
import os
from dataclasses import dataclass
from ui import console

@dataclass
class PhishingOption:
    text: str
    success: bool
    trace: int

@dataclass
class PhishingScenario:
    persona: str
    context: str
    prompt: str
    options: list[PhishingOption]

def _load_phishing_scenarios() -> list[PhishingScenario]:
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base_path, "data", "phishing_scenarios.json")
    
    if not os.path.exists(path):
        return []
        
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    scenarios = []
    for s_data in data:
        options = [PhishingOption(**opt) for opt in s_data.get('options', [])]
        scenario = PhishingScenario(
            persona=s_data.get('persona', ''),
            context=s_data.get('context', ''),
            prompt=s_data.get('prompt', ''),
            options=options
        )
        scenarios.append(scenario)
    return scenarios

def _run_social_engineering_game(hacker):
    scenarios = _load_phishing_scenarios()
    if not scenarios:
        console.error("Falha ao carregar banco de dados de Engenharia Social.")
        return 0

    scenario = random.choice(scenarios)
    console.header("SOCIAL ENGINEERING", scenario.persona)
    console.info(scenario.context)
    print(f"\n[FALA]: \"{scenario.prompt}\"")
    
    for i, option in enumerate(scenario.options):
        print(f" [{i}] {option.text}")
    
    choice_idx = console.ask("Sua escolha: ")
    try:
        selected_option = scenario.options[int(choice_idx)]
        from core.logger import AuditLogger
        AuditLogger.log("PHISHING", f"Alvo: {scenario.persona} | Escolha: {selected_option.text[:30]}...")
        
        if selected_option.success:
            console.success("O alvo caiu na armadilha! Acesso garantido (Bypass Total).")
            hacker.increase_trace(selected_option.trace)
            return 999 # Dano massivo para representar o bypass
        else:
            console.error("O alvo desconfiou! Alerta de segurança emitido.")
            hacker.increase_trace(selected_option.trace * 2)
            hacker.take_damage(30)
            hacker.increase_alert(1)
            return 0
    except:
        console.warning("Hesitação detectada. O alvo encerrou o chat.")
        hacker.increase_trace(15)
        return 0

class BaseEffect:
    def execute(self, hacker, target_node, script):
        console.system(f"[*] Executando: {script.name}")
        hacker.increase_trace(script.trace_impact)
        return script.damage

class ZeroDayEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        console.header("ZERO-DAY EXPLOIT ATIVADO", "EXECUTANDO VULNERABILIDADE DESCONHECIDA")
        hacker.remove_script("zeroday")
        return 999

class PhishingEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        return _run_social_engineering_game(hacker)

class XSSEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        if "Web Server" in target_node.node_type:
            console.success("Payload XSS injetado.")
            target_node.is_xss_active = True
            return 100
        console.error("Apenas para Web Servers!")
        return 0

class OverflowEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        console.warning("!!! EXECUTANDO OVERFLOW !!!")
        target_node.is_corrupted = True
        target_node.data_files = []
        hacker.increase_trace(script.trace_impact)
        return 100

class DecrypterEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        if target_node.is_under_ransomware:
            console.success("Ransomware neutralizado!")
            target_node.ransomware_timer = 0
            return 0
        console.error("Servidor não infectado.")
        return 0

class SupplyChainEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        if "Supplier" in target_node.node_type or "Partner" in target_node.node_type:
            console.success("Backdoor plantado na atualização de software do fornecedor.")
            target_node.is_supply_chain_infected = True
            target_node.backdoor_timer = 4
            return 100 
        console.error("Este script só funciona em alvos externos (Supplier/Partner)!")
        return 0

class RansomwareEffect(BaseEffect):
    def execute(self, hacker, target_node, script):
        if target_node.is_under_ransomware:
            console.error("Servidor já infectado.")
            return 0
        console.header("INICIANDO CRIPTOGRAFIA", "EXTORSÃO EM CURSO")
        console.info("Escolha sua estratégia de extorsão:")
        print(" [1] Extorsão Padrão: Resgate seguro após 5 turnos.")
        print(" [2] Extorsão Dupla: Vazar dados agora (+Créditos), mas dobra o Rastreio.")
        sub_choice = console.ask("Escolha: ")
        
        target_node.ransomware_timer = 5
        hacker.increase_alert(1)
        console.warning("Ataque detectado! Nível de alerta corporativo aumentou (+1).")
        
        if sub_choice == "2":
            gain = random.randint(500, 1000)
            console.warning(f"DADOS VAZADOS! +${gain} imediatos. Equipe de resposta em alerta máximo.")
            hacker.add_credits(gain)
            hacker.increase_trace(40)
            hacker.increase_alert(1)
            console.warning("Vazamento massivo! Nível de alerta corporativo aumentou novamente (+1).")
        
        hacker.increase_trace(script.trace_impact)
        return 100

# Cache de instâncias (Singleton/Registry Pattern)
_EFFECTS_CACHE = {
    "zeroday": ZeroDayEffect(),
    "phishing": PhishingEffect(),
    "xss": XSSEffect(),
    "overflow": OverflowEffect(),
    "decrypter": DecrypterEffect(),
    "supplychain": SupplyChainEffect(),
    "ransomware": RansomwareEffect()
}

_BASE_EFFECT = BaseEffect()

def get_effect(script_id):
    """Retorna a instância em cache do efeito solicitado."""
    return _EFFECTS_CACHE.get(script_id, _BASE_EFFECT)

