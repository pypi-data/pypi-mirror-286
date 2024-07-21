class Config:
    def __init__(self, **kwargs):
        self.config = kwargs
        self.config.setdefault('gdbrowser', 'https://gdbrowser.com/')
        self.config.setdefault('commentURL', 'http://www.boomlings.com/database/uploadGJComment21.php')
        self.config.setdefault('gameVersion', '22')
        self.config.setdefault('binaryVersion', '42')
        self.config.setdefault('gdWorld', '0')

    def get(self, key: str, default=None):
        return self.config.get(key, default)