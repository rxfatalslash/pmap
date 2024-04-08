#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: rxfatalslash

import os, re, sys, signal
from datetime import datetime
import argparse as arg
import socket as soc

FORMAT = "HOST\t\tSTATE"
PF = "PORT\t\tSTATE"

def handler(sig, frame):
    print("\n\nExiting program...")
    sys.exit(0)

def parse_arguments():
    p = arg.ArgumentParser(description="Port scanner, free of external dependencies")
    p.add_argument("-t", "--target", dest="ip", type=host, required=True, help="IP address to scan (required)")
    p.add_argument("-p", "--ports", type=ports, default="1-1000", help="Port/s to scan, you are able to use multiple ports (,), ranges (-) and all ports (_)")
    p.add_argument("-v", "--verbose", action="store_true", help="Activate verbosity")
    p.add_argument("--open", action="store_true", default=True, help="Show only open ports")
    p.add_argument("-Pn", "--noping", action="store_true", help="Skip the ping comprobation")
    p.add_argument("--timeout", type=timeout, default=10, help="Set the timeout in seconds (default: 10 seconds)")
    p.add_argument("-o", "--output", dest="out", help="Store the output in a file")

    return p.parse_args()

def timeout(timeout):
    try:
        if re.search("\d[1-9]?", timeout):
            return int(timeout)
        else:
            print("Introduce an integer as timeout")
            sys.exit(1)
        
    except ValueError:
        raise arg.ArgumentTypeError("Error analyzing timeout")

def ping(ip, verbose, timeout):
    if verbose:
        if timeout:
            r = os.system(f"ping -c 1 {ip} -w {timeout}")
        else:
            r = os.system(f"ping -c 1 {ip}")
    else:
        if timeout:
            r = os.system(f"ping -c 1 {ip} -w {timeout} 1>/dev/null")
        else:
            r = os.system(f"ping -c 1 {ip} 1>/dev/null")

    if r == 0:
        return True
    else:
        return False

def host(ip):
    try:
        if re.search("^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?", ip):
            return ip
        else:
            print("Introduce a valid IP address")
            sys.exit(1)

    except ValueError:
        raise arg.ArgumentTypeError("Error analyzing hosts")

def ports(ports):
    try:
        if "," in ports:
            return [int(port) for port in ports.split(",")]
        elif re.search("^-$", ports):
            return list(range(1, 65536))
        elif "-" in ports:
            start, end = map(int, ports.split("-"))
            return list(range(start, end + 1))
        else:
            return [int(ports)]
    
    except ValueError:
        raise arg.ArgumentTypeError("Error analyzing ports")
    
def scan_ports(ip, ports, open):
    for port in ports:
        s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        s.settimeout(0.01)

        try:
            s.connect((ip, port))
            print(f"{port}\t\t\033[1;32mOpen\033[0;m")

            s.close()
        except soc.error:
            if not open:
                print(f"{port}\t\t\033[1;31mClosed\033[0;m")

def scan_file(ip, ports, open):
    for port in ports:
        s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        s.settimeout(0.01)

        try:
            s.connect((ip, port))
            return f"{port}\t\t\t\tOpen\n"

            s.close()
        except soc.error:
            if not open:
                return f"{port}\t\t\t\tClosed\n"

if __name__ == "__main__":
    args = parse_arguments()
    date = datetime.now().strftime("%Y-%m-%d %X")
    scan = scan_file(args.ip, args.ports, args.open)

    signal.signal(signal.SIGINT, handler)

    print(f"Port scanner Pmap 1.0 {date}")
    
    if not args.noping:
        if not args.out:
            if ping(args.ip, args.verbose, args.timeout):
                print(f"Scan report from {args.ip}\n")
                print(FORMAT)
                print(f"{args.ip}\t\033[1;32mUp\033[0;m\n")

                if ping(args.ip, args.verbose, args.timeout) and args.ports:
                    print(PF)
                    scan_ports(args.ip, args.ports, args.open)
            else:
                print(f"Scan report from {args.ip}\n")
                print(FORMAT)
                print(f"{args.ip}\t\033[1;31mDown\033[0;m\n")
        
        else:
            if ping(args.ip, args.verbose, args.timeout):
                print(f"Scan report from {args.ip}\n")
                print(FORMAT)
                print(f"{args.ip}\t\033[1;32mUp\033[0;m\n")

                if ping(args.ip, args.verbose, args.timeout) and args.ports:
                    print(PF)
                    scan_ports(args.ip, args.ports, args.open)

                    with open(args.out, 'w') as file:
                        file.write(f"Port scanner Pmap 1.0 {date}\n\n")
                        file.write("HOST\t\t\tSTATE\n")
                        file.write(f"{args.ip}\t\tUp\n\n")
                        file.write("PORT\t\t\tSTATE\n")
                        file.write(scan)
                                

    else:
        print(f"Scan report from {args.ip}\n")
        print(FORMAT)
        print(f"{args.ip}\t\033[1;32mUp\033[0;m\n")
        print(PF)
        scan_ports(args.ip, args.ports, args.open)
