#!/usr/bin/python3
from sys import argv, exit, stdin
import socket


Scanner = socket
ips = []


def help():
    print("sipscan.py [OPTIONS] [IPADDRESSES]")
    print("Socket IP Scanner is a tool that takes in ip addresses and can do multiple things, including displaying the hostnames of each ip address, as well as filtering out dead ip addresses and only displaying currently alive ips. as well as identifying ips with their hostname.")
    print("\nOPTIONS:\n")
    print("-a/(-)-alive        Filters only alive ips into list")
    print("-vi/(-)-visual      Gives the visual desplay of results (defualt)")
    print("-r                  Reads ips and assumes hosts are all alive. for incase some ips block ping.")
    print("-f/(-)-file         Imports hosts from file, fan only be used once")
    print("-e/(-)-extra        Adds extra options to nmap scanner")
    print("-ln/(-)-local       Adds local network addresses to scanner")
    print("-t/(-)-text         Changes the scripts result so that it only displays the ips given. -a and -hn will change these from defualt input")
    print("-hn/(-)-hostname    Addition to -t that includes hostname to raw result")

