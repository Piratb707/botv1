from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

members_cb = CallbackData('user','id','action')

def get_start_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр участников', callback_data='get_all_members')],
        [InlineKeyboardButton('Регистрация на турнир', callback_data='add_new_member')]
        ])

    return ikb

def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [InlineKeyboardButton('/account')]
    ], resize_keyboard=True)

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [InlineKeyboardButton('/cancel')]
    ], resize_keyboard=True)

    return kb