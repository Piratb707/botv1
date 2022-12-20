from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

members_cb = CallbackData('user','id','action')

def get_start_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр участников', callback_data='get_all_members')],
        [InlineKeyboardButton('Регистрация на турнир', callback_data='add_new_member')],
        [InlineKeyboardButton('Расписание игр', callback_data='game_anonce')],
        [InlineKeyboardButton('Турнирная таблица', callback_data='game_table')]
        ])

    return ikb

def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [InlineKeyboardButton('/start')]
    ], resize_keyboard=True)

    return kb