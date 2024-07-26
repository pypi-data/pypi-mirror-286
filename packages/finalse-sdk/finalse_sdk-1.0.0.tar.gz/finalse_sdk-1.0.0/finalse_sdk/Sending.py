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


class Sending:
    def __init__(self, value: str):
        self._type = "Sending" 
        self.value = value

    @staticmethod
    def NotYetDone():
        return Sending("NotYetDone")

    @staticmethod
    def PartiallyDone():
        return Sending("PartiallyDone")

    @staticmethod
    def TotallyDone():
        return Sending("TotallyDone")

    @staticmethod
    def all_possibles_values():
        return {"NotYetDone",
                "PartiallyDone",
                "TotallyDone"}

    @staticmethod
    def from_string(value):
        if value == "NotYetDone": return Sending.NotYetDone()
        elif value == "PartiallyDone": return Sending.PartiallyDone()
        elif value == "TotallyDone": return Sending.TotallyDone()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in Sending.all_possibles_values()

    def is_not_yet_done(self):
        return self.value == "NotYetDone"

    def is_partially_done(self):
        return self.value == "PartiallyDone"

    def is_totally_done(self):
        return self.value == "TotallyDone"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Sending(value=" + self.value + ")"

    def __str__(self):
        return self.value