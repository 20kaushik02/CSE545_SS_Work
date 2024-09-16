from scapy.all import *

l2=Ether(src='96:e4:fb:1b:7b:fd', dst='cc:cc:cc:cc:cc:cc')
l3=IP(src='10.0.0.2', dst='10.0.0.3')

syn_l4=TCP(sport=31337, dport=31337, seq=31337, ack=31337, flags=0x02)
syn_pkt=l2/l3/syn_l4

ans,unans=srp(syn_pkt, iface='eth0')
print(ans[0].answer[TCP])

ack_l4=TCP(sport=31337, dport=31337, seq=31338, ack=ans[0].answer[TCP].seq + 1, flags=0x10)
ack_pkt=l2/l3/ack_l4

ans,unans=srp(ack_pkt, iface='eth0')
