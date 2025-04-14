import argparse
from core.RequestHelper import RequestHelper
from core.ValidationHelper import ValidationHelper
from core.SummaryReporter import SummaryReporter
from rich.console import Console
import threading
import queue

valid_endpoints_with_methods = []
successful_endpoints = []
origin_header_request = []
fingerprint = []

# Locks for thread-safe access
lock = threading.Lock()

parser = argparse.ArgumentParser(
    prog='restHound',
    description='REST API Scanner',
)

parser.add_argument('-u', '--url', help="Target base URL or IP")
parser.add_argument('-w', '--wordlist', help="Wordlist with API routes")
parser.add_argument('-o', '--output', help="Save report to file")
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-t', '--thread', type=int, default=4, help='Amount of threads to be used (default=4)')

args = parser.parse_args()
console = Console(record=True)

q = queue.Queue()


def scan_worker():
    while not q.empty():
        try:
            queue_endpoint = q.get()
            full_url = RequestHelper.request_endpoint_from_wordlist(queue_endpoint, args.url, args.verbose, console)
            if full_url:
                with lock:
                    successful_endpoints.append(full_url)
            q.task_done()
        except Exception as e:
            if args.verbose:
                console.print(f"[red][!] Error:[/] {e}")
            q.task_done()


def post_process_worker():
    while True:
        try:
            endpoint = post_q.get(timeout=1)
        except queue.Empty:
            break

        if args.verbose:
            console.print(f"[cyan][→] Checking:[/] {endpoint}")

        with lock:
            valid_endpoints_with_methods.append(RequestHelper.check_methods(endpoint))
            origin_header_request.append(RequestHelper.request_with_origin_header(endpoint))
            fingerprint.append(RequestHelper.header_fingerprint(endpoint))
        post_q.task_done()


if args.url and args.wordlist:

    if args.thread < 1:
        print("Thread count must be at least 1.")
        exit(1)

    if ValidationHelper.is_valid_url(args.url) or ValidationHelper.is_valid_ip(args.url):

        with open(args.wordlist, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    q.put(line)

        # Start scanning threads
        threads = []
        for _ in range(args.thread):
            t = threading.Thread(target=scan_worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # do post-processing with threads
        post_q = queue.Queue()
        for endpoint in successful_endpoints:
            post_q.put(endpoint)

        post_threads = []
        for _ in range(args.thread):
            t = threading.Thread(target=post_process_worker)
            t.start()
            post_threads.append(t)

        for t in post_threads:
            t.join()

        SummaryReporter.print_summary(
            successful_endpoints,
            valid_endpoints_with_methods,
            origin_header_request,
            fingerprint,
            console
        )

        if args.output:
            console.save_text(args.output)

    else:
        print("Please provide a valid target (URL or IP).")
else:
    if args.url and not args.wordlist:
        print("Please provide a wordlist.")
    elif args.wordlist and not args.url:
        print("Please provide a target.")
    else:
        print('Please provide valid arguments. Use -h for help.')
