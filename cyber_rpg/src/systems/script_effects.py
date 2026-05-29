import random
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

def _run_social_engineering_game(hacker):
    scenarios = [
        PhishingScenario(
            persona="Estagiário de TI (Nervoso)",
            context="O estagiário atendeu o chat de suporte interno.",
            prompt="Oi! Desculpa a demora. Eu não consigo achar o ticket de manutenção do seu servidor. Qual era o código mesmo?",
            options=[
                PhishingOption(text="Diga que é urgente: 'Código 404-X. Se eu não logar agora, o CEO vai me matar!'", success=True, trace=5),
                PhishingOption(text="Seja técnico: 'A porta 8080 está em loop infinito, preciso de acesso root para o kill -9.'", success=False, trace=30),
                PhishingOption(text="Ameace: 'Você é novo? Me passa o acesso ou ligo pro seu supervisor agora!'", success=True, trace=50)
            ]
        ),
        PhishingScenario(
            persona="Analista de RH (Ocupada)",
            context="Você enviou um e-mail falso sobre 'Bônus de Performance'.",
            prompt="Recebi seu e-mail, mas o link está pedindo minha credencial de admin. É seguro?",
            options=[
                PhishingOption(text="Minta com calma: 'Sim, é a nova política de segurança Zero-Trust da empresa.'", success=True, trace=10),
                PhishingOption(text="Pressione: 'O prazo para o bônus acaba em 5 minutos. Você quem sabe.'", success=True, trace=40),
                PhishingOption(text="Ignore e envie outro link: 'Tente este portal alternativo de contingência.'", success=False, trace=60)
            ]
        ),
        PhishingScenario(
            persona="Segurança de Plantão (Cético)",
            context="Você ligou simulando ser da manutenção predial.",
            prompt="Estranho... não recebi nenhum aviso de manutenção no andar 4 hoje.",
            options=[
                PhishingOption(text="Use jargão de infra: 'Houve um vazamento no chiller principal. Se não isolarmos a sala de racks, vai fritar tudo.'", success=True, trace=20),
                PhishingOption(text="Fingir erro: 'Ah, desculpe, deve ser no andar 5 então. Pode conferir pra mim?'", success=False, trace=15),
                PhishingOption(text="Confusão burocrática: 'Verifique a Ordem de Serviço #8829-B no sistema legado.'", success=True, trace=5)
            ]
        )
    ]

    scenario = random.choice(scenarios)
    console.header("SOCIAL ENGINEERING", scenario.persona)
    console.info(scenario.context)
    print(f"\n[FALA]: \"{scenario.prompt}\"")
    
    for i, option in enumerate(scenario.options):
        print(f" [{i}] {option.text}")
    
    choice_idx = console.ask("Sua escolha: ")
    try:
        selected_option = scenario.options[int(choice_idx)]
        if selected_option.success:
            console.success("O alvo caiu na armadilha! Acesso garantido.")
            hacker.increase_trace(selected_option.trace)
            return 100
        else:
            console.error("O alvo desconfiou e bloqueou a tentativa.")
            hacker.increase_trace(selected_option.trace)
            hacker.take_damage(20)
            return 0
    except:
        console.warning("Hesitação detectada. O alvo encerrou o chat.")
        hacker.increase_trace(10)
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

def get_effect(script_id):
    effects_registry = {
        "zeroday": ZeroDayEffect(),
        "phishing": PhishingEffect(),
        "xss": XSSEffect(),
        "overflow": OverflowEffect(),
        "decrypter": DecrypterEffect(),
        "supplychain": SupplyChainEffect(),
        "ransomware": RansomwareEffect()
    }
    return effects_registry.get(script_id, BaseEffect())
