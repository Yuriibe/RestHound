import requests


class RequestHelper:

    @staticmethod
    def request_wordlist_endpoints(wordlist, url) -> list:
        valid_endpoints = []
        with open(wordlist, "r") as file:
            for line in file:
                entry = line.strip()
                if entry:
                    api_url = url + "/" + entry
                    response = requests.get(api_url)
                    if response.status_code != 404:
                        print(api_url)
                        valid_endpoints.append(api_url)
        return valid_endpoints

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
        print(response)
        return {
            "url": url,
            "server": response.headers.get("Server"),
            "x_powered_by": response.headers.get("X-Powered-By"),
        }