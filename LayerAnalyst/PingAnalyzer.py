
from .LayerAnalyzer import LayerAnalyzer
from scapy.all import ICMP, IP, IPv6
from utils.blacklistManager import BlacklistManager as bl
from utils.logsManager import LogsManager
from memory.IPActivityCounter import IPActivityCounter

class PingAnalyzer(LayerAnalyzer):
    data = IPActivityCounter(10,# Seuil,
                            10,# timeoutScan (sec),
                            100) #freqClean (sec) 
    reasonBan = "IPban try to PING"

    @staticmethod
    def analyse(paquet):
        
        print("paquet non ICMP")
        #On verifie si c'est ICMP
        if paquet.haslayer(ICMP):
            print("paquet ICMP")
            #demande de ping : 8
            if paquet[ICMP].type == 8:
                src = "Inconnu"
                if paquet.haslayer(IP):
                    src = paquet[IP].src
                elif paquet.haslayer(IPv6):
                    src = paquet[IPv6].src

                #Verifie IP ban
                if bl.IPisBlacklist(src):
                    print("****************************************************\n")
                    print(f">>> ALLERT {src} try to ping ! IP BAN ! \n")
                    print("****************************************************\n")
                    LogsManager.add(PingAnalyzer.reasonBan,src,None)

                if PingAnalyzer.data.add(src):
                    return True
                else:
                    #La source est détectée comme suspecte, on ban l'ip de l'attaquant 
                    bl.add(src,PingAnalyzer.reasonBan)
                    LogsManager.add(PingAnalyzer.reasonBan,src,None)
                    print(PingAnalyzer.reasonBan)

                    return False
        return True

            