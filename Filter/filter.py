from abc import ABC, abstractmethod
from scapy.all import Packet

class Filter(ABC):
    
    @property
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        '''Chaque enfant doit définir l'attribut : name'''
        pass
    
    @staticmethod
    @abstractmethod
    def help():
        pass

    @staticmethod
    @abstractmethod
    def filter(paquet: Packet) -> Packet | None:
        pass
