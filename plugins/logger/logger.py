import plugins.pluginapi


class Plugin(plugins.pluginapi.BasicPlugin):
	def __init__(self, bot, config):
		name = 'Logger'
		desc = 'Keeps logs'
		plugins.pluginapi.BasicPlugin.__init__(self, name, desc, config, bot.connection)

	#def on_message():
	#	pass