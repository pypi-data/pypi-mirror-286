from . import dns
from . import cloudflare

import argparse
import os

def check_env():
    if os.environ.get("IGN8_DNS_TYPE") == None:
        print("IGN8_DNS_TYPE not set")
        exit(1)
    if os.environ.get("IGN8_DNS_URL") == None:
        print("IGN8_DNS_URL not set")
        exit(1)
    if os.environ.get("IGN8_DNS_TOKEN") == None:
        print("IGN8_DNS_TOKEN not set")
        exit(1)
    if os.environ.get("IGN8_DNS_DOMAIN") == None:
        print("IGN8_DNS_DOMAIN not set")
        exit(1)
    if os.environ.get("IGN8_DNS_PROVIDER") == None:
        print("IGN8_DNS_PROVIDER not set")
        exit(1)
    if os.environ.get("IGN8_DNS_ZONEID") == None:
        print("IGN8_DNS_ZONEID not set")
        exit(1)
    if os.environ.get("IGN8_DNS_RECORD_NAME") == None:
        print("IGN8_DNS_RECORD_NAME not set")
        exit(1)
    if os.environ.get("IGN8_DNS_RECORD_CONTENT") == None:
        print("IGN8_DNS_RECORD_CONTENT not set")
        exit(1)
    if os.environ.get("IGN8_DNS_RECORD_TTL") == None:
        os.environ.setdefault("IGN8_DNS_RECORD_TTL", "300")
    if os.environ.get("IGN8_DNS_RECORD_TYPE") == None:
        os.environ.setdefault("IGN8_DNS_RECORD_TYPE", "A")
    if os.environ.get("IGN8_DNS_RECORD_PROXIED") == None:
        os.environ.setdefault("IGN8_DNS_RECORD_PROXIED", False )
    return True



def main():
    parser = argparse.ArgumentParser(description="Keep ign8 and automate", usage="ign8_dns <action> \n\n\
\
               version : 0.9.15 \n\
               actions:\n\
               envcheck            check if env is set \n\
               setenv              set env \n\
               list                list dns records \n\
               sync                sync dns record\n\
               libvirt             create dns records for virtlib\n\
               libvirt_leases      create dns records for virtlib\n\
               register            register dns record for this host\n\
               save_secret         Save a secret as tst record\n\
               load_secret         load a secret from tst record\n\
               delete_secret       delete a secret as tst record\n\
               generate_key        generate key for shared encryption\n\
\n\
               2023 Knowit Miracle\n\
               ")
    
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    if args.action[0] == "sync":
        print("sync dns")
        dns.sync_dns(args)
        
    if args.action[0] == "envcheck":
        print("env check")
        dns.env_check()

    if args.action[0] == "setenv":
        print("set env")
        dns.set_env()
    
    if args.action[0] == "libvirt_leases":
        print("set env")
        dns.libvirt_leases()

    if args.action[0] == "virtlightning":
        print("set env")
        dns.virtlightning()

    if args.action[0] == "libvirt":
        print("set env")
        dns.libvirt(args)

    if args.action[0] == "register":
        dns.register()


    if args.action[0] == "default":
        print("set env")
        dns.default(args)

    if args.action[0] == "clean":
        dns.clean(args)

    if args.action[0] == "cloudflare":
        cloudflare.check_access()
        
    if args.action[0] == "list":
        if(cloudflare.check_access()):
            print(cloudflare.list_dns())
            return True
        
    if args.action[0] == "add_record":
        if check_env():
          if(cloudflare.check_access()):
            cloudflare.add_record()   
            return True
    
    if args.action[0] == "save_secret":
        cloudflare.save_secret(args.action[1], args.action[2])   
          
    if args.action[0] == "delete_secret":
        cloudflare.delete_secret(args.action[1])   
          
    if args.action[0] == "load_secret":
        cloudflare.load_secret(args.action[1])   

    if args.action[0] == "generate_key":
        cloudflare.generate_key()   

    





