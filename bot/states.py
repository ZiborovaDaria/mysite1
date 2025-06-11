from aiogram.fsm.state import StatesGroup, State

class FeedbackStates(StatesGroup):
    choosing_type = State()
    choosing_city = State()
    choosing_store = State()
    entering_product_name = State()
    choosing_product = State()
    choosing_rating = State()
    writing_text = State()
    forwarding_to_operator = State()