from mycroft import MycroftSkill, intent_file_handler


class ModeSelector(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('selector.mode.intent')
    def handle_selector_mode(self, message):
        type = message.data.get('type')

        self.speak_dialog('selector.mode', data={
            'type': type
        })


def create_skill():
    return ModeSelector()

