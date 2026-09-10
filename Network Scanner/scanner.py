from scapy.all import IP, ICMP, sr1, ARP, Ether, srp
import argparse
import os
import sys
import socket

def address():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP Address/Adresses.")
    parser.add_argument("-n", "--network", dest="network", help="Target network, x.x.x")
    options = parser.parse_args()

    if not options.target and not options.network:
        parser.error("[-] Please specify and IP Address or Addresses, use --help for more info.")
    return options

def scan(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=10)
    if resp == None:
        print("Target is down")
    else:
        print("Target is up")
        
def scan_network(prefix):
    range = f"{prefix}.0/24"

    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = ARP(pdst=range)
    packet = broadcast / arp_request

    print(f"Scanning range {range}")
    answered, _ = srp(packet, timeout=2, verbose=False, iface="Ethernet 3")

    print("\n--- Active Hosts Found ---")
    for sent, received in answered:
        print(f"IP: {received.psrc:<15} |  MAC: {received.hwsrc}")

options = address()

if options.target:
    single_output = scan(options.target)
elif options.network:
    network_output = scan_network(options.network)