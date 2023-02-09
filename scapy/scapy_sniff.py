#make sure you have scapy installed!
#packet sniffer using scapy 

from scapy.all import sniff 

def packet_callback(packet):
    print(packet.show())
    
def main():
    sniff(prn=packet_callback, count=1)
    
if __name__ == '__main__':
    main()