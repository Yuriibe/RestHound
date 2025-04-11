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
                        valid_endpoints.append(api_url)
        print(valid_endpoints)
        return valid_endpoints

    @staticmethod
    def check_methods(url):
        try:
            r = requests.options(url)
            allow = r.headers.get("Allow")
            cors_allow = r.headers.get("Access-Control-Allow-Methods")
            return {
                "url": url,
                "status": r.status_code,
                "allow": allow,
                "cors_allow": cors_allow,
            }
        except Exception as e:
            return e
