from typing import Optional
from urllib.parse import urlencode
from aiohttp import ClientSession
from pydantic import BaseModel

from .utils import millisatoshis
from .Response import (
    GSendPaymentResponse,
    TransactionResponse,
    ChargesResponse,
    GetIdResponse,
    GetGamerTagResponse,

    LSendPaymentResponse,
    ValidateResponse,
    CreateChargeResponse,

    ESendPaymentResponse,

    PPaymentResponse,
    GetPaymentResponse,

    CCreateChargeResponse,
    GetChargeResponse,
    DecodeChargeResponse,

    CreateWithdrawalResponse,
    GetWithdrawalResponse,

    CreateVoucherResponse,
    GetVoucherResponse,
    RedeemVoucherResponse,
    RevokeVoucherResponse,

    GetWalletResponse,

    CreateStaticChargeResponse,
    GetStaticChargeResponse,
    UpdateStaticChargeResponse,

    AuthGetWalletResponse
)

class api:

    apikey: str

    def __new__(cls, apikey: str):
        setattr(cls, 'apikey', apikey)
        return cls

    class _utils:

        def __init__(self) -> None:
            self._base_url  = 'https://api.zebedee.io'
            self.apikey = api.apikey
            self._session   = ClientSession(headers=dict(apikey = api.apikey))

    class gamertag(_utils):

        async def send_payment(self, amount: millisatoshis, gamertag: str, description: str):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/gamertag/send_payment", json=dict(amount = str(amount), gamertag = gamertag, description = description)) as response:
                    return await response.json()
                    return GSendPaymentResponse(**await response.json())
                
        async def transaction(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/gamertag/transaction/" + zbd_id) as response:
                    return await response.json()
                    return TransactionResponse(**await response.json())
                
        async def charges(self, amount: millisatoshis, gamertag: str, description: str = 'Requesting Charge for Gamertag', expiresIn: int = 1800, internalId: Optional[str] = None, callbackUrl: Optional[str] = None):
            async with self._session as session:
                json = dict(amount = str(amount), gamertag = gamertag, description = description, expiresIn = expiresIn)
                if internalId is not None:
                    json['internalId'] = internalId
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl
                async with session.post(self._base_url + "/v0/gamertag/charges", json=json) as response:
                    return await response.json()
                    return ChargesResponse(**await response.json())
                
        async def get_id(self, gamertag: str):
            async with self._session as session:
                async with session.get(self._base_url + "/user-id/gamertag/" + gamertag) as response:
                    return await response.json()
                    return GetIdResponse(**await response.json())
                
        async def get_gamertag(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/gamertag/user-id/" + zbd_id) as response:
                    return await response.json()
                    return GetGamerTagResponse(**await response.json())
                
    class lightning(_utils):

        async def send_payment(self, amount: millisatoshis, lnAddress: str, comment: str = 'Sending to a Lightning Address', internalId: Optional[str] = None, callbackUrl: Optional[str] = None):
            async with self._session as session:
                json = dict(amount = str(amount), lnAddress = lnAddress, comment = comment)
                if internalId is not None:
                    json['internalId'] = internalId
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl
                async with session.post(self._base_url + "/v0/ln-address/send-payment", json=json) as response:
                    return await response.json()
                    return LSendPaymentResponse(**await response.json())
                
        async def validate(self, lnAddress: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/ln-address/validate/" + lnAddress) as response:
                    return await response.json()
                    return ValidateResponse(**await response.json())
                
        async def create_charge(self, lnaddress: str, amount: millisatoshis, description: str = ''):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/ln-address/fetch-charge", json=dict(lnaddress = lnaddress, amount = str(amount), description = description)) as response:
                    return await response.json()
                    return CreateChargeResponse(**await response.json())
    
    class email(_utils):

        async def send_payment(self, amount: millisatoshis, email: str, comment: str = 'Sending to a email'):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/email/send-payment", json=dict(amount = str(amount), email = email, comment = comment)) as response:
                    return await response.json()
                    return ESendPaymentResponse(**await response.json())
    
    class payments(_utils):

        async def send_payment(self, invoice: str, amount: millisatoshis = 0, description: str = 'Custom Payment Description', internalId: Optional[str] = None, callbackUrl: Optional[str] = None):
            async with self._session as session:
                json = dict(invoice = invoice, description = description)
                if internalId is not None:
                    json['internalId'] = internalId
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl
                if amount != 0:
                    json['amount'] = str(amount)
                async with session.post(self._base_url + "/v0/payments", json=json) as response:
                    return await response.json()
                    return PPaymentResponse(**await response.json())
        
        async def get_payment(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/payments/" + zbd_id) as response:
                    return await response.json()
                    return GetPaymentResponse(**await response.json())
                
    class charge(_utils):

        async def create_charge(self, amount: millisatoshis, description: str = 'My Charge Description', expiresIn: int = 1800, internalId: Optional[str] = None, callbackUrl: Optional[str] = None):
            async with self._session as session:
                json = dict(amount = str(amount), description = description, expiresIn = expiresIn)
                if internalId is not None:
                    json['internalId'] = internalId
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl                
                async with session.post(self._base_url + "/v0/charges", json=json) as response:
                    return await response.json()
                    return CCreateChargeResponse(**await response.json())
                
        async def get_charge(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/charges/" + zbd_id) as response:
                    return await response.json()
                    return GetChargeResponse(**await response.json())
        
        async def decode_charge(self, invoice: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/decode-invoice/" + invoice) as response:
                    return await response.json()
                    return DecodeChargeResponse(**await response.json())
    
    class withdrawal(_utils):

        async def create_withdrawal(self, amount: millisatoshis, description: str = 'Withdraw QR!', expiresIn: int = 1800, internalId: Optional[str] = None, callbackUrl: Optional[str] = None):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/withdrawal-requests", json=dict(amount= str(amount), description = description, expiresIn = expiresIn, internalId = internalId, callbackUrl = callbackUrl)) as response:
                    return await response.json()
                    return CreateWithdrawalResponse(**await response.json())
                
        async def get_withdrawal(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/withdrawal-requests/" + zbd_id) as response:
                    return await response.json()
                    return GetWithdrawalResponse(**await response.json())
                
    class voucher(_utils):

        async def create_voucher(self, amount: millisatoshis, description: str= 'Voucher for user.'):
            async with self._session as session:
                async with session.post(self._base_url + "/v1/create-voucher", json=dict(amount = str(amount), description = description)) as response:
                    return await response.json()
                    return CreateVoucherResponse(**await response.json())
                
        async def get_voucher(self, voucher_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/vouchers/" + voucher_id) as response:
                    return await response.json()
                    return GetVoucherResponse(**await response.json())
        
        async def redeem_voucher(self, code_voucher: str):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/redeem-voucher", json= dict(code = code_voucher)) as response:
                    return await response.json()
                    return RedeemVoucherResponse(**await response.json())
        
        async def revoke_voucher(self, code_voucher: str):
            async with self._session as session:
                async with session.post(self._base_url + "/v0/revoke-voucher", json=dict(code = code_voucher)) as response:
                    return await response.json()
                    return RevokeVoucherResponse(**await response.json())
    
    class wallet(_utils):

        async def get_wallet(self):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/wallet") as response:
                    return await response.json()
                    return GetWalletResponse(**await response.json())
    
    class static(_utils):

        async def create_static_charges(self, minAmount: millisatoshis, maxAmount: millisatoshis, description: str = 'Static Charge API', successMessage: str = 'Success', allowedSlots: int = 1000, internalId: Optional[str] = None, callbackUrl: Optional[str] = None, identifier: Optional[str] = None):
            async with self._session as session:
                json = dict(minAmount = str(minAmount), maxAmount = str(maxAmount), description = description, successMessage = successMessage, allowedSlots = allowedSlots)
                if internalId is not None:
                    json['internalId'] = internalId
                if identifier is not None:
                    json['identifier'] = identifier
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl
                async with session.post(self._base_url + "/v0/static-charges", json=json) as response:
                    return await response.json()
                    return CreateStaticChargeResponse(**await response.json())
        
        async def get_static_charge(self, zbd_id: str):
            async with self._session as session:
                async with session.get(self._base_url + "/v0/static-charges/" + zbd_id) as response:
                    return await response.json()
                    return GetStaticChargeResponse(**await response.json())

        async def update_static_charge(self, zbd_id: str, minAmount: millisatoshis, maxAmount: millisatoshis, description: str = 'Static Charge API', successMessage: str = 'Success', allowedSlots: int = 1000, internalId: Optional[str] = None, callbackUrl: Optional[str] = None, identifier: Optional[str] = None):
            async with self._session as session:
                json = dict(minAmount = minAmount, maxAmount = maxAmount, description = description, successMessage = successMessage, allowedSlots = allowedSlots)
                if internalId is not None:
                    json['internalId'] = internalId
                if identifier is not None:
                    json['identifier'] = identifier
                if callbackUrl is not None:
                    json['callbackUrl'] = callbackUrl
                async with session.patch(self._base_url + "/v0/static-charges/" + zbd_id, json=json) as response:
                    return await response.json()
                    return UpdateStaticChargeResponse(**await response.json())
                
    class keysend(_utils):
        pass

    class utility(_utils):
        pass

    # Authorization

    
        
