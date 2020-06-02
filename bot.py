#bot.py
import os #import env vars for bot
from twitchio.ext import commands
from trivia import generate_questions 
import random
import time
import asyncio
from datetime import datetime 

class Bot(commands.Bot):

    current_question = None
    trivia_round = None
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
        if(self.current_question != None):
            if((ctx.content).lower() == self.current_question[2].lower()):
                await ctx.channel.send(f"@{ctx.author.name} got it correct, with the answer being {self.current_question[2]}")
                self.trivia_round = False
        await self.handle_commands(ctx)

        


    @commands.command(name='weebs')
    async def weebs(self, ctx):
        await ctx.send('ANTI WEEB SPAM NaM')

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        random.seed()
        question_masterlist, question_genres = generate_questions()
        game = True
        while game:
            self.trivia_round = True    
            hint = 0
            self.current_question = question_masterlist[random.randrange(0, len(question_masterlist), 1)]
            await ctx.send(f"Topic: {self.current_question[0]}. " + f"{self.current_question[1]}")
            now = datetime.now()
            while self.trivia_round:
                await asyncio.sleep(0.1)
                if((datetime.timestamp(datetime.now()) - datetime.timestamp(now)) >= 20 and hint == 0):
                    await ctx.send(f"HINT: The answer contains {len(self.current_question[2])} characters")
                    hint = 1
                elif((datetime.timestamp(datetime.now()) - datetime.timestamp(now)) >= 40 and hint == 1):
                    await ctx.send(f"Times up! The correct answer is {self.current_question[2]}")
                    self.trivia_round = False
            question_masterlist.remove(self.current_question)
               
bot = Bot()
bot.run()
