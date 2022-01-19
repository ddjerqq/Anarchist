class User:
    def __init__(
        self, 
        _id     : int, 
        _name   : str,
        _amount : int = 0,
        _auth   : str = None,
        _notifications: bool = False
        ) -> None:
        self.id     = _id
        self.name   = _name
        self.amount = _amount
        self.auth   = _auth
        self.notifications = _notifications
    
    @property
    def dict(self) -> dict:
        data = {
            "id"     : self.id,
            "name"   : self.name,
            "amount" : self.amount,
            "auth"   : self.auth,
            "notifications" : self.notifications
        }
        return data
    
    @classmethod
    def from_dict(cls, _dict: dict):
        _id     = _dict["id"]
        _name   = _dict["name"]
        _amount = _dict["amount"]
        try:             _auth = _dict["auth"]
        except KeyError: _auth = "0"
        
        try:             _notifications = _dict["notifications"]    
        except KeyError: _notifications = False
        
        return cls(_id, _name, _amount, _auth, _notifications)

    def __add__(self, amount: int) -> None:
        self.amount += amount

    def __sub__(self, amount: int) -> None:
        if self.amount - amount < 0:
            raise Exception("Amount cannot be negative")
        else:
            self.amount -= amount

    def __str__(self) -> str:
        return f"{self.id} {self.name}"