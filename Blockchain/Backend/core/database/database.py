import os 
import json

class BaseDB:
    def __init__(self):
        self.basepath = 'data'
        self.filepath = '/'.join((self.basepath, self.filename))

    def read(self):
        if not os.path.exists(self.filepath):
            print(f"File {self.filepath} does not exist")
            return False
        
        with open(self.filepath, 'r') as f:
            raw = f.readline()
    
        return json.loads(raw) if len(raw) > 0 else []

    def write(self, item):
        data = self.read()

        data = data + item if data else item

        with open(self.filepath, 'w+') as f:
            f.write(json.dumps(data))

class BlockchainDB(BaseDB):
    def __init__(self):
        self.filename = 'blockchain'
        super().__init__()

    def lastBlock(self):
        data = self.read()
        return data[-1] if data else None