#   Copyright © 2024 Finalse Cloud
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from typing import Dict
import json


class FeesPayer:
    def __init__(self, value: str):
        self._type = "FeesPayer" 
        self.value = value

    @staticmethod
    def Receiver():
        return FeesPayer("Receiver")

    @staticmethod
    def Sender():
        return FeesPayer("Sender")

    @staticmethod
    def all_possibles_values():
        return {"Receiver",
                "Sender"}

    @staticmethod
    def from_string(value):
        if value == "Receiver": return FeesPayer.Receiver()
        elif value == "Sender": return FeesPayer.Sender()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in FeesPayer.all_possibles_values()

    def is_receiver(self):
        return self.value == "Receiver"

    def is_sender(self):
        return self.value == "Sender"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FeesPayer(value=" + self.value + ")"

    def __str__(self):
        return self.value