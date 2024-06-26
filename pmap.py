#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: rxfatalslash

import os
import re
from datetime import datetime
import argparse as arg
import socket as soc

def parse_arguments():
    p = arg.ArgumentParser(description="Port scanner, free of external dependencies")
    p.add_argument("-t", "--target", dest="ip", type=host, required=True, help="IP address to scan (required)")
    p.add_argument("-p", "--ports", type=ports, default=[80], help="Port/s to scan, you are able to use multiple ports (,), ranges (-) and all ports (_)")
    p.add_argument("-v", "--verbose", action="store_true", help="Activate verbosity")
    p.add_argument("--open", action="store_true", help="Show only open ports")
    p.add_argument("-Pn", "--noping", action="store_true", help="Skip the ping comprobation")

    return p.parse_args()

def ping(ip, verbose):
    if verbose:
        r = os.system(f"ping -c 1 {ip}")
    else:
        r = os.system(f"ping -c 1 {ip} 1>/dev/null")

    if r == 0:
        return True
    else:
        return False


def host(ip):
    try:
        if re.search(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[1-9][0-9]{1,2})?$", ip):
            return ip
        else:
            print("[\033[1;31mERROR\033[0;m] Introduce a valid IP address")
            exit(1)

    except ValueError:
        raise arg.ArgumentTypeError(f"Error analyzing hosts")


def ports(ports):
    try:
        if "," in ports:
            return [int(port) for port in ports.split(",")]
        elif "-" in ports:
            start, end = map(int, ports.split("-"))
            return list(range(start, end + 1))
        elif "_" in ports:
            return list(range(1, 65536))
        else:
            return [int(ports)]
    
    except ValueError:
        raise arg.ArgumentTypeError(f"Error analyzing ports")
    
def scan_ports(ip, ports, open):
    for port in ports:
        s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        s.settimeout(1)

        try:
            s.connect((ip, port))
            if open:
                print(f"{port}\t\t\033[1;32mOpen\033[0;m")
            else:
                print(f"{port}\t\t\033[1;32mOpen\033[0;m")

            s.close()
        except soc.error:
            if not open:
                print(f"{port}\t\t\033[1;31mClosed\033[0;m")

if __name__ == "__main__":
    args = parse_arguments()
    date = datetime.now().strftime("%Y-%m-%d %X")

    print("\033[1;32m   _ __  _ __ ___   __ _ _ __\033[0;m")
    print("\033[1;32m  | '_ \\| '_ ' _ \\ / _' | '_ \\\033[0;m")
    print("\033[1;32m  | |_) | | | | | | (_| | |_) |\033[0;m")
    print("\033[1;32m  | .__/|_| |_| |_|\\__,_| -__/\033[0;m")
    print("\033[1;32m  | |                   | |\033[0;m")
    print("\033[1;32m  |_|                   |_|\033[0;m\n")
    print("-----------------------------------------")

    print(f"Port scanner Pmap 1.0 {date}")
    
    if not args.noping:
        if ping(args.ip, args.verbose):
            print(f"Scan repot from {args.ip}")
            print("-----------------------------------------\n")
            print("HOST\t\tSTATE")
            print(f"{args.ip}\t\033[1;32mUp\033[0;m\n")

            if ping(args.ip, args.verbose) and args.ports:
                print("PORT\t\tSTATE")
                scan_ports(args.ip, args.ports, args.open)
        else:
            print(f"Scan report from {args.ip}")
            print("-----------------------------------------\n")
            print("HOST\t\tSTATE")
            print(f"{args.ip}\t\033[1;31mDown\033[0;m\n")

    else:
        print(f"Scan report from {args.ip}")
        print("-----------------------------------------\n")
        print("HOST\t\tSTATE")
        print(f"{args.ip}\t\033[1;32mUp\033[0;m\n")
        print("PUERTO\t\tSTATE")
        scan_ports(args.ip, args.ports, args.open)