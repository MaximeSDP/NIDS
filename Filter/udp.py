from .filter import Filter
from scapy.all import UDP

class UDPFilter(Filter):

    name = "UDP filter ; layer 4"

    @staticmethod
    def help():
        print("tous les paquets de couche 4 ET de type UDP, sont visibles")

    @staticmethod
    def filter(paquet):
        return paquet[UDP] if UDP in paquet else None
