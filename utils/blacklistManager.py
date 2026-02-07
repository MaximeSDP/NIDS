from datetime import datetime
from .jsonManager import JsonManager
from .discordManager import DiscordManager

class BlacklistManager(JsonManager):
    NAME_FILE = "../data/blacklist.json"
    @staticmethod
    def add(ip, reason):
        data = JsonManager._load(BlacklistManager.NAME_FILE)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Structure : {ip : [raison, date]}
        data[ip] = [reason, date_str]
        JsonManager._save(BlacklistManager.NAME_FILE,data)
        print(f"[Blacklist] IP {ip} ajoutée. Raison: {reason}")
        DiscordManager.send_ban_alert(ip, reason)

    @staticmethod
    def remove(ip):
        data = JsonManager._load(BlacklistManager.NAME_FILE)
        if ip in data:
            del data[ip]
            JsonManager._save(BlacklistManager.NAME_FILE,data)
            print(f"[Blacklist] IP {ip} retirée.")
        else:
            print(f"[Blacklist] L'IP {ip} n'était pas blacklistée.")

    @staticmethod
    def IPisBlacklist(IP):
        data = JsonManager._load(BlacklistManager.NAME_FILE)
        if IP in data:
            return True
        else:
            return False