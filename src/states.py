from aiogram.fsm.state import State, StatesGroup


class PaymentStates(StatesGroup):
    card = State()
    crypto = State()
