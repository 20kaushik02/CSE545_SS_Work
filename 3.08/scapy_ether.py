from scapy.all import *

l2=Ether(src='a6:cb:ec:88:05:5e', dst='cc:cc:cc:cc:cc:cc', type=0xFFFF)
pkt=l2

ans, unans=srp(pkt, iface='eth0')
