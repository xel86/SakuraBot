#bot.py
import os #import env vars for bot
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['TMI_TOKEN'], client_id=os.environ['CLIENT_ID'], nick=os.environ['BOT_NICK'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = self._ws #needed to send messages within event_ready
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'

        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower(): #ignores bot & streamer
            return
        await self.handle_commands(ctx)

    @commands.command(name='weebs')
    async def weebs(self, ctx):
        await ctx.send('ANTI WEEB SPAM NaM')

bot = Bot()
bot.run()
