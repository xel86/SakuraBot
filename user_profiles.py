import json

class User():

    def __init__(self, username):

        f = open('userdata_master.json')
        self.user_master = json.load(f)
        f.close()
        self.username = username
        if(not (self.username in self.user_master)):
            self.user_master[self.username] = {'points': 0, 'emotes': {}}
            self.points = 0
        else:
            self.points = self.user_master[self.username]['points']
    
    def addPoints(self, amount):
        self.points += amount

    def returnPoints(self):
        return self.points

    def logEmote(self, emote):
        if(not 'emotes' in self.user_master[self.username]):
            self.user_master[self.username].update({'emotes': {}})
        if(not emote in self.user_master[self.username]['emotes']):
            self.user_master[self.username]['emotes'].update({emote : 0}) 
        self.user_master[self.username]['emotes'][emote] += 1

    def returnEmoteCount(self, emote):
        return self.user_master[self.username]['emotes'][emote]

    def save_user_data(self):
        self.user_master[self.username]['points'] = self.points
        with open('userdata_master.json', 'w') as f:
            json.dump(self.user_master, f)

