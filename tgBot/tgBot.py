from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup, default_state
import requests

router = Router()

kb = InlineKeyboardBuilder()
button = InlineKeyboardButton(text="Получить данные по товару", callback_data="artikul")
kb.add(button)

class MyStates(StatesGroup):
    wait_art = State()

@router.message(CommandStart, StateFilter(default_state))
async def start_bot(message: Message):
    await message.answer(text="Привет, нажми кнопку и отправь мне артикул товара на вб, а я пришлю актуальную информацию о нем",
                         reply_markup=kb.as_markup())

@router.callback_query(F.data == "artikul", StateFilter(default_state))
async def wait_artikul(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MyStates.wait_art)
    await callback.message.edit_text(text="Направьте мне артикул товара")

@router.message(StateFilter(MyStates.wait_art))
async def get_item_from_art(message: Message, state: FSMContext):
    await state.clear()
    artikul = int(message.text)
    result = requests.post(url='http://127.0.0.1:8000/api/v1/products', data={"artikul": artikul})
    await message.answer(text=result.text, reply_markup=kb.as_markup())

@router.message()
async def all_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Извините я не смог обработать ваше сообщение", reply_markup=kb.as_markup())