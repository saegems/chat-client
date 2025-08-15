import socket


def ip_to_int(ip):
    """Convert an IPv4 address to a 32-bit integer."""
    try:
        octets = ip.split(".")
        if len(octets) != 4:
            raise ValueError("Invalid IP address format")
        octets = [int(octet) for octet in octets]
        ip_int = (octets[0] * 256**3) + (octets[1] *
                                         256**2) + (octets[2] * 256) + octets[3]
        return ip_int
    except (ValueError, AttributeError):
        return 2130706433  # 127 * 256^3 + 0 * 256^2 + 0 * 256 + 1


def get_local_ip():
    '''Get the local ip address of the user's PC'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip_to_int(ip)
    except Exception:
        return ip_to_int("127.0.0.1")
