import plugins.pluginapi
import random, json


class _Plugin(plugins.pluginapi.BasicPlugin):
	def __init__(self, bot, config):
		name = 'Meme Generator'
		desc = 'Generates a random meme'
		plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)
		self.register_command('meme', self.cmd_meme)
		self.memes = json.loads(open('memes.json').read())
	
	def cmd_meme(self, usr, cmd):
		self.send_msg("%s - %s" % (random.choice(self.memes["meme-top"]), random.choice(self.memes["meme-bottom"])), self.channel)
