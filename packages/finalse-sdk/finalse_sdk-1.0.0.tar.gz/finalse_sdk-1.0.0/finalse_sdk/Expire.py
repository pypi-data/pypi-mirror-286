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
from finalse_sdk.Duration import Duration
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
import json


class Expire:
    def __init__(self, delay: Duration, time: UTCDateTime):
        self._type = "Expire" 
        self.delay = delay
        self.time = time

    @staticmethod
    def _type(): 
        return "Expire"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Expire.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('delay', self.delay.__to_remote_dict()),
            ('time', self.time.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('delay', self.delay.to_dict()),
            ('time', self.time.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Expire(Duration.from_remote_dict(d["delay"]),
                      UTCDateTime.from_remote_dict(d["time"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Expire(Duration.from_dict(d["delay"]),
                      UTCDateTime.from_dict(d["time"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Expire(delay=" + repr(self.delay) + 
                       ", time=" + repr(self.time) + ")")