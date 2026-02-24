# launcher.py
import multiprocessing
import socket
import time
from threading import Thread
from pathlib import Path
import shutil
import sys
import logging
from logging.handlers import RotatingFileHandler

import webview
import uvicorn

import os
import sys

# Asegurar root en path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend import config
from backend import control
from backend import main as backend_main
from frontend import app as frontend_app


def seed_data_if_missing():
    """Si falta la carpeta `data` junto al exe (o en desarrollo), copiarla desde
    la fuente disponible (carpeta `data` del repo o recursos embebidos de PyInstaller).

    Copia únicamente los ficheros que no existan en `config.DATA_DIR`.
    """
    dst = Path(config.DATA_DIR)
    dst.mkdir(parents=True, exist_ok=True)

    # Posibles orígenes de los archivos seed
    src_candidates = []
    if getattr(sys, 'frozen', False):
        # PyInstaller onefile extrae recursos en _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            src_candidates.append(Path(sys._MEIPASS) / 'data')
        # onedir: data puede estar junto al exe
        src_candidates.append(Path(sys.executable).resolve().parent / 'data')
    else:
        # modo desarrollo: carpeta data al lado del script
        src_candidates.append(Path(__file__).resolve().parent / 'data')
        src_candidates.append(Path(__file__).resolve().parent.parent / 'data')

    src = None
    for c in src_candidates:
        if c and c.exists() and c.is_dir():
            src = c
            break

    if not src:
        # No hay carpeta origen; nada que copiar. La inicialización creará archivos vacíos.
        return

    # Copiar sólo archivos inexistentes
    for item in src.iterdir():
        if item.is_file() and item.suffix in ('.parquet', '.csv'):
            target = dst / item.name
            if not target.exists():
                try:
                    shutil.copy2(item, target)
                except Exception:
                    pass

def run_uvicorn():
    cfg = uvicorn.Config(
        backend_main.app,
        host=config.BACKEND_HOST,
        port=int(config.BACKEND_PORT),
        log_level="info",
        reload=False,
    )
    server = uvicorn.Server(cfg)
    server.run()

def run_dash():
    # Ejecuta Dash en su propio puerto; desactivar reloader/debug para producción
    frontend_app.app.run_server(
        host=config.FRONTEND_HOST,
        port=int(config.FRONTEND_PORT),
        debug=False,
        use_reloader=False
    )

def wait_for_server(host, port, timeout=15.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection((host, int(port)), timeout=1)
            s.close()
            return True
        except Exception:
            time.sleep(0.1)
    return False

if __name__ == "__main__":
    multiprocessing.freeze_support()

    # Configurar logging para que los módulos (especialmente el almacenamiento)
    # puedan emitir trazas visibles en consola y fichero durante las pruebas.
    try:
        log_dir = Path(config.DATA_DIR) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root_logger.addHandler(ch)

        # Rotating file handler for detailed debug logs
        fh = RotatingFileHandler(str(log_dir / "agente.log"), maxBytes=1_000_000, backupCount=5, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root_logger.addHandler(fh)

        # Elevar nivel de librerías ruidosas si se desea
        logging.getLogger("uvicorn").setLevel(logging.INFO)
    except Exception:
        # No bloquear el arranque si la configuración de logging falla
        pass

    # Iniciar backend y frontend en hilos (misma instancia, sin procesos hijos)
    control.start_backend()

    t_frontend = Thread(target=run_dash, daemon=True)
    t_frontend.start()

    # Esperar frontend
    frontend_ok = wait_for_server(config.FRONTEND_HOST, config.FRONTEND_PORT, timeout=10)
    url = f"http://{config.FRONTEND_HOST}:{config.FRONTEND_PORT}"
    if not frontend_ok:
        print("Advertencia: la UI no respondió en el puerto esperado, abriendo igualmente...")

    # Abrir ventana nativa (pywebview)
    webview.create_window("Agente Político", url, width=1200, height=800)
    webview.start()