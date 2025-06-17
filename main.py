import subprocess
import uvicorn
import os
import time
import requests
import sys
import shutil
from multiprocessing import Process

from env_config import EnvConfig

def run_uvicorn():
    uvicorn.run("rest.api:rest_api", host=EnvConfig.get_api_host(), port=EnvConfig.get_api_port_int())

def run_streamlit():
    home_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_app/Home.py'))
    if not os.path.exists(home_py_path):
        raise FileNotFoundError(f"❌ Fichier introuvable : {home_py_path}")

    streamlit_executable = shutil.which("streamlit")
    if not streamlit_executable:
        possible_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "streamlit.exe")
        if os.path.exists(possible_path):
            streamlit_executable = possible_path
        else:
            raise FileNotFoundError(
                "❌ Impossible de trouver l'exécutable 'streamlit'. Vérifie ton environnement virtuel ou le PATH.")
    if not streamlit_executable:
        raise FileNotFoundError("❌ Impossible de trouver l'exécutable 'streamlit'. Assure-toi qu'il est installé et dans le PATH.")

    subprocess.run([streamlit_executable, "run", home_py_path])

def run_graphql_server():
    from interface.graphql.server import app
    app.run(debug=True, port=5050, use_reloader=False)

def wait_for_graphql(host="localhost", port=5050, timeout=10):
    url = f"http://{host}:{port}/graphql"
    for _ in range(timeout * 2):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("✅ GraphQL server is up.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    raise RuntimeError("❌ GraphQL server did not start in time.")

if __name__ == "__main__":
    p1 = Process(target=run_uvicorn)
    p3 = Process(target=run_graphql_server)

    p1.start()
    p3.start()

    wait_for_graphql()

    p2 = Process(target=run_streamlit)
    p2.start()

    p1.join()
    p2.join()
    p3.join()
