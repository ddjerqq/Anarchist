class User:
    def __init__(self,
                 snowflake: int,
                 name: str,
                 money: int = 0,
                 authentication: str = None,
                 notifications: int = 0) -> None:
        self.id = snowflake
        self.username = name
        self.money = money
        self.authentication = authentication
        self.notifications = notifications

    @staticmethod
    def from_id(user_id: int, db) -> "User":
        return db[user_id]

    @property
    def to_db(self) -> tuple:
        return self.id, self.username, self.money, self.authentication, self.notifications

    @staticmethod
    def from_db(user_tuple) -> "User":
        return User(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3], user_tuple[4])

    def __str__(self) -> str:
        return f"{self.username} ({self.id}) <{self.money}>"

    def __del__(self) -> None:
        del self.id
        del self.username
        del self.money
        del self.authentication
        del self.notifications
