import ipaddress
from urllib.parse import urlparse


class ValidationHelper:
    @staticmethod
    def is_valid_ip(ip) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_url(url) -> bool:
        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
