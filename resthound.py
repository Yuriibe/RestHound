import argparse
from RequestHelper import RequestHelper
from ValidationHelper import ValidationHelper

valid_endpoints_with_methods = []
successful_endpoints = []

parser = argparse.ArgumentParser(
    prog='restHound',
    description='REST API Scanner',
)

parser.add_argument('-u', '--url')
parser.add_argument('-w', '--wordlist')

args = parser.parse_args()

if args.url and args.wordlist:
    if ValidationHelper.is_valid_url(args.url) or ValidationHelper.is_valid_ip(args.url):
        successful_endpoints = RequestHelper.request_wordlist_endpoints(args.wordlist, args.url)
        for endpoints in successful_endpoints:
            valid_endpoints_with_methods.append(RequestHelper.check_methods(endpoints))
        print(valid_endpoints_with_methods)
    else:
        print("please provide valid target")
else:
    if args.url:
        print("please provide wordlist")
    elif args.wordlist:
        print("please provide a target")
