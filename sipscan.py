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
