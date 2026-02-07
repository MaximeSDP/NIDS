from scapy.all import sniff, conf
from LayerAnalyst import SynFlagAnalyzer,PingAnalyzer

# Sélection automatique de l'interface utilisée pour aller sur Internet
def get_best_interface():
    return conf.route.route("8.8.8.8")[0]

def analyse_paquet(paquet):
    try:
        print("test")
        for current_strategy in strategies:
            current_strategy.analyse(paquet)
    except Exception as e:
        print("ignore")

active_iface = get_best_interface()
print(f"Interface sélectionnée automatiquement : {active_iface}")

# On définit la stratégie d'analyse 
strategies = [SynFlagAnalyzer,PingAnalyzer]
print("Démarrage du NIDS... (Appuyez sur Ctrl+C pour arrêter)")

try:
    sniff(iface=active_iface, prn=analyse_paquet, store=0)
except Exception as e:
    print(f"Erreur lors du sniffing : {e}")