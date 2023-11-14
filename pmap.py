#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: rxfatalslash

import os
import datetime
import argparse as arg
import socket as soc

def main():
    args = parse_arguments()
    date = datetime.datetime.now().strftime("%Y-%m-%d %X")

    print(f"Escaner de puertos Pmap 1.0 {date}")
    
    if not args.noping:
        if ping(args.target, args.verbose):
            print(f"Informe del escaneo de {args.target}\n")
            print("HOST\t\tESTADO")
            print(f"{args.target}\t\033[1;32mEncendido\033[0;m\n")

            if ping(args.target, args.verbose) and args.ports:
                print("PUERTO\t\tESTADO")
                scan_ports(args.target, args.ports, args.open)
        else:
            print(f"Informe del escaneo de {args.target}\n")
            print("HOST\t\tESTADO")
            print(f"{args.target}\t\033[1;31mDesconectado\033[0;m\n")
    else:
        print(f"Informe del escaneo de {args.target}\n")
        print("HOST\t\tESTADO")
        print(f"{args.target}\t\033[1;32mEncendido\033[0;m\n")
        print("PUERTO\t\tESTADO")
        scan_ports(args.target, args.ports, args.open)

def parse_arguments():
    p = arg.ArgumentParser(description="Escaner de puertos escrito en Python, libre de dependencias externas")
    p.add_argument("-t", "--target", type=str, required=True, help="Dirección IP del objetivo (obligatorio)")
    p.add_argument("-p", "--ports", type=ports, default=[80], help="Puerto/s a escanear, puedes elegir uno o varios puertos separados por comas, o un rango de puertos separados por un guión, ej: (80,90) (100-1024). Por defecto se escaneará el puerto 80 si no se indica ningún puerto")
    p.add_argument("-v", "--verbose", action="store_true", help="Activar verbosidad en la ejecucíon del script")
    p.add_argument("--open", action="store_true", help="Mostrar solo los puertos abiertos")
    p.add_argument("-Pn", "--noping", action="store_true", help="Esta opción omite la comprobación del estado del host mediante el ping, se da por hecho que el host está encendido. Útil para casos en los que el host tiene desactivados los ping pero se sabe que está encendido")

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
        raise arg.ArgumentTypeError(f"Error al analizar los puertos")
    
def scan_ports(target, ports, open):
    for port in ports:
        s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        s.settimeout(1)

        try:
            s.connect((target, port))
            if open:
                print(f"{port}\t\t\033[1;32mAbierto\033[0;m")
            else:
                print(f"{port}\t\t\033[1;32mAbierto\033[0;m")

            s.close()
        except soc.error:
            if not open:
                print(f"{port}\t\t\033[1;31mCerrado\033[0;m")


if __name__ == "__main__":
    main()