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
import json
from typing import Dict
from typing import List
from typing import TypeVar

from finalse_sdk.Pagination import Pagination

T = TypeVar('T')


class RestCollection:
    def __init__(self, url: str, pagination: Pagination, items: List[T]):
        self._type = "RestCollection"
        self.url = url
        self.pagination = pagination
        self.items = items

    def to_array(self):
        return self.items

    def has_next_page(self):
        return self.pagination.next_page is not None

    def has_previous_page(self):
        return self.pagination.previous_page is not None

    @staticmethod
    def _type():
        return "RestCollection"

    @staticmethod
    def from_json(js: str, item_converter: any):
        value = json.loads(js)
        items = list(map(lambda item: item_converter(item), value['items']))
        return RestCollection(value['url'],
                              Pagination.from_remote_dict(value['pagination']),
                              items)

    @staticmethod
    def from_remote_dict(d: Dict[str, any], item_converter: any):
        return RestCollection(d["url"],
                              Pagination.from_remote_dict(d["pagination"]),
                              list(map(lambda el: item_converter(el), d["items"])))

    def __to_remote_dict(self):
        tuples = [
            ('url', self.url),
            ('pagination', self.pagination.__to_remote_dict()),
            ('items', list(map(lambda el: el.__to_remote_dict(), self.items)))
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('url', self.url),
            ('pagination', self.pagination.to_dict()),
            ('items', list(map(lambda el: el.to_dict(), self.items)))
        ])

    @staticmethod
    def from_dict(d: Dict[str, any], item_converter:any):
        return RestCollection(d["url"],
                              Pagination.from_dict(d["pagination"]),
                              list(map(lambda el: item_converter(el), d["items"])))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("RestCollection(url=" + self.url +
                ", pagination=" + repr(self.pagination) +
                ", items=" + repr(self.items) + ")")
