import hashlib
import json
import time


__version__ = '0.0.0'


class BlockIntegrityError(ValueError):
    pass


class Block(object):
    hashfunc = hashlib.sha256

    @staticmethod
    def get_current_timestamp():
        r = 10 ** 6
        return int(time.time() * r)

    def __init__(self, payload, index=0, timestamp=None, hash_prev=None):
        if hash_prev is None:
            hash_prev = self.hashfunc().hexdigest()
        if timestamp is None:
            timestamp = self.get_current_timestamp()
        self.index = index
        self.payload = payload
        self.timestamp = timestamp
        self.hash_prev = hash_prev
        self.hash_this = self.calc_hash()

    def serialize(self):
        return json.dumps(vars(self))

    @classmethod
    def deserialize(cls, json_string):
        d = json.loads(json_string)
        params = {
            'index': d['index'],
            'payload': d['payload'],
            'timestamp': d['timestamp'],
            'hash_prev': d['hash_prev'],
        }
        block = cls(**params)
        if block.hash_this != d['hash_this']:
            raise BlockIntegrityError

    def calc_hash(self):
        s = '{}{}{}{}'.format(
            self.index,
            self.payload,
            self.timestamp,
            self.hash_prev,
        )
        return self.hashfunc(s.encode()).hexdigest()

    def extend(self, payload):
        cls = self.__class__
        index = self.index + 1
        return cls(payload, index=index, hash_prev=self.hash_this)


class BlockChain(object):
    pass
