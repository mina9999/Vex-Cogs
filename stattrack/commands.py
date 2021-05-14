import datetime

from discord.ext.commands.cooldowns import BucketType
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

from stattrack.abc import MixinMeta
from stattrack.converters import TimeData, TimespanConverter

from .plot import plot

DEFAULT_TD = TimeData("1min", "1 minute", datetime.timedelta(days=1))


class StatTrackCommands(MixinMeta):
    async def all_in_one(
        self, ctx: commands.Context, timedata: TimeData, label: str, title: str, ylabel: str = None
    ):
        if self.df_cache is None:
            return await ctx.send("This command isn't ready yet. Try again in a few seconds.")
        await ctx.trigger_typing()  # wont be that long
        if ylabel is None:
            ylabel = title
        df = self.df_cache[[label]]
        file = await plot(df, timedata, title, ylabel)
        await ctx.send(file=file)

    @commands.cooldown(10, 60.0, BucketType.user)
    @commands.group()
    async def stattrack(self, ctx: commands.Context):
        """View my stats."""

    @stattrack.command()
    async def raw(self, ctx, var):
        await ctx.send(box(str(self.df_cache[[var]].head())))

    @stattrack.command()
    async def ping(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get my ping stats.

        Get command usage stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack ping 3w2d`
        `[p]stattrack ping 5d`
        `[p]stattrack ping all`
        """
        await self.all_in_one(ctx, timespan, "ping", "Commands per minute")

    @stattrack.command(name="commands")
    async def com(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get command usage stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack commands 3w2d`
        `[p]stattrack commands 5d`
        `[p]stattrack commands all`
        """
        await self.all_in_one(ctx, timespan, "command_count", "Commands per minute")

    @stattrack.command()
    async def messages(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get message stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack messages 3w2d`
        `[p]stattrack messages 5d`
        `[p]stattrack messages all`
        """
        await self.all_in_one(ctx, timespan, "message_count", "Messages per minute")

    @stattrack.command(aliases=["guilds"])
    async def servers(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get server stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack servers 3w2d`
        `[p]stattrack servers 5d`
        `[p]stattrack servers all`
        """
        await self.all_in_one(ctx, timespan, "guilds", "Server count")

    @stattrack.group(name="status")
    async def group_status(self, ctx: commands.Context):
        """See stats about user's statuses."""

    @group_status.command()
    async def online(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get online stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack status online 3w2d`
        `[p]stattrack status online 5d`
        `[p]stattrack status online all`
        """
        await self.all_in_one(ctx, timespan, "status_online", "Users online")

    @group_status.command()
    async def idle(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get idle stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack status idle 3w2d`
        `[p]stattrack status idle 5d`
        `[p]stattrack status idle all`
        """
        await self.all_in_one(ctx, timespan, "status_online", "Users idle")

    @group_status.command()
    async def offline(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get offline stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack status offline 3w2d`
        `[p]stattrack status offline 5d`
        `[p]stattrack status offline all`
        """
        await self.all_in_one(ctx, timespan, "status_offline", "Users offline")

    @group_status.command()
    async def dnd(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get dnd stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack status dnd 3w2d`
        `[p]stattrack status dnd 5d`
        `[p]stattrack status dnd all`
        """
        await self.all_in_one(ctx, timespan, "status_dnd", "Users dnd")

    @stattrack.group(name="users")
    async def users_group(sef, ctx: commands.Context):
        """See stats about user counts"""

    @users_group.command(name="total")
    async def users_total(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get total user stats.

        This includes humans and bots and counts users/bots once per server they share with me.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack users total 3w2d`
        `[p]stattrack users total 5d`
        `[p]stattrack users total all`
        """
        await self.all_in_one(ctx, timespan, "users_total", "Total users")

    @users_group.command()
    async def unique(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get total user stats.

        This includes humans and bots and counts them once, reagardless of how many servers they
        share with me.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack users unique 3w2d`
        `[p]stattrack users unique 5d`
        `[p]stattrack users unique all`
        """
        await self.all_in_one(ctx, timespan, "users_unique", "Unique users")

    @users_group.command()
    async def humans(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get human user stats.

        This is the count of unique humans. They are counted once, regardless of how many servers
        they share with me.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack users humans 3w2d`
        `[p]stattrack users humans 5d`
        `[p]stattrack users humans all`
        """
        await self.all_in_one(ctx, timespan, "users_humans", "Humans")

    @users_group.command()
    async def bots(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get bot user stats.

        This is the count of unique bots. They are counted once, regardless of how many servers
        they share with me.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack users bots 3w2d`
        `[p]stattrack users bots 5d`
        `[p]stattrack users bots all`
        """
        await self.all_in_one(ctx, timespan, "users_bots", "Bots")

    @stattrack.group(name="channels")
    async def channels_group(self, ctx: commands.Context):
        """See how many channels there are in all my guilds"""

    @channels_group.command(name="total")
    async def chan_total(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get total channel stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack channels total 3w2d`
        `[p]stattrack channels total 5d`
        `[p]stattrack channels total all`
        """
        await self.all_in_one(ctx, timespan, "channels_total", "Total channels")

    @channels_group.command()
    async def text(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get text channel stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack channels text 3w2d`
        `[p]stattrack channels text 5d`
        `[p]stattrack channels text all`
        """
        await self.all_in_one(ctx, timespan, "channels_text", "Text channels")

    @channels_group.command()
    async def voice(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get voice channel stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack channels voice 3w2d`
        `[p]stattrack channels voice 5d`
        `[p]stattrack channels voice all`
        """
        await self.all_in_one(ctx, timespan, "channels_voice", "Voice channels")

    @channels_group.command()
    async def categories(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get categories stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack channels categories 3w2d`
        `[p]stattrack channels categories 5d`
        `[p]stattrack channels categories all`
        """
        await self.all_in_one(ctx, timespan, "channels_cat", "Categories")

    @channels_group.command()
    async def stage(self, ctx: commands.Context, timespan: TimespanConverter = DEFAULT_TD):
        """
        Get stage channel stats.

        **Arguments**

        `<timespan>` How long to look for, or `all` for all-time data. Defaults to 1 day. Must be
        at least 1 hour.

        **Examples:**

        `[p]stattrack channels stage 3w2d`
        `[p]stattrack channels stage 5d`
        `[p]stattrack channels stage all`
        """
        await self.all_in_one(ctx, timespan, "channels_stage", "Stage channels")
