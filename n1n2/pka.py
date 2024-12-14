#pka.py
class PKA:
    def __init__(self):
        self.keys = {}

    def register(self, device_id, public_key):
        self.keys[device_id] = public_key

    def get_public_key(self, device_id):
        return self.keys.get(device_id)