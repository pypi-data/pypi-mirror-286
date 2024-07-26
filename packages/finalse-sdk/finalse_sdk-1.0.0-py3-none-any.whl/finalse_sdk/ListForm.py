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
from urllib.parse import quote
from typing import Dict
from typing import Optional
import json


class ListForm:
    def __init__(self,
                 filter: Optional[str] = None,
                 limit: Optional[int] = None,
                 sort_by: Optional[str] = None):
        self._type = "ListForm" 
        self.filter = filter
        self.limit = limit
        self.sort_by = sort_by

    @staticmethod
    def _type(): 
        return "ListForm"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return ListForm.from_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('filter', self.filter),
            ('limit', self.limit),
            ('sortBy', self.sort_by)
        ]
        # return dict(t for t in tuples if t[1] is not None)
        return [(key, value) for key, value in tuples if value is not None]


    def to_dict(self):
        return dict([
            ('filter', self.filter),
            ('limit', self.limit),
            ('sort_by', self.sort_by)
        ])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return ListForm(d["filter"] if "filter" in d else None,
                        d["limit"] if "limit" in d else None,
                        d["sortBy"] if "sortBy" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return ListForm(d["filter"] if "filter" in d else None,
                        d["limit"] if "limit" in d else None,
                        d["sort_by"] if "sort_by" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    @staticmethod
    def empty():
        return ListForm(None, None, None)

    def to_query_string(self) -> str:
        if self.filter is None and self.limit is None and self.sort_by is None :
            return "" 
        else:
            return "?" + "&".join(key + "=" + quote(value) for key, value in self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("ListForm(filter=" + str(self.filter) +
                         ", limit=" + str(self.limit) + 
                         ", sort_by=" + str(self.sort_by) + ")")

