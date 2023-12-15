from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from src.utils import messages as msg
from src.utils.formatters import format_start, format_profile
from src.database import get_user, add_user
from src.keyboards import (
    menu_kb,
    create_profile_kb,
    create_categories_kb
)


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    m = format_start(message.from_user.username)

    await add_user({'id': message.from_user.id, 'username': message.from_user.username})
    await message.answer(text=m, reply_markup=menu_kb)


@router.message(Command('profile'))
@router.message(F.text.casefold() == 'профиль')
async def profile(message: types.Message):
    profile_kb = create_profile_kb()
    user = await get_user(message.from_user.id)
    m = format_profile(message.from_user.username, message.from_user.id, user['registration_date'], user['balance'])

    await message.answer(text=m, reply_markup=profile_kb)


@router.message(Command('help'))
@router.message(F.text.casefold() == 'помощь')
async def help(message: types.Message):
    await message.answer(text=msg.help_msg, reply_markup=menu_kb)


@router.message(Command('catalog'))
@router.message(F.text.casefold() == 'каталог')
async def catalog(message: types.Message):
    categories_kb = await create_categories_kb()

    await message.answer(text=msg.catalog_msg, reply_markup=categories_kb)
