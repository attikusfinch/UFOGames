from aiogram import Router
from keyboard.main_button import *
from create_bot import _
from aiogram import F, Router

from database.users_db import UserWallet
from database.wallet_db import Wallet

from create_bot import dp

from utils.ufo_wallet import UfoUtils
from settings import WALLET

from keyboard.withdraw_button import get_deposit_buttons
from aiogram import types
from aiogram.utils.markdown import hide_link

start_deposit_router = Router()

user_wallet_db = UserWallet()
ufo_wallet = UfoUtils()
wallet_db = Wallet()

@start_deposit_router.callback_query(F.data == "deposit_button")
async def deposit(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id
    
    address = await user_wallet_db.get_address(user_id)

    await ctx.message.edit_text(
        f"{hide_link(f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={address}')}" + "\n" +
        _("📥 Используйте адрес ниже для пополнения баланса." + "\n" + "\n" +

        "Монета: Uniform Fiscal Object (UFO)" + "\n" + "\n" + 

        "<code>{}</code>" + "\n" + "\n" + 
        
        "<b>ПЕРЕД ОТПРАВКОЙ ПЕРЕПРОВЕРЬТЕ ПРАВИЛЬНО-ЛИ ВЫ ВВЕЛИ АДРЕС КОШЕЛЬКА." + "\n" + 
        "МИНИМАЛЬНАЯ СУММА ПОПОЛНЕНИЯ 1000 UFO. 1 UFO БУДЕТ ИСПОЛЬЗОВАНО ДЛЯ ОПЛАТЫ КОМИССИИ.</b>").format(address),
        parse_mode="HTML",
        reply_markup=await get_deposit_buttons(user_id)
        )

@start_deposit_router.callback_query(F.data == "check_transactions")
async def check_transaction(ctx: types.CallbackQuery):
    user_id = ctx.from_user.id

    private = await user_wallet_db.get_private(user_id)

    balance = await ufo_wallet.get_balance(private)
    balance = round(balance)

    if balance < 1000:
        await ctx.message.edit_text(
            _("<b>Баланс должен быть больше 1000 UFO</b>" + "\n" +
                         "Чтобы UFO попали на ваш баланс пополните его на {} UFO").format(
                             1000-balance
                            )
                         , parse_mode="HTML"
                         , reply_markup=await get_deposit_buttons(user_id))
        return

    tx_id = await ufo_wallet.send(private, WALLET, balance-1)

    if tx_id is None:
        await ctx.answer(_("API перегруженно, попробуйте снова позже"), show_alert=True)
        return

    await wallet_db.set_ufo(user_id, balance-1)

    await dp.send_message(user_id, _("💸 Успешное пополнение {} UFO !").format(balance), parse_mode='HTML')