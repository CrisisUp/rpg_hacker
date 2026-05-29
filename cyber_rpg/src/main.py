import sys
import os

# Garante que o Python encontre os módulos na pasta 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game_loop import GameLoop
from ui import console

def main():
    try:
        game = GameLoop()
        game.start()
    except KeyboardInterrupt:
        # Captura o Ctrl+C e fecha o jogo sem o erro de Traceback
        print("\n")
        console.warning("Sessão interrompida pelo usuário.")
        console.system("Limpando rastros e desconectando... Adeus, Hacker.")
        sys.exit(0)
    except Exception as e:
        console.error(f"Ocorreu um erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
