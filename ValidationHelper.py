import ipaddress
from urllib.parse import urlparse


class ValidationHelper:
    @staticmethod
    def is_valid_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_url(url):
        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
