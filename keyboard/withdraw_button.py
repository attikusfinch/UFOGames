from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from create_bot import _


async def get_deposit_buttons(address):
    markup = InlineKeyboardBuilder()
    
    markup.row(
        InlineKeyboardButton(text=_("EDGE WALLET"), url=f"https://deep.edge.app/pay/ufo/{address}"),
        width=1)

    markup.row(
            InlineKeyboardButton(text=_("🔄 Проверить"), callback_data="check_transactions"),
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("назад"), callback_data="profile_button"), 
            width=1)
    
    return markup.as_markup(resize_keyboard=True)

async def get_withdraw_buttons(user_id):
    markup = InlineKeyboardBuilder()
    
    markup.row(
            InlineKeyboardButton(text=_("✅ Подтвердить"), callback_data="comfirm_withdraw_button"), 
            width=1)
    
    markup.row(
            InlineKeyboardButton(text=_("❌ Отменить"), callback_data="cancel_withdraw_button"),
            width=1)
    
    return markup.as_markup(resize_keyboard=True)