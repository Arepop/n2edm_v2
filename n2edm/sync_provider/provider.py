class SyncProvider:
    def __init__(self):
        self.auth = False
        self.login = None
        self.passwd = None
        self.adress = None

    def connect(self, adress):
        self.address = adress
        #TODO connection to database/server

    def sync(self):
        if not self.auth:
            raise ConnectionError("Could not connect to server")
