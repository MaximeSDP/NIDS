from datetime import datetime
from .jsonManager import JsonManager
from .discordManager import DiscordManager

class LogsManager(JsonManager):
    NAME_FILE = "../data/logs.json"
    @staticmethod
    def add(typeAlert,srcIP,targetport):
        data = JsonManager._load(LogsManager.NAME_FILE)
        if not isinstance(data, list):
            data = []
            
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = {
            "timestamp" : date_str,
            "typeAlert" : typeAlert,
            "srcIP" : srcIP,
            "ports" : targetport
        }
        data.append(entry)
        
        JsonManager._save(LogsManager.NAME_FILE,data)

        #Envoie message discord
        message = f"[Logs] IP {srcIP} ajoutée. Raison: {typeAlert}"
        DiscordManager.send_log(message) 
        print(message)

    @staticmethod
    def remove(srcIP):
        data = JsonManager._load(LogsManager.NAME_FILE)
        if isinstance(data, list):
            new_data = [log for log in data if log.get("srcIP") != srcIP]
            if len(new_data) != len(data):
                JsonManager._save(LogsManager.NAME_FILE, new_data)
                print(f"[Logs] Logs pour l'IP {srcIP} retirés.")
            else:
                print(f"[Logs] Aucun log trouvé pour l'IP {srcIP}.")
        else:
            print(f"[Logs] Le fichier de logs est vide ou invalide.")

