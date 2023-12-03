from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from src import messages as msg
from src.database import get_user, add_user
from src.keyboards import (
    menu_kb,
    create_profile_kb,
    create_categories_kb
)


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    m = msg.start_msg.format(username=message.from_user.username)

    await add_user({'id': message.from_user.id, 'username': message.from_user.username})
    await message.answer(text=m, reply_markup=menu_kb)


@router.message(Command('profile'))
@router.message(F.text.casefold() == 'профиль')
async def profile(message: types.Message):
    profile_kb = create_profile_kb()
    user = await get_user(message.from_user.id)
    m = msg.profile_msg.format(
        username=message.from_user.username,
        user_id=message.from_user.id,
        registration_date=user['registration_date'],
        balance=user['balance']
    )

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