import json
import operator


class User():

    def __init__(self, username):
       
        f = open('userdata_master.json')
        user_master = json.load(f)
        f.close()
        self.user_master = user_master 
        self.username = username
    
    def changeUser(self, username):
        self.username = username
        if(not (self.username in self.user_master)):
            self.user_master[self.username] = {'points': 0, 'emotes': {}}
            self.points = 0

    def addPoints(self, amount):
        self.user_master[self.username]['points'] += amount 

    def returnPoints(self):
        return self.user_master[self.username]['points'] 

    def logEmote(self, emote, amount):
        if(not 'emotes' in self.user_master[self.username]):
            self.user_master[self.username].update({'emotes': {}})
        if(not emote in self.user_master[self.username]['emotes']):
            self.user_master[self.username]['emotes'].update({emote : 0}) 
        self.user_master[self.username]['emotes'][emote] += amount 

    def returnEmoteCount(self, emote):
        return self.user_master[self.username]['emotes'][emote]

    def favoriteEmote(self):
        sorted_emotes = sorted(self.user_master[self.username]['emotes'].items(), key=lambda x: x[1], reverse=True)
        return (f"@{self.username}'s most used emote is {sorted_emotes[0][0]} with {sorted_emotes[0][1]} uses!")

    def save_user_data(self):
        with open('userdata_master.json', 'w') as f:
            json.dump(self.user_master, f)

    def deductPoints(self, amount):
        self.user_master[self.username]['points'] -= amount 

    def sendPoints(self, amount, otheruser):
        self.user_master[self.username]['points'] -= amount
        self.user_master[otheruser]['points'] += amount


def pointLeaderboard():
    f = open('userdata_master.json')
    user_master = json.load(f)
    f.close()
    sorted_users = sorted(user_master.items(), key=lambda x: x[1]['points'], reverse=True)
    leaderboard = "" 
    for count, user in enumerate(sorted_users[:5]):
       leaderboard += (f"(#{count+1}) @{user[0]} {user[1]['points']} gems, ") 
    return leaderboard

def syncGlobalChatData():
    f = open('userdata_master.json')
    user_master = json.load(f)
    f.close()
    if(not "$CHAT_GENERAL" in user_master):
        user_master.update({'$CHAT_GENERAL' : {}})
        user_master['$CHAT_GENERAL'].update({'emotes': {}})
    for user in user_master.items():
        for emote in user[1]['emotes']:
            user_master['$CHAT_GENERAL']['emotes'][emote] = 0
    for user in user_master.items():
        if(user[0] != "$CHAT_GENERAL"):
            for emote in user[1]['emotes']:
                if(not emote in user_master['$CHAT_GENERAL']['emotes']):
                    user_master['$CHAT_GENERAL']['emotes'].update({emote : 0})
                user_master['$CHAT_GENERAL']['emotes'][emote] += user[1]['emotes'][emote] 
        
    with open('userdata_master.json', 'w') as f:
        json.dump(user_master, f)

syncGlobalChatData()
