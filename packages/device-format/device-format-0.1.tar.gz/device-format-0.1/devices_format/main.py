import re

formats = {
    "OLT": r"^[A-Z][A-Z]F-([A-Z0-9]{10}|[A-Z0-9]{10}-[1-9]{1})$",
    "OTB": r"^CA2-[A-Z0-9]{10}-[A-Z]{1,2}[0-9]{1,2}-T[0-9]{1,2}$",
    "CA1": r"^CA1-[A-Z0-9]{10}-[A-Z]{1,2}$",
    "CA2": r"^CA2-[A-Z0-9]{10}-[A-Z]{1,2}[0-9]{1,2}$",
    "FTSBS": r"^P[0-9]{1,2}-[A-Z0-9]{8,10}$",
    "CPE": r"^P[0-9]{1,2}-[A-Za-z0-9\-]+$",
}


class Device:
    def __init__(self, device_name, device_type) -> None:
        self.device_name = device_name
        self.device_type = str(device_type).upper()

    def get_device_format(self):
        if not formats.get(self.device_type):
            return False
        if self.device_type not in formats.keys():
            return False
        result = re.fullmatch(formats.get(self.device_type), self.device_name)
        if result is not None:
            return True
        return False
