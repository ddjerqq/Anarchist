import disnake
from datetime import datetime
from database import database
from utils import *



def embed_from_block(block: dict) -> disnake.Embed:
    """
    Create an embed from a block
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Args:
      block (dict): the block from the blockchain
    
    Returns:
      disnake.Embed of the block
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    `Block #{id}`\n
    `Sender        Receiver      Amount        `\n
    `Name: {name}  Name: {name}  {amount} coins`\n
    `ID: {id}      ID: {id}                    `\n
    `Previous hash`\n
    `0000d13ed7d30173fb0b85fd81bab62c565c10cba43fb726caa55e7ebbba0a97`\n
    `UTC: Mon Jan 24 04:02:52 2022 `
    """
    em = disnake.Embed(
        title = f"Block #{block['index']}",
        color = 0x00ff00
    )
    em.add_field(
        name   = "Sender",
        value  = f"Name: {database[block['data']['sender_id']].name} \nID: {block['data']['sender_id']}",
        inline = True
    )
    em.add_field(
        name   = "Receiver",
        value  = f"Name: {database[block['data']['receiver_id']].name} \nID: {block['data']['receiver_id']}",
        inline = True
    )
    em.add_field(
        name   = "Amount",
        value  = f"{block['data']['amount']} coins",
        inline = True
    )
    em.add_field(
        name   = "Previous hash",
        value  = f"`{block['prev_hash']}`",
        inline = False
    )
    em.set_footer(
        text = "Timestamp:  " + datetime.fromtimestamp(block['data']['timestamp']).strftime("%c")
    )
    return em