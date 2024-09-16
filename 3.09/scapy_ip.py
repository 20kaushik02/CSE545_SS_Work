from scapy.all import *

l2=Ether(src='86:22:3f:d1:20:b5', dst='cc:cc:cc:cc:cc:cc')
l3=IP(src='10.0.0.2', dst='10.0.0.3', proto=0xFF)
pkt=l2/l3

ans, unans=srp(pkt, iface='eth0')
