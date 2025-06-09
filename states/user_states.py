from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_favorite = State()
    waiting_for_name_prediction = State()
    waiting_for_remove_favorite = State()
