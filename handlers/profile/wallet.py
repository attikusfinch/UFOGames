from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from database.wallet_db import Wallet
from create_bot import _
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from keyboard.cancel_button import *

from handlers.profile.states import WalletState

start_wallet_router = Router()

wallet_db = Wallet()

@start_wallet_router.callback_query(F.data == "connect_wallet_button")
async def set_wallet(ctx: types.CallbackQuery, state: FSMContext):    
    await ctx.message.edit_text(
        _("✍️ Введите адрес своего кошелька." + "\n" + "\n" + 

	    "<b>⚠️ Внимание! Используйте только адрес к которому у вас есть доступ по seed-фразе.</b>" + "\n" + "\n" +

	    "🚫 Не используйте адреса, выданные вам такими сервисами как: Graviex, Hotbit."), 
        parse_mode="HTML", 
        reply_markup=await get_profile_button()
    )

    await state.set_state(WalletState.get_wallet)

@start_wallet_router.message(WalletState.get_wallet)
async def get_wallet(ctx: types.Message, state: FSMContext):
    user_id = ctx.from_user.id
    
    wallet = ctx.text
    
    if "0" in wallet:
        await ctx.reply(
            _("❗️ Кошельки uf1 не поддерживаются"),
            reply_markup=await get_profile_button()
            )
        await state.clear()
        return
    
    if not wallet.startswith(("U", "u", "C")):
        await ctx.reply(
            _("❗️ Кошелек указан не верно, попробуйте снова"),
            reply_markup=await get_profile_button()
            )
        await state.clear()
        return
    
    response = await wallet_db.set_wallet(user_id, wallet)
    
    if response is None:
        await ctx.reply(
            _("❗️ Введите /start"),
            reply_markup=await get_profile_button()
        )
        await state.clear()
        return

    await ctx.reply(
        _("✅ Кошелек успешно закреплен за вашим аккаунтом, теперь вы можете выводить ваши UFO."),
        parse_mode="HTML",
        reply_markup=await get_profile_button()
    )
    await state.clear()