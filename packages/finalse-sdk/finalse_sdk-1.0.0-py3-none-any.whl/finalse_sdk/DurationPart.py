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


class DurationPart:
    def __init__(self, w: int, d: int, h: int, m: int, s: int, ms: float):
        self._type = "DurationPart" 
        self.w = w
        self.d = d
        self.h = h
        self.m = m
        self.s = s
        self.ms = ms

    @staticmethod
    def _type(): 
        return "DurationPart"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return DurationPart.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('w', self.w),
            ('d', self.d),
            ('h', self.h),
            ('m', self.m),
            ('s', self.s),
            ('ms', self.ms)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('w', self.w),
            ('d', self.d),
            ('h', self.h),
            ('m', self.m),
            ('s', self.s),
            ('ms', self.ms)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return DurationPart(d["w"],
                            d["d"],
                            d["h"],
                            d["m"],
                            d["s"],
                            d["ms"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return DurationPart(d["w"],
                            d["d"],
                            d["h"],
                            d["m"],
                            d["s"],
                            d["ms"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("DurationPart(w=" + str(self.w) + 
                             ", d=" + str(self.d) + 
                             ", h=" + str(self.h) + 
                             ", m=" + str(self.m) + 
                             ", s=" + str(self.s) + 
                             ", ms=" + str(self.ms) + ")")