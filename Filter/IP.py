from .filter import Filter
from scapy.all import IP,IPv6

class IPFilter(Filter):

    name = "IP filter ; layer 3"

    @staticmethod
    def help():
        print("tous les paquets de couche 3 sont visibles")

    @staticmethod
    def filter(paquet):
        if IP in paquet:
            return paquet[IP]
        if IPv6 in paquet:
            return paquet[IPv6]
        return None
