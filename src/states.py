from aiogram.fsm.state import StatesGroup, State


class PaymentStates(StatesGroup):
    card = State()
    crypto = State()
