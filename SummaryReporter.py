from rich.console import Console
from rich.pretty import pprint


class SummaryReporter:

    @staticmethod
    def print_ascii_banner():

        print(r"""
          _____           _   _    _                       _ 
         |  __ \         | | | |  | |                     | |
         | |__) |___  ___| |_| |__| | ___  _   _ _ __   __| |
         |  _  // _ \/ __| __|  __  |/ _ \| | | | '_ \ / _` |
         | | \ \  __/\__ \ |_| |  | | (_) | |_| | | | | (_| |
         |_|  \_\___||___/\__|_|  |_|\___/ \__,_|_| |_|\__,_|

        """)

    @staticmethod
    def show_reachable_endpoints(endpoints, console):
        console.print("\n[bold green]✅ Reachable Endpoints[/]")
        console.print("=" * 60)
        for url in endpoints:
            console.print(f"- {url}")

    @staticmethod
    def show_methods(endpoints, console):
        console.print("\n[bold blue]🔍 Valid Endpoints with Allowed Methods:[/]")
        console.print("=" * 60)
        for item in endpoints:
            url = item.get("url")
            status = item.get("status")
            allow = item.get("allow") or item.get("cors_allow") or "N/A"
            console.print(f"[{status}] {url} → Methods: {allow}")

    @staticmethod
    def show_cors_checks(cors_results, console):
        console.print("\n[bold red]🚨 CORS Reflection Check:[/]")
        console.print("=" * 60)
        for cors in cors_results:
            url = cors.get("url")
            origin = cors.get("reflected_origin")
            creds = cors.get("allow_credentials")
            if origin == "https://evil.com" and creds == "true":
                console.print(f"[red][!] Potential CORS vuln: {url}")
                console.print(f"    ↳ Access-Control-Allow-Origin: {origin}")
                console.print(f"    ↳ Access-Control-Allow-Credentials: {creds}")
            else:
                console.print(f"[green][✓] Safe: {url}")

    @staticmethod
    def show_header_fingerprint(fingerprint, console):
        console.print("\n[bold cyan]🧬 Header Fingerprint Summary[/]")
        console.print("=" * 60)
        header_fields = [
            ("Server", "server"),
            ("X-Powered-By", "x_powered_by"),
            ("X-Generator", "x_generator"),
            ("X-Runtime", "x_runtime"),
            ("Via", "via"),
        ]
        for cors in fingerprint:
            console.print(f"  {cors.get('url')}")
            for label, key in header_fields:
                value = cors.get(key)
                if value:
                    console.print(f"    ↳ {label}: {value}")

    @staticmethod
    def print_summary(successful_endpoints, valid_endpoints_with_methods, origin_header_request, fingerprint):
        SummaryReporter.print_ascii_banner()
        console = Console()
        SummaryReporter.show_reachable_endpoints(successful_endpoints, console)
        SummaryReporter.show_methods(valid_endpoints_with_methods, console)
        SummaryReporter.show_cors_checks(origin_header_request, console)
        SummaryReporter.show_header_fingerprint(fingerprint, console)
