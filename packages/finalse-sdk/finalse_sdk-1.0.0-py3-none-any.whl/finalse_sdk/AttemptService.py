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
from finalse_sdk.Attempt import Attempt
from finalse_sdk.Auth import Auth
from finalse_sdk.Http import Http
from finalse_sdk.ListForm import ListForm
from finalse_sdk.Page import Page
from finalse_sdk.Sdk import Sdk
import json


class AttemptService:
    def __init__(self, auth: Auth):
        self._type = "AttemptService" 
        self.auth = auth

    def get(self, form: str):
        return Http.get("/" + Sdk.version() + "/attempts/" + form, "", {}, Attempt.from_json, self.auth)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "AttemptService(auth=" + repr(self.auth) + ")"