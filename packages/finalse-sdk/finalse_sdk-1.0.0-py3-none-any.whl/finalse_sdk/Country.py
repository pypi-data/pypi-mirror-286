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
from finalse_sdk.Iso3166CountryCode import Iso3166CountryCode
from typing import Dict
import json


class Country:
    def __init__(self, code: Iso3166CountryCode, name: str):
        self._type = "Country" 
        self.code = code
        self.name = name

    @staticmethod
    def _type(): 
        return "Country"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Country.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('code', self.code.__to_remote_dict()),
            ('name', self.name)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('code', self.code.to_dict()),
            ('name', self.name)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Country(Iso3166CountryCode.from_remote_dict(d["code"]),
                       d["name"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Country(Iso3166CountryCode.from_dict(d["code"]),
                       d["name"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Country(code=" + repr(self.code) + 
                        ", name=" + self.name + ")")