from finalse_sdk.Deposit import Deposit
from finalse_sdk.Auth import Auth
from finalse_sdk.FPayClient import FPayClient

f_pay = FPayClient(Auth(token="<token>", secret_key="<secretKey>"))
deposit: Deposit = f_pay.deposit().initiate(dict(
    amount= "10_000 XOF",
    source= "CI MtnMoney +2250500000000",
    h1= "Premier Dépôt via API"
))
print(deposit)
print(deposit.h1_descriptor.fr)
print(deposit.status)
print(deposit.amount)
