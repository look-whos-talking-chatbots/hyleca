"""
File that contains the class for loading a Bot to the system.
"""

import json
from dataclasses import dataclass, asdict


@dataclass
class Bot:
    name: str
    version: str
    language: str
    description: str
    slot_fillers: dict
    dialogue_flows: dict
    onhold_duration: int = 1
    max_exchanges: int = 0

    @classmethod
    def load_bot(cls, settings):
        with open(settings['path'], 'r') as file:
            data = json.load(file)
            obj = cls(**data)
            # Warning: Following line loads all the variables given to the bot's settings
            #          (from AGENT_INDEX) except the "path" and the "generators"
            for key, value in settings.items():
                if key not in ['path', 'generators']:
                    setattr(obj, key, value)
            if 'generators' in settings:
                obj.set_generation(generators=settings['generators'])
            return obj

    def set_generation(self, generators=None):
        """Sets which generators should be used while running the bot

        :param generators: list of strings
        :return:
        """
        if generators is not None:
            for flow in self.dialogue_flows:
                for state in flow['states']:
                    if state['type'] == 'dialogue':
                        state['generators'] = generators

    def to_json(self):
        return json.dumps(asdict(self))
