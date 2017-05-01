import plugins.pluginapi
import json

# This is an example plugin. Feel free to remove it! :)
class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'ld'
        desc = 'Find an LD game from the user'
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('find', self.cmd_find)
        with open('ld38.json') as f:
            self.ld_data = json.loads(f.read())

    def cmd_find(self, usr, cmd, chan):
        if len(cmd) > 1:
            user_to_find = cmd[1]
        else:
            user_to_find = usr
        for g in self.ld_data['games']:
            if g['author'] == user_to_find:
                self.send_msg("%s by %s: https://ldjam.com%s" % (g['name'], g['author'], g['path']), chan)
                return
        self.send_msg("Couldn't find any games by " + user_to_find, chan)
