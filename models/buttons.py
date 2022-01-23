import disnake
from disnake import ui
from disnake import Button
from disnake import MessageInteraction
from disnake import ButtonStyle


class YesNoButton(ui.View):
    def __init__(self, *, timeout: float = 180, intended_user: disnake.user.User = None):
        super().__init__(timeout = timeout)
        self.indended_user = intended_user
        self.choice = None
    
    @ui.button(label="yes", style=ButtonStyle.green)
    async def _yes(self, button: Button, inter: MessageInteraction):
        if self.indended_user:
            if inter.author != self.indended_user:
                return
        self.choice = True
        self.stop()

    @ui.button(label="no", style=ButtonStyle.danger)
    async def _no(self, button: Button, inter: MessageInteraction):
        if self.indended_user:
            if inter.author != self.indended_user:
                return
        self.choice = False
        self.stop()