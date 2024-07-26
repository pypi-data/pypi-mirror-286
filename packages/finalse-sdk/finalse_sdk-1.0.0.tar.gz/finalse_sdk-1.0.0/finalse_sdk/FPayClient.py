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
from finalse_sdk.AttemptService import AttemptService
from finalse_sdk.Auth import Auth
from finalse_sdk.AuthAccessService import AuthAccessService
from finalse_sdk.DepositService import DepositService
from finalse_sdk.FundRequestService import FundRequestService
from finalse_sdk.QuasiTransferService import QuasiTransferService
from finalse_sdk.TransactionService import TransactionService
from finalse_sdk.TransferService import TransferService
from finalse_sdk.WalletService import WalletService


class FPayClient:
    def __init__(self, auth: Auth):
        self._type = "FPayClient" 
        self.auth = auth
        self._auth_access = AuthAccessService(auth)
        self._deposit = DepositService(auth)
        self._attempt = AttemptService(auth)
        self._fund_request = FundRequestService(auth)
        self._quasi_transfer = QuasiTransferService(auth)
        self._transaction = TransactionService(auth)
        self._transfer = TransferService(auth)
        self._wallet = WalletService(auth)

    def auth_access(self):
        return self._auth_access

    def deposit(self):
        return self._deposit

    def attempt(self):
        return self._attempt

    def fund_request(self):
        return self._fund_request

    def quasi_transfer(self):
        return self._quasi_transfer

    def transaction(self):
        return self._transaction

    def transfer(self):
        return self._transfer

    def wallet(self):
        return self._wallet

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FPayClient(auth=" + repr(self.auth) + ")"