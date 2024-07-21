import requests, base64, hashlib, itertools, time, importlib.util, os
from typing import Callable, List, Optional, Dict, Any
from .config import Config

class GDBot:
    def __init__(self, username: str, password: str, lvl: str, config: Optional[Config] = None):
        self.config = config if config else Config()
        self.username = username
        self.password = password
        self.lvl = lvl
        self.accID = self.getID(username)
        self.commands = {}
        self.ready = []
        self.errs = []
        self.banned = []

    def base64_encode(self, s: str) -> str:
        return base64.urlsafe_b64encode(s.encode('utf-8')).decode('utf-8')

    def getID(self, user: str) -> str:
        r = requests.get(f"{self.config.get('gdbrowser')}/api/profile/{user}")
        r.raise_for_status()
        data = r.json()
        if 'accountID' in data:
            return data['accountID']
        else:
            raise ValueError(f"LoginError: User {user} not found")

    def comment(self, msg: str, perc: str = "0") -> requests.Response:
        xor = lambda data, key: ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, itertools.cycle(key)))
        gjp = lambda pw: base64.b64encode(xor(pw, "37526").encode()).decode().replace("+", "-").replace("/", "_")

        def generate_gjp2(password: str = "", salt: str = "mI29fmAnxgTs") -> str:
            password += salt
            return hashlib.sha1(password.encode()).hexdigest()

        def generate_chk(values: List[str], key: str, salt: str) -> str:
            values.append(salt)
            string = "".join(map(str, values))
            return base64.urlsafe_b64encode(xor(hashlib.sha1(string.encode()).hexdigest(), key).encode()).decode()

        data = {
            "gameVersion": self.config.get("gameVersion"),
            "binaryVersion": self.config.get("binaryVersion"),
            "gdw": self.config.get("gdWorld"),
            "accountID": self.accID,
            "userName": self.username,
            "comment": base64.b64encode(msg.encode()).decode(),
            "gjp": gjp(self.password),
            "gjp2": generate_gjp2(self.password),
            "levelID": self.lvl,
            "percent": perc,
            "secret": "Wmfd2893gb7"
        }

        data["chk"] = generate_chk([self.username, base64.b64encode(msg.encode()).decode(), self.lvl, perc], "29481", "0xPT6iUrtws0J")

        proxies = self.config.get("proxy")
        response = requests.post(f"{self.config.get('commentURL')}", data=data, headers={"User-Agent": ""}, proxies=proxies if proxies else None)

        if response.text == "-10" or response.text.startswith("temp_"):
            for callback in self.banned:
                callback(self)

        return response.text

    def command(self, name: str) -> Callable:
        def decorator(func: Callable):
            self.commands[name] = func
            return func
        return decorator

    def on_ready(self, func: Callable[[Any], None]) -> None:
        self.ready.append(func)

    def on_error(self, func: Callable[[Any, Exception], None]) -> None:
        self.errs.append(func)

    def on_banned(self, func: Callable[[Any], None]) -> None:
        self.banned.append(func)

    def load_commands(self, directory: str) -> None:
        for c in os.listdir(directory):
            if c.endswith('.py'):
                spec = importlib.util.spec_from_file_location(c[:-3], os.path.join(directory, c))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr in dir(module):
                    func = getattr(module, attr)
                    if callable(func) and hasattr(func, '__command__'):
                        self.commands[func.__command__] = func

    def run(self):
        for callback in self.ready:
            callback(self)
        while True:
            try:
                proxies = self.config.get("proxy")
                r = requests.get(f"{self.config.get('gdbrowser')}/api/comments/{self.lvl}?count=1", proxies={"http": proxies, "https": proxies} if proxies else None)
                if r.status_code == 200:
                    data = {
                        "comment": r.json()[0].get('content'),
                        "commentID": r.json()[0].get('ID'),
                        "playerID": r.json()[0].get('playerID'),
                        "accountID": r.json()[0].get('accountID'),
                        "levelID": r.json()[0].get('levelID'),
                        "moderator": r.json()[0].get('moderator'),
                        "rank": r.json()[0].get('rank') or "0",
                        "cp": r.json()[0].get('cp') or "0",
                        "moons": r.json()[0].get('moons') or "0",
                        "stars": r.json()[0].get('stars') or "0",
                        "diamonds": r.json()[0].get('diamonds') or "0",
                        "coins": r.json()[0].get('coins') or "0",
                        "userCoins": r.json()[0].get('userCoins') or "0",
                        "demons": r.json()[0].get('demons') or "0",
                        "commentRGB": r.json()[0].get('color'),
                        "username": r.json()[0].get('username')
                    }
                    for cmd, func in self.commands.items():
                        if data.get("comment").startswith(cmd):
                            func(self, data)
            except requests.RequestException as e:
                for callback in self.errs:
                    callback(self, e)
            time.sleep(2)