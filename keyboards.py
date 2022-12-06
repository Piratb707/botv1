from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

members_cb = CallbackData('user','id','action')

def get_start_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр участиков', callback_data='get_all_members')],
        [InlineKeyboardButton('Регистрация на турнир', callback_data='add_new_member')]
        ])

    return ikb