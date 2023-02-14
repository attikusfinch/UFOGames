from aiogram import types
from aiogram import Router
from keyboard.main_button import *
from database.wallet_db import Wallet
from database.withdraw_db import WithdrawHistory
from create_bot import _
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from keyboard.cancel_button import *

from keyboard.withdraw_button import get_withdraw_buttons
from handlers.profile.states import WithdrawState

from keyboard.cancel_button import *

from utils.ufo_wallet import UfoUtils
from database.users_db import UserWallet

start_withdraw_router = Router()

wallet_db = Wallet()
withdraw_db = WithdrawHistory()
user_wallet_db = UserWallet()

ufo_wallet = UfoUtils()

@start_withdraw_router.callback_query(F.data == "withdraw_button")
async def withdraw(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id

    wallet = await wallet_db.get_wallet(user_id)
    if wallet is None:
        await ctx.message.edit_text(_("👛 Привяжите кошелек"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    withdraw = await withdraw_db.get_withdraw_address(user_id)
    if withdraw is not None:
        await ctx.message.edit_text(_("👛 Ваш запрос на вывод обрабатывается"), reply_markup=await get_profile_button())
        await state.clear()
        return

    await ctx.message.edit_text(
        _("📤 Введите сумму UFO для вывода"),
        parse_mode="HTML",
        reply_markup=await get_cancel_button()
        )
    
    await state.set_state(WithdrawState.get_amount)

@start_withdraw_router.message(WithdrawState.get_amount)
@start_withdraw_router.callback_query(WithdrawState.get_amount)
async def get_amount(ctx: types.Message, state: FSMContext):
    user_id = ctx.from_user.id

    if isinstance(ctx, types.CallbackQuery):
        await ctx.message.edit_text(_("❌ Отмена"), reply_markup=await get_profile_button())
        await state.clear()
        return

    amount = ctx.text
    
    if amount.isdigit() is False:
        await ctx.reply(_("❌ Количество должно быть числом"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    amount = int(amount)
    
    await state.update_data(amount=amount)
    
    if amount < 1000:
        await ctx.reply(_("❌ Сумма должна быть больше 1000 UFO"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    UFO = await wallet_db.get_ufo(user_id)
    if UFO < amount:
        await ctx.reply(_("❌ Недостаточно UFO для вывода"), reply_markup=await get_profile_button())
        await state.clear()
        return
    
    wallet = await wallet_db.get_wallet(user_id)

    await ctx.reply(
        _("<b>📤 Подтверждение вывода</b>" + "\n" + "\n" +

        "Сумма: <code>{}</code> UFO" + "\n" + 
        "Комиссия: <code>1</code> UFO" + "\n" +
        "Адрес: <code>{}</code>").format(amount, wallet),
        parse_mode="HTML",
        reply_markup=await get_withdraw_buttons(user_id)
        )
    
    await state.set_state(WithdrawState.get_approve)

@start_withdraw_router.callback_query(WithdrawState.get_approve, F.data == "comfirm_withdraw_button")
async def accept_approve(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id
    
    data = await state.get_data()
    
    amount = data["amount"]
    
    withdraw_wallet = await wallet_db.get_wallet(user_id)
    
    tx_id = await ufo_wallet.withdraw(withdraw_wallet, amount-1) # - fee

    if tx_id is None:
        await ctx.answer(_("API перегруженно, попробуйте снова позже"), show_alert=True)
        return
    
    await wallet_db.set_ufo(user_id, amount, False)
    await withdraw_db.set_withdraw(user_id, withdraw_wallet, amount)
    
    await ctx.message.edit_text(_("<b>{} UFO</b> скоро будут переведены на ваш кошелек 👛").format(amount), parse_mode="HTML")
    await state.clear()

@start_withdraw_router.callback_query(WithdrawState.get_approve, F.data == "cancel_withdraw_button")
async def cancel_approve(ctx: types.CallbackQuery, state: FSMContext):
    user_id = ctx.from_user.id
    
    await ctx.message.edit_text(_("❌ Отмена"), parse_mode="HTML", reply_markup=await get_profile_button())
    await state.clear()