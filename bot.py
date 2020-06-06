#bot.py
import os #import env vars for bot
from twitchio.ext import commands
from trivia import generate_questions 
import random
import time
import asyncio
from datetime import datetime 
from user_profiles import User, pointLeaderboard, syncGlobalChatData 
from emoteslist import global_emotes
import sys
import re

class Bot(commands.Bot):

    current_question = None
    trivia_round = None
    emote_parameter = None
    current_trivia_game = False
    currentUser = User("USER_INTERACTION_PLACER")
    def __init__(self):
        super().__init__(irc_token=os.environ['TMI_TOKEN'], client_id=os.environ['CLIENT_ID'], nick=os.environ['BOT_NICK'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        self.currentUser = User("USER_INTERACTION_PLACER")

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = self._ws #needed to send messages within event_ready
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower(): #ignores bot & streamer
            return
        if(self.current_question != None and self.trivia_round == True):
            if((ctx.content).lower() == self.current_question[2].lower()):
                await ctx.channel.send(f"@{ctx.author.name} got it correct for 25 gems, with the answer being {self.current_question[2]}")
                currentUser = User(ctx.author.name.lower()) 
                currentUser.addPoints(25)
                currentUser.save_user_data()
                self.trivia_round = False

        emote_gen = (emote for emote in global_emotes if emote in (ctx.content).split())
        for emote in emote_gen:
            self.currentUser.changeUser(ctx.author.name.lower())
            self.currentUser.logEmote(emote, (ctx.content).count(emote))
        await self.handle_commands(ctx)

        if(ctx.content == "$save_data"):
            print("saved")  
            self.currentUser.save_user_data()


    @commands.command(name='ecount')
    async def ecount(self, ctx, emote):
        syncGlobalChatData()
        currentUser = User("$CHAT_GENERAL")
        try:
            await ctx.send(f"{emote} has been used {currentUser.returnEmoteCount(emote)-1} in chat!")
        except:
            await ctx.send("I either don't know that emote or the input is wrong")
            return


    @commands.command(name='sendgems')
    async def sendgems(self, ctx, amount, otheruser):
        num = None
        insuredname = None
        currentUser = User(ctx.author.name.lower())
        try:
            num = int(amount)
            if("@" in otheruser):
                insuredname = otheruser[1:]
            else:
                insuredname = otheruser
            str(otheruser)
        except:
            await ctx.send("Please insert in format $sendgems amount name with whole numbers") 
            return
        try:
            currentUser.sendPoints(num, insuredname)
        except:
            await ctx.send("I don't know that user :(, maybe they haven't typed in this chat yet")
            return
        await ctx.send(f"@{ctx.author.name} has sent {num} gems to @{insuredname}")
        currentUser.save_user_data()

    @commands.command(name='gamble')
    async def gamble(self, ctx, amount):
        currentUser = User(ctx.author.name.lower())
        bet = None
        if(amount == "all"):
            bet = currentUser.returnPoints()
        elif(amount == "half"):
            bet = currentUser.returnPoints() / 2
        else:
            try:
                bet = int(amount)
            except:
                await ctx.send(f"@{ctx.author.name}, improper bet type. Please only use whole numbers, \"all\", or \"half\"")
                return
        random.seed()
        gamba = random.randint(0,1) 
        if(gamba == 1):
            currentUser.addPoints(bet)
            await ctx.send(f"Congrats @{ctx.author.name}, you have won {bet} gems, and now have a total of {currentUser.returnPoints()} gems")
        if(gamba == 0):
            currentUser.deductPoints(bet) 
            await ctx.send(f"Unlucky @{ctx.author.name}, you have lost {bet} gems, and now have a total of {currentUser.returnPoints()} gems")
        currentUser.save_user_data()

    @commands.command(name='shutdown')
    async def shutdown(self, ctx):
        if((ctx.author.name.lower() == "1xelerate") or (ctx.author.is_mod)):
            await ctx.send("guess ill leave Sadge")
            sys.exit()
        else:
            await ctx.send(f"@{ctx.author.name} does not have permission to control me LULW")
    
    @commands.command(name='favorite')
    async def favorite(self, ctx, optional_user=None):
        currentUser = User(ctx.author.name.lower()) 
        if(optional_user != None):
            if("@" in optional_user):
                optional_user = optional_user[1:]
            try:
                if(optional_user == "chat"):
                    syncGlobalChatData()
                    currentUser = User("$CHAT_GENERAL")
                else:
                    currentUser = User(optional_user.lower())
            except:
                await ctx.send("I don't know that user :(") 
                return
        await ctx.send(currentUser.favoriteEmote())

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        await ctx.send(pointLeaderboard())
        
    @commands.command(name='emotecount')
    async def emotecount(self, ctx, emote):
        try:
            self.currentUser.changeUser(ctx.author.name.lower())
            await ctx.send(f"@{ctx.author.name} has used {emote} {self.currentUser.returnEmoteCount(emote) -1} times since my inception")
        except:
            await ctx.send("Sorry, I either don't know that emote or your input is wrong, do $emotecount emotename")

    @commands.command(name='gems')
    async def gems(self, ctx, optional_user=None):
        currentUser = User(ctx.author.name.lower()) 
        if(optional_user != None):
            if("@" in optional_user):
                optional_user = optional_user[1:]
            try:
                currentUser = User(optional_user.lower())
            except:
                await ctx.send("I don't know that user :(") 
                return
        await ctx.send(f"@{currentUser.username} has {currentUser.returnPoints()} gems")

    @commands.command(name='weebs')
    async def weebs(self, ctx):
        await ctx.send('ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ANTI WEEB SPAM NaM ')

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        if(not self.current_trivia_game):
            self.current_trivia_game = True
            question_size = 5
            question_number = 1
            random.seed()
            question_masterlist, question_genres = generate_questions()
            await ctx.send("Trivia will start in 10 seconds!")
            while question_size >= question_number:
                await asyncio.sleep(10)
                self.trivia_round = True    
                hint = 0
                self.current_question = question_masterlist[random.randrange(0, len(question_masterlist), 1)]
                await ctx.send(f"[{question_number}/{question_size}] {self.current_question[0]}: " + f"{self.current_question[1]}")
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
                question_number+=1
            self.current_question = None
            self.current_trivia_game = False
               
bot = Bot()
bot.run()
