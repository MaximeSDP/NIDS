
from .LayerAnalyzer import LayerAnalyzer
from scapy.all import conf, IP, IPv6, get_if_addr, get_if_hwaddr
from Filter import TCPFilter
from utils.blacklistManager import BlacklistManager as bl
from utils.logsManager import LogsManager
from memory.IPActivityCounter import IPActivityCounter

# Sélection automatique de l'interface utilisée pour aller sur Internet
def get_best_interface():
    return conf.route.route("8.8.8.8")[0]

def findNameByMAC(mac):
    try:
        nom_machine = conf.manufdb.get(mac)
    except:
        return None
    return nom_machine


class SynFlagAnalyzer(LayerAnalyzer):
    '''
    Verifie si on subit une attaque SYN. Sur plusieurs ports ou un seul
    '''

    active_iface = get_best_interface()
    my_ip = get_if_addr(active_iface)      
    my_mac = get_if_hwaddr(active_iface)   
    #Le temps est long volotairement car la simulation peut etre ralenti du à python. 
    data = IPActivityCounter(10,# Seuil,
                             10,# timeoutScan (sec),
                             100) #freqClean (sec)       
    reasonBan = "IPban try to SYN"                    
    
    @staticmethod
    def analyse(paquet):
        paquetFilter = TCPFilter.filter(paquet)
        if paquetFilter == None:
            return False # pas un paquet TCP

        # Extraction de la source
        src = paquet.src
        if IP in paquet:
            src = paquet[IP].src
        elif IPv6 in paquet:
            src = paquet[IPv6].src

        # SI ce n'est pas un SYN OU c'est nous la source, on s'arrete
        if paquetFilter.flags != "S" or (paquet.src == SynFlagAnalyzer.my_mac or src == SynFlagAnalyzer.my_ip): 
            return False
        
        if bl.IPisBlacklist(src):
            print("****************************************************\n")
            print(f">>> ALLERT demande SYN par {src} ! IP BAN ! \n")
            print("****************************************************\n")
            LogsManager.add(SynFlagAnalyzer.reasonBan,src,paquetFilter.dport)

            return False

        #ajoute l'ip dans les donnés tmp     
        print(f"Test ip {src}") 
        if SynFlagAnalyzer.data.add(src):
                return True
        else:
            #La source est détectée comme suspecte, on ban l'ip de l'attaquant 
            bl.add(src,SynFlagAnalyzer.reasonBan)
            LogsManager.add(SynFlagAnalyzer.reasonBan,src,None)
            print(SynFlagAnalyzer.reasonBan)
            
            return False