#!/usr/bin/python3
from sys import argv, exit, stdin
import socket
import re


Scanner = socket
ips = []


def help():
    print("sipscan.py [OPTIONS] [IPADDRESSES]")
    print("Socket IP Scanner is a tool that takes in ip addresses and can do multiple things, including displaying the hostnames of each ip address, as well as filtering out dead ip addresses and only displaying currently alive ips. as well as identifying ips with their hostname.")
    print("\nOPTIONS:\n")
    print("-a/(-)-alive        Filters only alive ips into list")
    print("-vi/(-)-visual      Gives the visual desplay of results (defualt)")
    print("-f/(-)-file         Imports hosts from file, can only be used once")
    print("-ln/(-)-local       Adds local network addresses to scanner")
    print("-t/(-)-text         Changes the scripts result so that it only displays the ips given. -a and -hn will change these from defualt input")
    print("-hn/(-)-hostname    Addition to -t that includes hostname to raw result")


def cleanips():
    for ipind in range(len(ips)-1, -1, -1):
        # first, im going to expand any ip ranges given. eg "xxx.xxx.xxx.xxx/xx" or "xxx.xxx.xxx.xxx-xxx" to a list of that range.
        if (re.search(
                r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}", ips[ipind]) != None):
            ipaddr, subnet = ips[ipind].split("/")
            # building subnet mask for getting beginning ip
            submask = "1" * int(subnet) + "0" * (32-int(subnet))
            ipmask = ""
            bip = ""
            for i in ipaddr.split("."):
                ipmask += '{0:08b}'.format(int(i))
            # now to build broadcast ip
            for i in range(len(submask)):
                bip += "1" if (submask[i] == "1" and ipmask[i] == "1") else "0"
            bip = str(int(bip[0:8], 2)) + "." + str(int(bip[8:16], 2)) + \
                "." + str(int(bip[16:24], 2)) + \
                "." + str(int(bip[24:32], 2))
            for directAddr in range(int(bip[bip.rfind(".")+1:]), int(bip[bip.rfind(".")+1:]) + 2**(32-int(subnet))):
                ips.append(bip[:bip.rfind(".")+1] + str(directAddr))
            ips.pop(ipind)
        elif (re.search(
                r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}-\d{1,3}", ips[ipind]) != None):
            min, max = ips[ipind].split(".")[-1].split("-")
            for directAddr in range(int(min), int(max)+1):
                ips.append(
                    ips[ipind][: ips[ipind].rfind(".")+1] + str(directAddr))
            ips.pop(ipind)
        elif (re.search(
                r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", ips[ipind]) == None):
            try:
                socket.gethostbyname(ips[ipind])
            except socket.gaierror:
                ips.pop(ipind)
    ips.sort()


def addLocalNetwork():
    # opens a socket on computer to connect to internet
    dnsServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dnsServer.connect(("8.8.8.8", 80))  # Talks to dns provider from google
    localip = dnsServer.getsockname()[0]  # this will get the local ip
    dnsServer.close()  # Turns off socket for possible later use
    for directAddr in range(256):  # 192.168.1.0-255
        ips.append(localip[:localip.rfind(".")+1] + str(directAddr))


def importFromFile(file=""):
    if file == "" and not stdin.isatty():
        ips.extend(stdin.read().split())
    elif file != "":
        ips.extend(open(file, "r").read().split())


def main():
    alive = localnetwork = hostnames = text = False
    visual = True
    earg = ""
    if len(argv) < 1 and stdin.isatty():
        print("Error: no targets given")
        help()
        return
    for i in argv[1:]:
        if earg == "f":
            importFromFile(i)
            continue
        if (i == "-a" or i == "-alive" or i == "--alive"):
            alive = True
        elif (i == "-vi" or i == "-visual" or i == "--visual"):
            visual = True
            text = False
        elif (i == "-t" or i == "-text" or i == "--text"):
            text = True
            visual = False
        elif(i == "-ln" or i == "-local" or i == "--local"):
            localnetwork = True
        elif(i == "-hn" or i == "-hostname" or i == "--hostname"):
            hostnames = False
        elif(i == "-h" or i == "-help" or i == "--help"):
            help()
            return
        elif(i == "-f" or i == "-file" or i == "--file"):
            earg = "f"
        elif(i[0] == "-"):
            print("Error: " + i + " Doesnt exist.")
            help()
            return
        elif(re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.(\d{1,3}/\d{2}|(\d{1,3}-\d{1,3}|\d{1,3}))", i) != None):
            ips.append(i)
        else:
            try:
                socket.gethostbyname(i)
            except socket.gaierror:
                pass
            else:
                ips.append(i)

        importFromFile()  # check to see if given nothing
        if localnetwork:
            addLocalNetwork()

        if len(ips) == 0:
            print("Error: no targets given.")
            help()
            return

        # Generator code
        cleanips()
        if visual:
            if alive:
                print("Alive Hosts:")
                # TODO: setup way to ping hosts
            else:
                print("Hostname (ip address)")
                for ip in ips:
                    try:
                        hostname = Scanner.getfqdn(ip)
                        ipaddr = Scanner.gethostbyname(ip)
                    except:
                        continue
                    else:
                        if hostname != ipaddr:
                            print(hostname + " (" + ipaddr + ")")
        elif text:
            for ip in ips:
                try:
                    hostname = Scanner.getfqdn(ip)
                    ipaddr = Scanner.gethostbyname(ip)
                except:
                    continue
                else:
                    if hostname != ipaddr:
                        if hostnames:
                            print(ipaddr + ":" + hostname)
                        else:
                            print(ipaddr)


if __name__ == "__main__":
    main()
