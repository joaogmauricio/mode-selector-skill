from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
import time

class ModeSelector(MycroftSkill):

	_initial_skills = []

	def __init__(self):
		MycroftSkill.__init__(self)

	def initialize(self):
		self.register_entity_file('type.entity')
		self.bus.once('mycroft.skills.list', self.get_active_skills)
		self.bus.emit(Message("skillmanager.list"))

	def get_active_skills(self, message):
		for key, value in message.data.items():
			if (value["active"]):
				self._initial_skills.append(key)
#		self.debug.error(len(self._initial_skills))

	@intent_handler('selector.mode.intent')
	def handle_selector_mode(self, message):
		type = message.data.get('type')

		if 'gpt' in type:
			# always keep this one on
			self.bus.emit(Message("skillmanager.keep", {'skill': "mode-selector-skill"}))
			time.sleep(1.5)
			self.bus.emit(Message("skillmanager.activate", {'skill': "fallback-chatgpt3-skill.joaogmauricio"}))
		elif 'normal' in type:
			for skill in self._initial_skills:
#				self.debug.error(skill)
				self.bus.emit(Message("skillmanager.activate", {'skill': skill}))
		elif any(t in type for t in ['private', 'privacy', 'offline', 'stealth']):
			# TODO: change STT to offline + disable all skills but the local ones
			self.bus.emit(Message("skillmanager.keep", {'skill': "mode-selector-skill"}))

		self.speak_dialog('mode.changed', data={
			'type': type
		})


def create_skill():
	return ModeSelector()

