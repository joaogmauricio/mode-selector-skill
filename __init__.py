from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
import time

class ModeSelector(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)

	def initialize(self):
		self.register_entity_file('type.entity')
		self.bus.on('mycroft.skills.list', self.test)

	def test(self, message):
		self.log.error("123")

	@intent_handler('selector.mode.intent')
	def handle_selector_mode(self, message):
		type = message.data.get('type')

		if 'gpt'.lower() in type:
			# always keep this one on
			self.bus.emit(Message("skillmanager.keep", {'skill': "mode-selector-skill"}))
			time.sleep(0.4)
			self.bus.emit(Message("skillmanager.activate", {'skill': "fallback-chatgpt3-skill.joaogmauricio"}))

		if 'normal'.lower() in type:
			self.bus.emit(Message("skillmanager.list"))

		self.speak_dialog('mode.changed', data={
			'type': type
		})


def create_skill():
	return ModeSelector()

