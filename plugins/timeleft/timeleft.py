import plugins.pluginapi
import time

class Plugin(plugins.pluginapi.BasicPlugin):
    def __init__(self, bot, config):
        name = 'pineapple'
        desc = 'Blame Ajay.'
        plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
        self.register_command('timeleft', self.cmd_timeleft)
        self.ld_ends = 1460941200
        

    def cmd_timeleft(self, usr, cmd, chan):
        self.send_msg(time.strftime("Time left: %d days, %H hours, %M minutes, %S seconds.", time.gmtime(self.ld_ends - time.time())), chan)