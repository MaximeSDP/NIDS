from abc import ABC, abstractmethod
from scapy.all import Packet

class LayerAnalyzer(ABC):
    
    @staticmethod
    @abstractmethod
    def analyse(paquet: Packet) -> True | False:
        pass
