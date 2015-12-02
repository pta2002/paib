import plugins.pluginapi
import random, json


class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'Game Idea Generator'
        desc = 'Generates a random idea for a game! (List by sorceress)'
        self.dataFile = "data.json"
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('idea', self.cmd_idea)
        self.register_command('submitidea', self.cmd_submitidea)
        

    def cmd_idea(self, usr, cmd):
        self.data = json.loads(open(self.dataFile).read())["idea-generator"]
        choice1 = random.choice(self.data["list1"]).lower()
        choice2 = random.choice(self.data["list2"]).lower()
        choice3 = random.choice(self.data["list3"]).lower()
        
        self.send_msg("Make a%s %s %s %s!" % (self.add_n(choice1), choice1, choice2, choice3), self.channel)
    
    def cmd_submitidea(self, usr, cmd):
        ideas = ' '.join(cmd[1:]).split('/')
        if len(ideas) != 3:
            self.send_msg('Please submit 3 ideas, one for each part, separated by slashes (/)', self.channel)
        else:
            for idea in range(len(ideas)):
                if ideas[idea].strip() != '':
                    self.submit_idea(ideas[idea], idea+1)
    
    def submit_idea(self, idea, part):
        try:
            data = json.loads(open(self.dataFile).read())
            data["idea-generator"]["suggestions"]["part" + str(part)].append(idea)
            open(self.dataFile, 'w').write(json.dumps(data, sort_keys=True, indent=4))
            self.send_msg('Your idea was successfully submitted. It will be reviewed and may soon be in the bot!', self.channel)
        except:
            self.send_msg('There was an error submitting your idea. Please try again later!', self.channel)
    
    def add_n(self, text):
        if text[0].lower() == "a" or text[0].lower() == "e" or text[0].lower() == "i" or text[0].lower() == "o" or text[0].lower() == "u":
            return 'n'
        else:
            return ''