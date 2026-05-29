from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

# Inicializa o Console do Rich
console = Console()

def success(message: str):
    console.print(f"[bold green]✔️ [OK][/bold green] {message}")

def error(message: str):
    console.print(f"[bold red]✘ [ERRO][/bold red] {message}")

def info(message: str):
    console.print(f"[bold cyan]ℹ[/bold cyan] {message}")

def warning(message: str):
    console.print(f"[bold yellow]⚠️ [ALERTA][/bold yellow] {message}")

def system(message: str):
    console.print(f"[dim white]» {message}[/dim white]")

def header(title: str, subtitle: str = "OPERACIONAL"):
    """Exibe um cabeçalho estilizado."""
    console.print(
        Panel(
            Text(title.upper(), justify="center", style="bold magenta"),
            subtitle=f"[bold white]{subtitle}[/bold white]",
            box=box.DOUBLE,
            border_style="bright_blue"
        )
    )

def display_status_table(hacker):
    """Mostra o status do jogador em uma tabela elegante."""
    table = Table(box=box.ROUNDED, header_style="bold cyan", expand=True)
    table.add_column("HACKER", style="bold white")
    table.add_column("CONEXÃO", style="bold green")
    table.add_column("RAM", style="bold yellow")
    table.add_column("CRÉDITOS", style="bold gold1")
    
    table.add_row(
        hacker.handle.upper(),
        f"{hacker.connection_stability}%",
        f"{hacker.current_ram}GB / {hacker.max_ram}GB",
        f"${hacker.credits}"
    )
    console.print(table)

def trace_bar(percent: int):
    """Desenha uma barra de rastreio dinâmica."""
    color = "red" if percent > 70 else "yellow" if percent > 40 else "white"
    filled = int(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)
    console.print(f"[bold {color}]RASTREIO: {bar} {percent}%[/bold {color}]")

def ask(prompt: str) -> str:
    """Abstração para entrada de texto do usuário."""
    return console.input(f"\n[bold green]hacker@root:~$[/bold green] {prompt}").strip()

def wait_for_enter(message: str = "Pressione ENTER para continuar..."):
    """Pausa a execução até o usuário pressionar ENTER."""
    console.input(f"\n[dim]{message}[/dim]")

def display_manual():
    """Exibe o manual de ajuda."""
    console.clear()
    header("HACKER'S HANDBOOK", "GUIA DE CAMPO")
    console.print("\n[bold cyan]MODOS ESPECIAIS:[/bold cyan]")
    console.print("  - [white]... :[/] Abre este manual.")
    console.print("  - [bold magenta].... :[/] [RESTRITO] Ativa o Agente Ghost (IA de Auto-Hacking).")
    
    console.print("\n[bold cyan]COMANDOS DISPONÍVEIS:[/bold cyan]")
    console.print("  - [white]Números (0, 1...):[/] Navegar entre servidores.")
    console.print("  - [white]D:[/] Baixar arquivos detectados.")
    console.print("  - [white]B:[/] Acessar a Dark Web (Mercado Negro).")
    console.print("  - [white]S:[/] Ver contratos secundários disponíveis.")
    console.print("  - [white]L:[/] Abrir logs de auditoria.")
    console.print("  - [white]Q:[/] Encerrar conexão.")
    wait_for_enter()

