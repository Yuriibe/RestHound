import argparse
import requests
from ValidationHelper import ValidationHelper

helper = ValidationHelper()

parser = argparse.ArgumentParser(
    prog='restHound',
    description='REST API Scanner',
)

parser.add_argument('-u', '--url')
parser.add_argument('-w', '--wordlist')

args = parser.parse_args()
if args.url and args.wordlist:
    print(args.url, args.wordlist)
    if ValidationHelper.is_valid_url(args.url) or ValidationHelper.is_valid_ip(args.url):
        print("123")
else:
    if args.url:
        print("please provide wordlist")
    elif args.wordlist:
        print("please provide valid target")
