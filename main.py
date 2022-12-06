from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher , FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State


from config import TOKEN
from db import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

class User_States(StatesGroup):

    name = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


@dp.callback_query_handler(text='register_to_tournament')
async def cb_reg_new_user(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer('Напиши Имя.')

    await User_States.name.set()


dp.message_handler(state=User_States.name)
async def handle_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("А теперь напиши логин.")
    await User_States.lname()



if __name__ == '__main__':
    executor.start_polling(dp)