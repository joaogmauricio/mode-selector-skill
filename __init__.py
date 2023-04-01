from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
import time

class ModeSelector(MycroftSkill):

	_initial_skills = []
	_current_mode = "normal"

	def __init__(self):
		MycroftSkill.__init__(self)

	def initialize(self):
		self.register_entity_file('type.entity')
		self.bus.once('mycroft.skills.list', self.get_active_skills)
		self.bus.emit(Message("skillmanager.list"))
		time.sleep(2)
		if self._current_mode == "normal":
			self.bus.emit(Message("skillmanager.deactivate", {'skill': "fallback-chatgpt3-skill.joaogmauricio"}))

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
			self.bus.emit(Message("skillmanager.activate", {'skill': "mycroft-naptime.mycroftai"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "fallback-unknown.mycroftai"}))
		elif 'normal' in type:
			for skill in self._initial_skills:
#				self.debug.error(skill)
				self.bus.emit(Message("skillmanager.activate", {'skill': skill}))
		elif any(t in type for t in ['private', 'privacy', 'offline', 'stealth']):
			# disable all skills but local ones
			self.bus.emit(Message("skillmanager.keep", {'skill': "mode-selector-skill"}))
			time.sleep(1.5)
			self.bus.emit(Message("skillmanager.activate", {'skill': "mycroft-naptime.mycroftai"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "mycroft-volume.mycroftai"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "mycroft-timer.mycroftai"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "mycroft-alarm.mycroftai"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "roomba-master-skill"}))
			self.bus.emit(Message("skillmanager.activate", {'skill': "fallback-unknown.mycroftai"}))

			# TODO: change STT to offline

		self._current_mode = type

		self.speak_dialog('mode.changed', data={
			'type': type
		})


	@intent_handler('get.current.mode.intent')
	def handle_get_current_mode(self, message):
		self.speak_dialog('current.mode', data={
			'type': self._current_mode
		})

	@intent_handler('list.modes.intent')
	def handle_list_modes(self, message):
		self.speak_dialog('list.modes')


def create_skill():
	return ModeSelector()

