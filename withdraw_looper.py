from database.withdraw_db import WithdrawHistory

from utils.ufo_wallet import UfoUtils

import asyncio

headers = {'accept': '*/*','Content-Type': 'application/json',}

withdraw_db = WithdrawHistory()
ufo_wallet = UfoUtils()

async def withdraw_ufo(user_id, address, count):
    response = await ufo_wallet.withdraw(address, count)

    if response is not None:
        print(response)
        print(f"💸 Вывод {count} UFO на кошелёк {address} прошел успешно | {user_id}\n{response}")
        
        return True
    else:
        print(response)
        print(f"😢 Ошибка отпраки токенов на кошелёк: {address} | {user_id}" + "\n" + 
                              "Сообщите в тех. поддержку")

        return False

async def main():
    while True:
        queue = await withdraw_db.get_all_addresses()

        if len(queue) == 0:
            await asyncio.sleep(30)

        for user in queue:
            withdraw = await withdraw_ufo(user[1], user[2], user[3])
            if withdraw:
                await withdraw_db.delete_withdraw(user[1])
            await asyncio.sleep(5)

        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())