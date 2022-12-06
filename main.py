from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher , FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import get_start_ikb, members_cb,get_start_kb
from config import TOKEN
import db 

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
class User_States(StatesGroup):

    name = State()

async def on_startup(_):
    await db.db_connect()
    print('Подключение к БД выполнено')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                            text='Добро пожаловать',
                            reply_markup=get_start_kb())


@dp.message_handler(commands=['account'])
async def process_start_command(message: types.Message):
    await message.answer(text='Личный кабинет',reply_markup=get_start_ikb())

@dp.callback_query_handler(text='get_all_members')
async def cb_get_all_members(callback: types.CallbackQuery) -> None:
    members = await db.get_all_members()

    if not members:
        await callback.message.answer('Нет нихуя')
        await callback.answer()



@dp.callback_query_handler(text='add_new_member')
async def cb_reg_new_user(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer('Напиши Имя.')

    await User_States.name.set()

dp.message_handler(state=User_States.name)
async def handle_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("А теперь напиши логин.")
    await User_States.name()

if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True,
                           on_startup=on_startup)