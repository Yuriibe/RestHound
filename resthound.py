import argparse
from core.RequestHelper import RequestHelper
from core.ValidationHelper import ValidationHelper
from core.SummaryReporter import SummaryReporter
from rich.console import Console

valid_endpoints_with_methods = []
successful_endpoints = []
origin_header_request = []
fingerprint = []

parser = argparse.ArgumentParser(
    prog='restHound',
    description='REST API Scanner',
)

parser.add_argument('-u', '--url', help="Target base URL or IP")
parser.add_argument('-w', '--wordlist', help="Wordlist with API routes")
parser.add_argument('-o', '--output', help="Save report to file")
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-t', '--thread', help='Amount of threads to be used')

args = parser.parse_args()
console = Console(record=True)

if args.url and args.wordlist:
    if ValidationHelper.is_valid_url(args.url) or ValidationHelper.is_valid_ip(args.url):
        successful_endpoints = RequestHelper.request_wordlist_endpoints(args.wordlist, args.url, args.verbose, console)
        for endpoint in successful_endpoints:
            if args.verbose:
                console.print(f"[cyan][→] Checking:[/] {endpoint}")
            valid_endpoints_with_methods.append(RequestHelper.check_methods(endpoint))
            origin_header_request.append(RequestHelper.request_with_origin_header(endpoint))
            fingerprint.append(RequestHelper.header_fingerprint(endpoint))

        SummaryReporter.print_summary(successful_endpoints, valid_endpoints_with_methods, origin_header_request,
                                      fingerprint, console)

        if args.output:
            console.save_text(args.output)
    else:
        print("please provide valid target")
else:
    if args.url:
        print("please provide wordlist")
    elif args.wordlist:
        print("please provide a target")
    print('please provide valid arguments use -h for help')
