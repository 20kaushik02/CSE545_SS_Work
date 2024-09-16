#!/opt/pwn.college/python

from scapy.utils import rdpcap
from scapy.packet import Raw

pcap_path = "/home/hacker/my_pcaps/3.06.pcap"
pcap_file = rdpcap(pcap_path)

result = ""
alternate=True
for pkt in pcap_file:
	try:
		if alternate:
			result += pkt[Raw].load.decode()
		alternate = not alternate
	except:
		pass

print(result)