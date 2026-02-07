from scapy.all import Ether, IP, TCP,ICMP, sendp, get_if_hwaddr, get_if_addr, conf
import time

def simulate_attack():

    try:
        iface = conf.route.route("8.8.8.8")[0]
        local_mac = get_if_hwaddr(iface)
        local_ip = get_if_addr(iface)
        
        print(f"Interface d'attaque  : {iface}")
        print(f" (doit correspondre à celle de test.py)")
    except Exception as e:
        print(f"Erreur de détection interface: {e}")
        return

    # Creation de la source
    fake_mac = "00:00:00:00:00:66"  
    fake_ip = "192.168.1.66"        

    print(f"--- SIMULATION D'ATTAQUE SYN ---")
    print(f"Attaquant simulé : IP={fake_ip}, MAC={fake_mac}")
    print(f"Victime (Moi)    : IP={local_ip}, MAC={local_mac}")
    print(f"Envoi de paquets sur 25 ports différents...\n")


    for port in range(3000, 3025):
        packet = Ether(src=fake_mac, dst=local_mac) / \
                 IP(src=fake_ip, dst=local_ip) / \
                 TCP(dport=port, flags="S")

        # Envoi niveau Layer 2 : sendp
        sendp(packet, iface=iface, verbose=0)
        print(f"[+] Paquet SYN envoyé vers le port {port}")
        
        # petite pause, evite le crash
        time.sleep(0.05) 
    
    print("\n--- ATTAQUE SYN TERMINÉE---")
    
    # Creation de la source 2
    fake_mac_2 = "00:00:00:00:00:67"  
    fake_ip_2 = "192.168.1.67"
    
    print(f"\n--- SIMULATION D'ATTAQUE PING (ICMP Flood) ---")
    print(f"Attaquant simulé : IP={fake_ip_2}, MAC={fake_mac_2}")
    
    for i in range(1, 26):
        packet = Ether(src=fake_mac_2, dst=local_mac) / \
                 IP(src=fake_ip_2, dst=local_ip) / \
                 ICMP(type=8)

        sendp(packet, iface=iface, verbose=0)
        print(f"[+] Paquet PING (ICMP Request) n°{i} envoyé")
        time.sleep(0.05)

    print("\n--- ATTAQUE TERMINÉE ---")

if __name__ == "__main__":
    simulate_attack()
