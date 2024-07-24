import re
import socket


class Network:
    def __init__(self):
        self.prefix = None
        self.id = None
        self.val = None

        pattern = re.compile(
            r"^(vm)-"
            r"([0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{12})-"
            r"([a-zA-Z0-9]+)-"
            r"[a-zA-Z0-9]+-"
            r"[a-zA-Z0-9]+$"
        )
        match = pattern.match(socket.gethostname())
        if match:
            self.prefix = match.group(1)
            self.id = match.group(2)
            self.val = match.group(3)

    def is_cloud(self):
        return self.prefix is not None and self.id is not None and self.val is not None
