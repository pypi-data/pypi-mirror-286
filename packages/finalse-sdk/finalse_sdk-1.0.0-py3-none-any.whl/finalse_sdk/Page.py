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


class Page:
    def __init__(self, index: int, url: str, query_string: str):
        self._type = "Page" 
        self.index = index
        self.url = url
        self.query_string = query_string

    @staticmethod
    def _type(): 
        return "Page"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Page.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('index', self.index),
            ('url', self.url),
            ('queryString', self.query_string)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('index', self.index),
            ('url', self.url),
            ('query_string', self.query_string)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Page(d["index"],
                    d["url"],
                    d["queryString"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Page(d["index"],
                    d["url"],
                    d["query_string"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Page(index=" + str(self.index) + 
                     ", url=" + self.url + 
                     ", query_string=" + self.query_string + ")")