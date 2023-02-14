import ufobit
from settings import wallet_private

class UfoUtils:
    async def create_wallet(self):
        wallet = ufobit.Key()
        
        return wallet.get_sw_address(), wallet.to_wif()

    async def get_balance(self, private: str):
        wallet = ufobit.Key(private)
        
        try:
            balance = await wallet.get_balance("ufo")
        except ConnectionError:
            return None

        return float(balance)
    
    async def withdraw(self, address: str, amount: int):
        return await self.send(wallet_private, address, amount)

    async def send(self, private: str, address: str, amount: int):
        outputs = [ # destination address
            (address, amount, 'ufo'),
        ]
        
        user_wallet = ufobit.Key(private)
        
        try:
            unspents = await user_wallet.get_unspents()
            tx_id = await user_wallet.send(outputs=outputs ,unspents=unspents)
        except ConnectionError as error:
            print(error)
            return None

        return tx_id