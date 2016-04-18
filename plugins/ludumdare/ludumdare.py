from plugins.ludumdare.update_db import *
import plugins.pluginapi

class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'ludumdare'
        desc = 'Add LD stuff.'
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('update_db', self.cmd_updatedb)
        self.config = config

    def cmd_updatedb(self, usr, cmd, chan):
        if usr in self.config["admin"]["admins"]:
            self.send_msg("Updating DB: bot will be down for a bit", chan)
            entries = update_db()
            self.send_msg("Done. Fetched %s entries" % str(entries), chan)
