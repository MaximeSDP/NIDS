import time

class IPActivityCounter: 
    """
    Sauvegarde les ip sources. Detecte si quelqu'un essaie de faire une action + X fois.
    """
    def __init__(self,seuil = 1,timeoutScan = 1, freqClean = 100):
        self.memory = {}
        self.SEUIL= seuil # detection d'une attaque si ca dépasse le seuil
        self.TIMEOUT_SCAN = timeoutScan  # Une attaque doit se faire en moins de Xs
        self.FREQ_CLEAN = freqClean # On nettoie la mémoire tous les X paquets reçus

    def add(self,src_ip):
        if src_ip not in self.memory: #Nouveau
            self.memory[src_ip] = [1,time.time()]
            return True
        else: #Deja present
            current_time = time.time()
            count,start_time = self.memory[src_ip]
            
            if current_time - start_time > self.TIMEOUT_SCAN: # reset si temps écoulé
                self.memory[src_ip] = [1,current_time]
                return True
            else:
                self.memory[src_ip] = [count+1,start_time]
                # Vérification du seuil
                if count + 1 > self.SEUIL:
                    return False

                return True