from scapy.all import *

# Define the IP address of the target
target_ip = str(socket.gethostbyname('www.adobe.com'))
roll = 60

# Create the ICMP Echo Request packet
ping_request = IP(dst=target_ip)/ICMP()

# Send the packet and receive the response
ping_response = sr1(ping_request, timeout=2)

# Check if a response was received
if ping_response is not None:
    print("Ping response received from", target_ip)
else:
    print("No response received from", target_ip)


wrpcap(f"ping{roll}.pcap", ping_response)

print(f"Saved packets to {os.path.abspath(f'ping{roll}.pcap')}")