from scapy.all import IP, ICMP, sr1, ARP, Ether, srp
import argparse
import socket

def address():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP Address/Adresses.")
    parser.add_argument("-n", "--network", dest="network", nargs="?", const="auto",
                         help="Target network, x.x.x. Omit the value (just pass -n) to auto-detect.")
    parser.add_argument("-r", "--range", dest="iprange",
                        help="Set the range of ip's separated by --> x-x")
    options = parser.parse_args()

    if not options:
        parser.error("[-] Please specify and IP Address or Addresses, use --help for more info.")
    
    return options

def get_local_prefix():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    prefix = ".".join(local_ip.split(".")[:3])

    return prefix

def scan(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=2)
    if resp == None:
        print(f"{ip} is down")
    else:
        print(f"{ip} is up")
        
def scan_network(prefix):
    network = f"{prefix}.0/24"

    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = ARP(pdst=network)
    packet = broadcast / arp_request

    print(f"Scanning network {network}")
    answered, _ = srp(packet, timeout=2, verbose=False)

    print("\n--- Hosts Found ---")
    for sent, received in answered:
        print(f"IP: {received.psrc:<15} |  MAC: {received.hwsrc}")

def scan_range(iprange,prefix):
        start, end = map(int, iprange.split("-"))
        print(start,end)
        print(prefix)
        for i in range(start, end + 1):
            ip = f"{prefix}.{i}"
            scan(ip)

#============================================================================================================

options = address()

if options.target:
    single_output = scan(options.target)
elif options.network:
    prefix = get_local_prefix() if options.network == "auto" else options.network
    network_output = scan_network(prefix)
elif options.iprange:
    prefix = get_local_prefix()
    range_output = scan_range(options.iprange,prefix)