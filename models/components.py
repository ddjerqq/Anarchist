import disnake
from disnake import ui
from disnake import Button
from disnake import MessageInteraction
from disnake import ButtonStyle


class YesNoButton(ui.View):
    def __init__(self, *, timeout: float = 180, intended_user: disnake.user.User = None):
        super().__init__(timeout = timeout)
        self.intended_user = intended_user
        self.choice = None
    
    @ui.button(label="yes", style=ButtonStyle.green)
    async def _yes(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = True
        self.stop()

    @ui.button(label="no", style=ButtonStyle.danger)
    async def _no(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = False
        self.stop()


class LowerHigherGuessButton(ui.View):
    """
    lower
    higher
    guess
    """
    def __init__(self, *, timeout: float = 180, intended_user: disnake.user.User = None):
        super().__init__(timeout=timeout)
        self.intended_user = intended_user
        self.choice = None

    @ui.button(label="lower", style=ButtonStyle.danger)
    async def _lower(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = "lower"
        self.stop()

    @ui.button(label="same", style=ButtonStyle.green)
    async def _guess(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = "guess"
        self.stop()

    @ui.button(label="higher", style=ButtonStyle.primary)
    async def _higher(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = "higher"
        self.stop()


class BlackJackButton(ui.View):
    def __init__(self, *, timeout: float = 180, intended_user: disnake.user.User = None):
        super().__init__(timeout = timeout)
        self.intended_user = intended_user
        self.choice = None

    @ui.button(label="hit", style=ButtonStyle.green)
    async def _hit(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = "hit"
        self.stop()

    @ui.button(label="stand", style=ButtonStyle.gray)
    async def _stand(self, button: Button, inter: MessageInteraction):
        if self.intended_user:
            if inter.author != self.intended_user:
                return
        self.choice = "stand"
        self.stop()
