import time

class User:
    def __init__( self, name: str, id: int) -> None:
        self._signup_time = time.time()

        self.name   = name
        self.id     = id

        self.bank   = 0.0
        self.wallet = 0.0
        self.items  = []

        self.last_work_time = time.localtime(315770570)

    @property
    def dict(self) -> dict:
        return {
            "_signup_time"   : self._signup_time,
            "name"           : self.name,
            "id"             : self.id,
            "bank"           : self.bank,
            "wallet"         : self.wallet,
            "items"          : self.items,
            "last_work_time" : self.last_work_time
        }
    
    @property
    def csv(self) -> str:
        return f"{ self.id },{ self.name },{ self.wallet },{ self.bank },{ self._signup_time },{ self.items },{ self.wallet },{ self.last_work_time.tm_wday }/{ self.last_work_time.tm_mon }/{ self.last_work_time.tm_year }-{self.last_work_time.tm_hour}:{self.last_work_time.tm_min}:{self.last_work_time.tm_sec}"

    def __str__(self):
        return self.name + " " + str( self.id )

def user_from_dict(dictionary: dict) -> User:
    user = User("", 0)
    user._signup_time = dictionary['_signup_time']
    user.name         = dictionary['name']
    user.id           = dictionary['id']
    user.bank         = dictionary['bank']
    user.wallet       = dictionary['wallet']
    user.items        = dictionary['items']
    user.last_work_time = dictionary['last_work_time']
    return user