from .filter import Filter
from scapy.all import Ether

class EtherFilter(Filter):

    name = "Ether filter ; layer 2"

    @staticmethod
    def help():
        print("tous les paquets de couche 2 sont visibles")

    @staticmethod
    def filter(paquet):
        return paquet[Ether] if Ether in paquet else None
