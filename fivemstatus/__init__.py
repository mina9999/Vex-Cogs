import contextlib
import importlib
import json
from pathlib import Path

from redbot.core import VersionInfo
from redbot.core.bot import Red

from . import vexutils
from .fivemstatus import FiveMStatus
from .vexutils.meta import out_of_date_check

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot: Red) -> None:
    cog = FiveMStatus(bot)
    await out_of_date_check("fivemstatus", cog.__version__)
    r = bot.add_cog(cog)
    if r is not None:
        await r
