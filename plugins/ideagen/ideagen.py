import plugins.pluginapi
import random, json


class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'Game Idea Generator'
        desc = 'Generates a random idea for a game! (List by sorceress)'
        dataFile = "data.json"
        self.data = json.loads(open(dataFile).read())["idea-generator"]
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('idea', self.cmd_idea)
        

    def cmd_idea(self, usr, cmd):
        choice1 = random.choice(self.data["list1"]).lower()
        choice2 = random.choice(self.data["list2"]).lower()
        choice3 = random.choice(self.data["list3"]).lower()
        
        self.send_msg("Make a%s %s %s %s!" % (self.add_n(choice1), choice1, choice2, choice3), self.channel)
    
    def add_n(self, text):
        if text[0].lower() == "a" or text[0].lower() == "e" or text[0].lower() == "i" or text[0].lower() == "o" or text[0].lower() == "u":
            return 'n'
        else:
            return ''