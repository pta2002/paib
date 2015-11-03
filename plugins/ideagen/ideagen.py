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
        self.send_msg("Make a %s %s %s!" % (random.choice(self.data["list1"]).lower(), random.choice(self.data["list2"]).lower(),
                                            random.choice(self.data["list3"]).lower()), self.channel)