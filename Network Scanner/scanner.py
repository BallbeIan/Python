from scapy.all import IP, ICMP, sr1, ARP, Ether, srp
import argparse
import os
import sys
import socket

def address():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP Address/Adresses.")
    parser.add_argument("-n", "--network", dest="network", nargs="?", const="auto",
                         help="Target network, x.x.x. Omit the value (just pass -n) to auto-detect.")
    parser.add_argument("-r", "--range", dest="range", help="Set the range of ip's separated by - x.x.x.x-x.x.x.x")
    options = parser.parse_args()

    if not options.target and not options.network:
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
    resp = sr1(icmp, timeout=10)
    if resp == None:
        print("Target is down")
    else:
        print("Target is up")
        
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

def scan_range(network):
    

#============================================================================================================

options = address()

if options.target:
    single_output = scan(options.target)
elif options.network:
    prefix = get_local_prefix() if options.network == "auto" else options.network
    network_output = scan_network(prefix)
elif options.range:
    prefix = get_local_prefix()
    range_output = scan_range(prefix)
