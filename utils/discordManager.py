import json
import urllib.request
import threading

class DiscordManager:
    WEBHOOK_URLS = {
        "security": "YOUR_SECURITY_WEBHOOK_URL",
        "logs": "YOUR_LOGS_WEBHOOK_URL",
        "general": "YOUR_GENERAL_WEBHOOK_URL"
    }

    @staticmethod
    def send_log(message, channel="logs"):
        """Envoie un message simple au webhook Discord sur le channel Logs (Non bloquant)"""
        threading.Thread(target=DiscordManager._send_async, args=(message, channel)).start()

    @staticmethod
    def _send_async(message, channel):
        url = DiscordManager.WEBHOOK_URLS.get(channel)
        
        if not url in url:
            return

        payload = {
            "content": message
        }
        
        DiscordManager._send(payload, url)

    @staticmethod
    def send_ban_alert(ip, reason, channel="security"):
        threading.Thread(target=DiscordManager._send_ban_async, args=(ip, reason, channel)).start()

    @staticmethod
    def _send_ban_async(ip, reason, channel):
        url = DiscordManager.WEBHOOK_URLS.get(channel)

        if not url in url:
            return

        embed = {
            "title": " NOUVELLE ALERTE DE SÉCURITÉ",
            "description": f"Une IP a été ajoutée à la blacklist.",
            "color": 15158332, # Rouge
            "fields": [
                {
                    "name": "IP Bannis",
                    "value": ip,
                    "inline": True
                },
                {
                    "name": "Raison",
                    "value": reason,
                    "inline": True
                }
            ],
            "footer": {
                "text": "Système de détection d'intrusion"
            }
        }

        payload = {
            "embeds": [embed]
        }
        
        DiscordManager._send(payload, url)

    @staticmethod
    def _send(payload, url):
        """Fonction interne pour envoyer la requête HTTP"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            urllib.request.urlopen(req)
        except Exception:
            pass
