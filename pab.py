import json
import sys, os, imp

import irc.bot
import irc.strings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Pab(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        self.config = config
        irc.bot.SingleServerIRCBot.__init__(self, [(config["connection"]["server"], config["connection"]["port"])],
                                            config["connection"]["nick"], config["connection"]["nick"])
        self.channel = config["connection"]["channel"]
        self.command_prefix = config["botsettings"]["command_prefix"]

        self.plugins = []

        self.load_plugins(config["botsettings"]["plugins_folder"])

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        for plugin in self.plugins:
            plugin.on_nicknameinuse(c.get_nickname())

    def on_welcome(self, c, e):
        c.join(self.channel)
        for plugin in self.plugins:
            plugin.on_welcome(c.get_nickname())

    def on_privmsg(self, c, e):
        for plugin in self.plugins:
            plugin.on_message(e.source.nick)

    def on_join(self, c, e):
        for plugin in self.plugins:
            plugin.on_userjoin(e.source.nick)

    def on_disconnect(self, c, e):
        for plugin in self.plugins:
            plugin.on_userquit(e.source.nick)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(self.command_prefix, 1)
        if len(a) > 1:
            self.do_command(e, a[1].strip())
        
        for plugin in self.plugins:
            plugin.on_message(e.arguments[0], e.source.nick)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        for plugin in self.plugins:
            plugin.on_command(cmd, nick)

    def load_plugins(self, plugins):
        print("Loading plugins")

        self.plugins = []
        for path in os.listdir(plugins):
            self.load_plugin(path)

    def load_plugin(self, path):
        print("Loading %s" % path)

        if os.path.isdir(os.path.join(self.config["botsettings"]["plugins_folder"], path)):
            plugin_file_path = os.path.join(self.config["botsettings"]["plugins_folder"], path, "%s.py" % path)

            if os.path.isfile(plugin_file_path):
                try:
                    print("Trying to import %s" % path)
                    plugin_module = imp.load_source(path, plugin_file_path)
                    print("Loaded %s" % path)
                except:
                    print("Error importing plugin %s!" % path)
                    return False

                if hasattr(plugin_module, "Plugin"):
                    try:
                        print("Creating plugin")
                        plugin = plugin_module.Plugin(self, self.config)
                        print("Loaded plugin %s" % plugin.name)
                    except:
                        print("Failed to load %s" % plugin_file_path)
                        return False

                    for p in self.plugins:
                        if p.name == plugin.name:
                            self.plugins.remove(p)
                    self.plugins.append(plugin)
                    return True


def main():
    configFile = 'config.json'
    try:
        configFile = open(configFile)
        settings = json.loads(configFile.read())
    except:
        print("Could not open the config. Quitting.")
        sys.exit(1)

    pab = Pab(settings)

    pab.start()

if __name__ == "__main__":
    main()
