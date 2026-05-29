import datetime
import os
from ui import console

class AuditLogger:
    """Sistema de log de auditoria para registrar eventos do jogo."""
    
    LOG_FILE = "data/audit.log"
    _session_logs = []

    @classmethod
    def log(cls, event_type: str, description: str, silent: bool = True):
        """Registra um evento no log de auditoria."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{event_type.upper()}] {description}"
        
        # Mantém em memória para a sessão atual
        cls._session_logs.append(log_entry)
        
        # Salva em arquivo
        try:
            os.makedirs(os.path.dirname(cls.LOG_FILE), exist_ok=True)
            with open(cls.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception:
            # Silencioso para não interromper o gameplay
            pass

    @classmethod
    def get_session_logs(cls, limit: int = 10):
        """Retorna os últimos logs da sessão atual."""
        return cls._session_logs[-limit:]

    @classmethod
    def clear_logs(cls):
        """Limpa o arquivo de logs (ex: novo jogo)."""
        if os.path.exists(cls.LOG_FILE):
            try:
                os.remove(cls.LOG_FILE)
            except:
                pass
        cls._session_logs = []

    @classmethod
    def display_logs(cls):
        """Exibe os logs formatados no console."""
        console.header("LOGS DE AUDITORIA DO SISTEMA", "HISTÓRICO DE ACESSO")
        if not cls._session_logs:
            console.info("Nenhum registro encontrado na sessão atual.")
        else:
            for entry in cls._session_logs[-15:]: # Mostra os últimos 15
                console.system(entry)
        console.wait_for_enter()
