import json

# Send and received data
class PromptMessage():
    def __init__(self, _value, _message):
        self._value = _value
        self._message = _message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
