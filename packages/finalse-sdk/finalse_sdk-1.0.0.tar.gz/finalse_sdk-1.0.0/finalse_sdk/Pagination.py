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
from finalse_sdk.Page import Page
from typing import Dict
from typing import Optional
import json


class Pagination:
    def __init__(self,
                 current_page: Page,
                 previous_page: Optional[Page],
                 next_page: Optional[Page],
                 started_time: str,
                 nb_items_on_current_page: int,
                 nb_items_per_page: int):
        self._type = "Pagination" 
        self.current_page = current_page
        self.previous_page = previous_page
        self.next_page = next_page
        self.started_time = started_time
        self.nb_items_on_current_page = nb_items_on_current_page
        self.nb_items_per_page = nb_items_per_page

    @staticmethod
    def _type(): 
        return "Pagination"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Pagination.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('currentPage', self.current_page.__to_remote_dict()),
            ('previousPage', self.previous_page.__to_remote_dict()),
            ('nextPage', self.next_page.__to_remote_dict()),
            ('startedTime', self.started_time),
            ('nbItemsOnCurrentPage', self.nb_items_on_current_page),
            ('nbItemsPerPage', self.nb_items_per_page)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('current_page', self.current_page.to_dict()),
            ('previous_page', self.previous_page.to_dict()),
            ('next_page', self.next_page.to_dict()),
            ('started_time', self.started_time),
            ('nb_items_on_current_page', self.nb_items_on_current_page),
            ('nb_items_per_page', self.nb_items_per_page)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Pagination(Page.from_remote_dict(d["currentPage"]),
                          Page.from_remote_dict(d["previousPage"]) if "previousPage" in d else None,
                          Page.from_remote_dict(d["nextPage"]) if "nextPage" in d else None,
                          d["startedTime"],
                          d["nbItemsOnCurrentPage"],
                          d["nbItemsPerPage"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Pagination(Page.from_dict(d["current_page"]),
                          Page.from_dict(d["previous_page"]) if "previous_page" in d else None,
                          Page.from_dict(d["next_page"]) if "next_page" in d else None,
                          d["started_time"],
                          d["nb_items_on_current_page"],
                          d["nb_items_per_page"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Pagination(current_page=" + repr(self.current_page) + 
                           ", previous_page=" + repr(self.previous_page) + 
                           ", next_page=" + repr(self.next_page) + 
                           ", started_time=" + self.started_time + 
                           ", nb_items_on_current_page=" + str(self.nb_items_on_current_page) + 
                           ", nb_items_per_page=" + str(self.nb_items_per_page) + ")")