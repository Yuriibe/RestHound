import argparse
from RequestHelper import RequestHelper
from ValidationHelper import ValidationHelper
from SummaryReporter import SummaryReporter

valid_endpoints_with_methods = []
successful_endpoints = []
origin_header_request = []
fingerprint = []
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
            origin_header_request.append(RequestHelper.request_with_origin_header(endpoints))
            fingerprint.append(RequestHelper.header_fingerprint(endpoints))
        SummaryReporter.print_summary(successful_endpoints, valid_endpoints_with_methods, origin_header_request,
                                      fingerprint)
    else:
        print("please provide valid target")
else:
    if args.url:
        print("please provide wordlist")
    elif args.wordlist:
        print("please provide a target")
