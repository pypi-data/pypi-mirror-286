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
from finalse_sdk.Auth import Auth
from finalse_sdk.AuthAccess import AuthAccess
from finalse_sdk.Http import Http
from finalse_sdk.ListForm import ListForm
from finalse_sdk.Page import Page
from finalse_sdk.RestCollection import RestCollection
from finalse_sdk.Sdk import Sdk
import json


class AuthAccessService:
    def __init__(self, auth: Auth):
        self._type = "AuthAccessService" 
        self.auth = auth

    def fetch_page(self, page: Page):
        if page is None:
            raise ValueError("The page passed in argument is null. Hint:  Verify with collection.has_next_page() first before calling this function.")
        qs = page.query_string
        return Http.list_all("/" + Sdk.version() + "/auth-access", qs, {}, lambda json: AuthAccess.from_remote_dict(json), self.auth)

    def create(self, form: dict):
        return Http.post("/" + Sdk.version() + "/auth-access",  form, "", {}, AuthAccess.from_json, self.auth)

    def get(self, form: str):
        return Http.get("/" + Sdk.version() + "/auth-access/" + form, "", {}, AuthAccess.from_json, self.auth)

    def list(self, form: dict = None):
        qs = ListForm.empty().to_query_string() if form is None else ListForm.from_dict(form).to_query_string()
        return Http.list_all("/" + Sdk.version() + "/auth-access", qs, {}, lambda json: AuthAccess.from_remote_dict(json), self.auth)

    def update(self, form: dict):
        return Http.patch("/" + Sdk.version() + "/auth-access/" + form['id'],  form, "", {}, AuthAccess.from_json, self.auth)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "AuthAccessService(auth=" + repr(self.auth) + ")"