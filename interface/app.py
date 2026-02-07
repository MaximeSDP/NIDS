import streamlit as st
import pandas as pd
import plotly.express as px # graphique
import sys
import os
import subprocess
import time
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.blacklistManager import BlacklistManager
from utils.logsManager import LogsManager


def getJsonLogs():
    logs = LogsManager._load(LogsManager.NAME_FILE)
    if not isinstance(logs, list):
        return []
    return logs

def getJsonBlacklist():
    blacklist = BlacklistManager._load(BlacklistManager.NAME_FILE)
    
    return blacklist

def updateJsonPannel(data):
    df = pd.DataFrame(data)
    st.dataframe(df) 

def typeAlertCount():
    logs = getJsonLogs()
    alertCountTmp = {}
    for log in logs:
        if log["typeAlert"] not in alertCountTmp:
            alertCountTmp[log["typeAlert"]] = 1
        else:
            alertCountTmp[log["typeAlert"]] += 1
    types=[]
    count=[]
    for typeA,nb in alertCountTmp.items():
        types.append(typeA)
        count.append(nb)

    alertCount = {
        "type of alert" : types,
        "number of alert" : count
    }
    return alertCount


st.set_page_config(page_title="Mon Dashboard", layout="wide")

#SideBar
st.sidebar.title("Menu")
menuSelection = st.sidebar.selectbox("Choisir une catégorie", ["accueil","Fichier logs", "Fichier BanIP", "Graphique"])
st.title(f"{menuSelection} :")

PID_FILE = os.path.join(os.path.dirname(__file__), '..', 'nids_process.pid')

def is_nids_running():
    """Vérifie si le processus NIDS est en cours d'exécution via un fichier PID."""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, 0) 
            return True, pid
        except (ValueError, OSError, FileNotFoundError):
            # Le processus n'existe plus ou fichier corrompu
            return False, None
    return False, None

#Menu
if menuSelection == "accueil" :
    # Synchronisation de l'état avec la réalité (PID file)
    running, current_pid = is_nids_running()
    st.session_state.launch = running

    logs = getJsonLogs()
    st.write(f"Total Attaque : {len(logs)}")
    
    # Affichage du statut
    if running:
        st.write(f"🟢 **Protection active** (PID: {current_pid})")
    else:
        st.write("🔴 **Protection inactive**")

    if not st.session_state.launch:
        if st.button("Lancer détection paquets :"):
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
            try:
                # Création de fichiers de logs pour el debug
                log_out = open(os.path.join(os.path.dirname(script_path), 'nids.log'), 'w')
                log_err = open(os.path.join(os.path.dirname(script_path), 'nids.err'), 'w')

                # SI on est sur windows on cache l'ouverture de cmd
                creation_flags = 0
                if sys.platform == "win32":
                    creation_flags = subprocess.CREATE_NO_WINDOW

                # Lancement avec redirection et détachement
                proc = subprocess.Popen(
                    [sys.executable, script_path],  #demarrage avec le meme environnement python
                    cwd=os.path.dirname(script_path),
                    stdout=log_out, #les deux sorties couplées au programme
                    stderr=log_err,
                    stdin=subprocess.DEVNULL, # Pour éviter toutes les entrées clavier 
                    creationflags=creation_flags #evite la fenetre windows
                )
                
                # On ferme pour le parent pour laisser ecrire dans les programmes enfants
                log_out.close()
                log_err.close()
                
                # Sauvegarde du PID
                with open(PID_FILE, 'w') as f:
                    f.write(str(proc.pid))
                
                st.session_state.launch = True
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors du lancement : {e}")
        
    else:
        if st.button("STOP !"):
            running, pid = is_nids_running()
            if running and pid:
                try:
                    # Force kill sur Windows pour être sûr 
                    if os.name == 'nt':
                        subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
                    else:
                        os.kill(pid, signal.SIGTERM)
                except Exception as e:
                    st.error(f"Erreur arrêt : {e}")
            
            # Nettoyage fichier PID
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            
            st.session_state.launch = False
            st.rerun()
            
        if st.button("Lancer simulation attaque SYN/PING"):
            attack_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'attack_sim.py'))
            try:
                with st.spinner('Attaque en cours...'):
                    proc = subprocess.Popen([sys.executable, attack_script], cwd=os.path.dirname(attack_script))
                    proc.wait() # Attendre la fin du script d'attaque
                
                st.toast("🚨 Simulation terminée ! Mise à jour...", icon="✅")
                time.sleep(1) # temps pour l'ecriture des logs
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lancement attaque : {e}")
            


elif menuSelection == "Fichier logs":
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear Logs", type="secondary"):
            LogsManager.clear()
            st.success("Logs effacés !")
            st.rerun()
    
    updateJsonPannel(getJsonLogs())

elif menuSelection == "Fichier BanIP":
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear Blacklist", type="secondary"):
            BlacklistManager.clear()
            st.success("Blacklist effacée !")
            st.rerun()
    
    blacklistData = getJsonBlacklist()
    if blacklistData:
        df = pd.DataFrame.from_dict(blacklistData, orient='index', columns=['Raison', 'Date'])
        st.dataframe(df)
    else:
        st.write("Aucune donnée dans la blacklist.")

elif menuSelection == "Graphique":
    st.title("📊 Statistiques Avancées") 

    df = pd.DataFrame(typeAlertCount())
    fig = px.pie(
        df, 
        values='number of alert', 
        names='type of alert', 
        title="Origines des types d'attaques",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, width='stretch') 