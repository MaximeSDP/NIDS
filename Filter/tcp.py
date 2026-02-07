from .filter import Filter
from scapy.all import TCP

class TCPFilter(Filter):

    name = "TCP filter ; layer 4"

    @staticmethod
    def help():
        print("tous les paquets de couche 4 ET de type TCP, sont visibles")

    @staticmethod
    def filter(paquet):
        return paquet[TCP] if TCP in paquet else None
