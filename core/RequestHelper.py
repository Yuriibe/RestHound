import requests


class RequestHelper:

    @staticmethod
    def request_endpoint_from_wordlist(endpoint, url, verbose, console) -> str:
        api_url = url + "/" + endpoint
        response = requests.get(api_url)
        if verbose:
            console.print(f"[green][✓] {api_url} → {response.status_code} [/]")
        if response.status_code != 404:
            return api_url

    @staticmethod
    def check_methods(url):
        try:
            response = requests.options(url)
            allow = response.headers.get("Allow")
            cors_allow = response.headers.get("Access-Control-Allow-Methods")
            return {
                "url": url,
                "status": response.status_code,
                "allow": allow,
                "cors_allow": cors_allow,
            }
        except Exception as e:
            return e

    @staticmethod
    def request_with_origin_header(url):
        headers = {
            "Origin": "https://evil.com"
        }
        try:
            response = requests.get(url, headers=headers)
            return {
                "url": url,
                "status": response.status_code,
                "reflected_origin": response.headers.get("Access-Control-Allow-Origin"),
                "allow_credentials": response.headers.get("Access-Control-Allow-Credentials"),
            }
        except Exception as e:
            return e

    @staticmethod
    def header_fingerprint(url):
        response = requests.options(url)
        return {
            "url": url,
            "server": response.headers.get("Server", None),  # Web server (nginx, Apache, etc.)
            "x_powered_by": response.headers.get("X-Powered-By", None),  # Framework (Express, PHP, etc.)
            "x_generator": response.headers.get("X-Generator", None),  # CMS platforms (WordPress, Joomla)
            "x_runtime": response.headers.get("X-Runtime", None),  # Rails, Flask, Laravel
            "via": response.headers.get("Via", None),  # Proxy/CDN info
        }
