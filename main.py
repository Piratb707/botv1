from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher , FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import *
from config import TOKEN
import db 

HELLO_MESSAGE = """
Добро пожаловать в личный кабинет!.
\nЕсли вам нужна инструкция по подключению нажми на - <b>/connect</b>.
Так же можно поддержать нас <b>донатом</b> - <b>/donate</b> .
"""
ACCOUNT_MESSAGE = """
Для просмотра списка участников выбери <b>"Просмотр участников"</b>.
Для регистрации на турнир выбери  <b>"Регистрация на турнир"</b>.
Для просмотра расписания игр выбери <b>"Расписание игр"</b>.
"""
NAVIGATION_MENU = """
Для возврата в меню нажмите - <b>/start</b>.
"""
GAME_ANNONCE = """
Пока ,что пусто.
"""

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

class User_States(StatesGroup):
    name = State()
    nlogin = State()

async def on_startup(_):
    await db.db_connect()
    print("""
    Подключение к БД выполнено....
    Звонок Лехе .....
    Добро получено !
    Отправка информации Серегей Михайловичу.
    """)

@dp.message_handler(commands=['connect'])
async def cmd_connenct(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                            text='Для начала тебе необходимо скачать клиент по ссылке https://clck.ru/32v9fV , далее вам необходимо добавить в игре в избранное сервер с адресом 109.248.250.45' + NAVIGATION_MENU, parse_mode="html")

@dp.message_handler(commands=['donate'])
async def cmd_donate(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                            text='Донат вы можете отправить на карту : \n<b>2200 7001 3485 8215 (Tinkoff)</b> \nОбязательно в коментарии указывайте на что вы отпарвили донат - автору или в призовой фонд .' + NAVIGATION_MENU, parse_mode="html")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Личный кабинет' + HELLO_MESSAGE+ ACCOUNT_MESSAGE + NAVIGATION_MENU,reply_markup=get_start_ikb(),parse_mode="html")

@dp.callback_query_handler(text='get_all_members')
async def cb_get_all_members(callback: types.CallbackQuery) -> None:
    members = await db.get_all_members()
    howmany = len(members)
    howmany = str(howmany)
    members = str(members)
    members = members.strip('[]').replace('(',' ').replace("'",'-|')
    members = members.replace(')','\n').replace(',',' ')

    if not members:
        await callback.message.delete()
        await callback.message.answer('Пусто')
    await callback.message.answer("Участники: \n" + '\n  ' + members + '\nВсего участников - ' + howmany + NAVIGATION_MENU,parse_mode="html")

@dp.callback_query_handler(text='add_new_member')
async def cb_reg_new_user(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer('Напиши своё Имя.')

    await User_States.name.set()

@dp.callback_query_handler(text='game_anonce')
async def cb_game_anonce(callback: types.CallbackQuery) -> None:
    await callback.message.answer(GAME_ANNONCE,parse_mode="html")

@dp.callback_query_handler(text='game_table')
async def cb_game_table(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Пока, что пусто.')

@dp.message_handler(state=User_States.name)
async def handle_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("А теперь напиши свой никнейм")
    await User_States.next()

@dp.message_handler(state=User_States.nlogin)
async def handle_nlogin(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['nlogin'] = message.text

    await db.register_to_tournament(state)  
    await message.reply('Вы добавлены в СПИСОК!' + NAVIGATION_MENU,parse_mode="html")

    await state.finish()
 
if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True,
                           on_startup=on_startup)