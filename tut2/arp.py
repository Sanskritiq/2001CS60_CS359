from scapy.all import Ether, ARP, wrpcap, srp1
import socket
import sys

ip = '172.16.103.118'
# ip = socket.gethostbyname(ip)

roll = 60
pckt =  Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

wrpcap(f"ARP_request_response_2001CS{roll}.pcap",pckt,append = True)
    
pckt = srp1(pckt,timeout=5,filter="arp")

try:
    wrpcap(f"ARP_request_response_2001CS{roll}.pcap",pckt,append = True)
except:
    print("no packet recieved")
    sys.exit()

