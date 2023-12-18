from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart

from src.database import add_user, get_categories, get_user
from src.keyboards import create_categories_kb, create_profile_kb, menu_kb
from src.utils import messages as msg
from src.utils.formatters import format_profile, format_start

router = Router()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    m = format_start(message.from_user.username)

    await add_user({'id': message.from_user.id, 'username': message.from_user.username})
    await message.answer(text=m, reply_markup=menu_kb)


@router.message(Command('profile'))
@router.message(F.text.casefold() == 'профиль')
async def profile(message: types.Message) -> None:
    profile_kb = create_profile_kb()
    user = await get_user(message.from_user.id)
    m = format_profile(message.from_user.username, message.from_user.id, user['registration_date'], user['balance'])

    await message.answer(text=m, reply_markup=profile_kb)


@router.message(Command('help'))
@router.message(F.text.casefold() == 'помощь')
async def rules(message: types.Message) -> None:
    await message.answer(text=msg.rules_msg, reply_markup=menu_kb)


@router.message(Command('catalog'))
@router.message(F.text.casefold() == 'каталог')
async def catalog(message: types.Message) -> None:
    categories = await get_categories()
    categories_kb = create_categories_kb(categories)

    await message.answer(text=msg.catalog_msg, reply_markup=categories_kb)
