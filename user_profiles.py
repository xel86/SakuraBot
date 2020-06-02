import json

class User():

    def __init__(self, username):

        f = open('userdata_master.json')
        self.user_master = json.load(f)
        f.close()
        self.username = username
        if(not (self.username in self.user_master)):
            self.user_master[self.username] = {'points': 0}
            self.points = 0
        else:
            self.points = self.user_master[self.username]['points']
    
    def addPoints(self, amount):
        self.points += amount

    def returnPoints(self):
        return self.points

    def save_user_data(self):
        self.user_master[self.username]['points'] = self.points
        with open('userdata_master.json', 'w') as f:
            json.dump(self.user_master, f)

