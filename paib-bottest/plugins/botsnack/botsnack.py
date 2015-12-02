import plugins.pluginapi
import random


class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'botsnack'
        desc = "Do `$botsnack` to give pab a snack!"
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('botsnack', self.cmd_botsnack)
        self.botsnack_messages = [
            "Mmmmm!",
            "Tasty!",
            "Thanks!",
        ]

    def cmd_botsnack(self, usr, cmd):
        self.send_msg(random.choice(self.botsnack_messages), self.channel)