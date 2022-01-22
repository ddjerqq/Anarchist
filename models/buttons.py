import disnake

from disnake.ext import commands
from disnake import AppCmdInter
from disnake import ui
from disnake import Button
from disnake import MessageInteraction
from disnake import ButtonStyle


class YesNoButton(ui.View):
    def __init__(self, *, timeout: float = 180):
        super().__init__(timeout = timeout)

        self.choice = None
    
    @ui.button(label="yes", style=ButtonStyle.green)
    async def _yes(self, button: Button, inter: MessageInteraction):
        self.choice = True
        self.stop()

    @ui.button(label="no", style=ButtonStyle.danger)
    async def _no(self, button: Button, inter: MessageInteraction):
        self.choice = False
        self.stop()