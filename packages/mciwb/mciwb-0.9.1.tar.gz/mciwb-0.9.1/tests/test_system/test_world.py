"""
System tests for the Copy class
"""

from time import sleep

from mciwb.imports import Direction, Item, Iwb, Player, get_client
from tests.conftest import ENTITY_NAME


def test_session_fixtures(mciwb_world: Iwb, minecraft_player: Player):
    """
    verify that the global session fixtures that create a minecraft server,
    RCON client and mciwb.Player are working
    """
    assert mciwb_world.player.pos == minecraft_player.pos


def test_world_reporting(mciwb_world: Iwb):
    """
    verify printing of the world object
    """
    assert f"player: {ENTITY_NAME}" in mciwb_world.__repr__()


def test_world_player_signs(mciwb_world: Iwb, minecraft_player: Player):
    """
    verify printing of the world object
    """

    sp = (
        'minecraft:oak_sign{{front_text:{{messages:[\'{{"text":"{0}"}}\','
        '\'{{"text":""}}\',\'{{"text":""}}\',\'{{"text":""}}\']}}}}'
    )

    client = get_client()
    # place some action signs in the world and verify they are actioned
    select = sp.format("select")
    extend = sp.format("expand")
    paste = sp.format("paste")

    sleep(1)
    p = minecraft_player.pos
    client.setblock(p + Direction.SOUTH * 3, select)
    sleep(0.5)
    client.setblock(p + Direction.SOUTH * 3, select)
    sleep(0.5)
    client.setblock(p + Direction.SOUTH, extend)
    sleep(0.5)
    client.setblock(p + Direction.SOUTH * 2 + Direction.UP, paste)
    sleep(0.5)

    block = mciwb_world.get_block(p + Direction.SOUTH * 2)

    assert block == Item.GRASS_BLOCK

    mciwb_world.set_block(p + Direction.SOUTH * 2, Item.AIR)
