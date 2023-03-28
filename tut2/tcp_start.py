from scapy.all import *

ip = str(socket.gethostbyname('www.adobe.com'))
roll = 60

dst_ip = ip
dst_port = 80

syn_packet = IP(dst=dst_ip)/TCP(dport=dst_port, flags="S")

syn_response = sr1(syn_packet)

seq_num = syn_response[TCP].ack
ack_num = syn_response[TCP].seq + 1

ack_packet = IP(dst=dst_ip)/TCP(dport=dst_port, flags="A", seq=seq_num, ack=ack_num)

wrpcap(f"tcp_handshake{roll}.pcap", [syn_packet, syn_response, ack_packet])

send(ack_packet)
