from scapy.all import *

dns_request = DNS(rd=1, qd=DNSQR(qname="servername"))

ip = '172.16.103.118'
roll = 60

ip = IP(dst=ip)
udp = UDP(dport=53)

dns_request_msg = ip/udp/dns_request

dns_response = sr1(dns_request_msg)

packets = [dns_request_msg, dns_response]

wrpcap(f"dns_request_response{roll}.pcap", packets)

print(dns_response[DNS].summary())