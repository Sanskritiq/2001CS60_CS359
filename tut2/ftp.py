from scapy.all import *

ip = '172.16.103.118'
roll = 60


pkt = (IP(dst=dstIP) / TCP(sport=RandShort(),
                            dport=21,flags="S",options=[
                                ('MSS', 1460), ('SAckOK', ''),
                                ('Timestamp', (5693231, 0)),
                                ('NOP', None), ('WScale', 6)
                                ]
                            ))
wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",pkt)
ans=sr1(pkt)
wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",ans,append=True)

sseq=ans.seq
sack=ans.ack

ack=(IP(proto=6, tos=0, dst=dstIP, options='',
        version=4)/TCP(seq=sack, ack=sseq+1, dport=21, flags="A", options=[
            ('NOP', None),
            ('NOP', None),
            ('Timestamp', (981592, 525503134))
            ]))
wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",ack,append=True)
ans=sr1(ack)

# FINI START
fin=(IP(proto=6, tos=0, dst=dstIP, options='',
        version=4)/TCP(dport=21, flags="F", options=[
            ('NOP', None),
            ('NOP', None),
            ('Timestamp', (981592, 525503134))
            ]))
wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",fin)
ans=sr1(fin)
wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",ans, append=True)
ack=(IP(proto=6, tos=0, dst=dstIP, options='',
        version=4)/TCP(dport=21, flags="A", options=[
            ('NOP', None),
            ('NOP', None),
            ('Timestamp', (981592, 525503134))
            ]))
wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",ack, append=True)




