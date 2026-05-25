from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime

def packet_callback(packet):
    if IP in packet:
        timestamp = datetime.now().strftime("%H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        print(f"\n[{timestamp}] {src_ip} -> {dst_ip}")
        
        if TCP in packet:
            print(f"  Protocol: TCP")
            print(f"  Port: {packet[TCP].sport} -> {packet[TCP].dport}")
        elif UDP in packet:
            print(f"  Protocol: UDP")
            print(f"  Port: {packet[UDP].sport} -> {packet[UDP].dport}")
        elif ICMP in packet:
            print(f"  Protocol: ICMP")

def start_sniffer():
    print("=" * 40)
    print("NETWORK SNIFFER STARTED")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    sniff(prn=packet_callback, store=0)

if __name__ == "__main__":
    start_sniffer()

