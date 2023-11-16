#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: rxfatalslash

import os
import re
from datetime import datetime
import argparse as arg
import socket as soc

def main():
    args = parse_arguments()
    date = datetime.now().strftime("%Y-%m-%d %X")

    print(f"Port scanner Pmap 1.0 {date}")
    
    if not args.noping:
        if not args.out:
            if ping(args.target, args.verbose):
                print(f"Scan repot from {args.target}\n")
                print("HOST\t\tSTATE")
                print(f"{args.target}\t\033[1;32mUp\033[0;m\n")

                if ping(args.target, args.verbose) and args.ports:
                    print("PORT\t\tSTATE")
                    scan_ports(args.target, args.ports, args.open)
            else:
                print(f"Scan report from {args.target}\n")
                print("HOST\t\tSTATE")
                print(f"{args.target}\t\033[1;31mDown\033[0;m\n")

        else:
            if ping(args.target, args.verbose):
                os.system(f"echo 'Scan report from {args.target}\n\nHOST\t\t\tSTATE\n{args.target}\tUp\n' > {args.out}")

                if ping(args.target, args.verbose) and args.ports:
                    os.system(f"echo 'PORT\t\t\tSTATE\n{scan_ports(args.target, args.ports, args.open)}\n' >> {args.out}")

            else:
                os.system(f"echo 'Scan report from {args.target}\n\nHOST\t\t\tSTATE\n{args.target}\tDown\n' > {args.out}")
    else:
        print(f"Scan report from {args.target}\n")
        print("HOST\t\tSTATE")
        print(f"{args.target}\t\033[1;32mUp\033[0;m\n")
        print("PUERTO\t\tSTATE")
        scan_ports(args.target, args.ports, args.open)

def parse_arguments():
    p = arg.ArgumentParser(description="Port scanner, free of external dependencies")
    p.add_argument("-t", "--target", type=host, required=True, help="IP address to scan (required)")
    p.add_argument("-p", "--ports", type=ports, default=[80], help="Port/s to scan, you are able to use multiple ports (,) and ranges (-)")
    p.add_argument("-v", "--verbose", action="store_true", help="Activate verbosity")
    p.add_argument("--open", action="store_true", help="Show only open ports")
    p.add_argument("-Pn", "--noping", action="store_true", help="Skip the ping comprobation")
    p.add_argument("-o", "--output", dest="out", nargs="?", help="Store the output in a file")

    return p.parse_args()

def ping(target, verbose):
    if verbose:
        r = os.system(f"ping -c 1 {target}")
    else:
        r = os.system(f"ping -c 1 {target} 1>/dev/null")

    if r == 0:
        return True
    else:
        return False


def host(targets):
    try:
        if re.search("^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[1-9][0-9]{1,2})?$", targets):
            if "/" in targets:
                hm = targets.split("/")[0]
                h = hm.split(".")
                if int(h[3]) == 0:
                    h[3] = list(range(1, 256))
                    return ".".join(map(str, h))
                else:
                    return ".".join(h)
            else:
                return targets
        else:
            print("Introduce a valid IP address")

    except ValueError:
        raise arg.ArgumentTypeError(f"Error analyzing hosts")


def ports(ports):
    try:
        if "," in ports:
            return [int(port) for port in ports.split(",")]
        elif "-" in ports:
            start, end = map(int, ports.split("-"))
            return list(range(start, end + 1))
        else:
            return [int(ports)]
    
    except ValueError:
        raise arg.ArgumentTypeError(f"Error analyzing ports")
    
def scan_ports(target, ports, open):
    for port in ports:
        s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        s.settimeout(1)

        try:
            s.connect((target, port))
            if open:
                print(f"{port}\t\t\033[1;32mOpen\033[0;m")
            else:
                print(f"{port}\t\t\033[1;32mOpen\033[0;m")

            s.close()
        except soc.error:
            if not open:
                print(f"{port}\t\t\033[1;31mClosed\033[0;m")


if __name__ == "__main__":
    main()