from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher , FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import get_start_ikb, members_cb, get_start_kb, get_cancel_kb
from config import TOKEN
import db 

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

class User_States(StatesGroup):
    name = State()
    nlogin = State()

async def on_startup(_):
    await db.db_connect()
    print('Подключение к БД выполнено')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                            text='Добро пожаловать',
                            reply_markup=get_start_kb())

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.answer('Зассал...',
        reply_markup=get_cancel_kb())           


@dp.message_handler(commands=['account'])
async def process_start_command(message: types.Message):
    await message.answer(text='Личный кабинет',reply_markup=get_start_ikb())

@dp.callback_query_handler(text='get_all_members')
async def cb_get_all_members(callback: types.CallbackQuery) -> None:
    members = await db.get_all_members()

    if not members:
        await callback.message.delete()
        await callback.message.answer('Нет нихуя')
    await callback.message.answer(members)

@dp.callback_query_handler(text='add_new_member')
async def cb_reg_new_user(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer('Напиши своё Имя.',
                                  reply_markup=get_cancel_kb())

    await User_States.name.set()

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
    await message.reply('Вы добавлены в СПИСОК!')

    await state.finish()
 


if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True,
                           on_startup=on_startup)