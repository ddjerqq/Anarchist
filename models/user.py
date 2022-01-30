class User:
    def __init__(self, _id: int, _name: str):
        self.id     = _id
        self.username   = _name
        self.money = 0
        self.authentication   = None
        self.notifications = 0
    
    @property
    def tuple(self) -> tuple:
        return self.id, self.username, self.money, self.authentication, self.notifications
