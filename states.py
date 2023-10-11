from aiogram.dispatcher.filters.state import StatesGroup, State


class MainStates(StatesGroup):
    profile = State()
    help = State()
    catalog = State()
    my_purchases = State()


class PaymentStates(StatesGroup):
    card = State()
    crypto = State()


class Items(StatesGroup):
    item = State()
