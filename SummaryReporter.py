class SummaryReporter:

    @staticmethod
    def print_summary(successful_endpoints, valid_endpoints_with_methods, origin_header_request, fingerprint):
        print("\n" + "=" * 60)
        print("✅ Reachable Endpoints:")
        print("=" * 60)
        for url in successful_endpoints:
            print(f"- {url}")

        print("\n" + "=" * 60)
        print("🔍 Valid Endpoints with Allowed Methods:")
        print("=" * 60)
        for item in valid_endpoints_with_methods:
            url = item.get("url")
            status = item.get("status")
            allow = item.get("allow") or item.get("cors_allow") or "N/A"
            print(f"[{status}] {url} → Methods: {allow}")

        print("\n" + "=" * 60)
        print("🚨 CORS Reflection Check:")
        print("=" * 60)
        for cors in origin_header_request:
            url = cors.get("url")
            origin = cors.get("reflected_origin")
            creds = cors.get("allow_credentials")
            if origin == "https://evil.com" and creds == "true":
                print(f"[!] Potential CORS vuln: {url}")
                print(f"    ↳ Access-Control-Allow-Origin: {origin}")
                print(f"    ↳ Access-Control-Allow-Credentials: {creds}")
            else:
                print(f"[✓] Safe: {url}")

        print("\n" + "=" * 60)
        print("🧬 Header Fingerprint Summary")
        print("=" * 60)

        header_fields = [
            ("Server", "server"),
            ("X-Powered-By", "x_powered_by"),
            ("X-Generator", "x_generator"),
            ("X-Runtime", "x_runtime"),
            ("Via", "via"),
        ]

        for cors in fingerprint:
            print(f"  {cors.get('url')}")
            for label, key in header_fields:
                value = cors.get(key)
                if value:
                    print(f"    ↳ {label}: {value}")
