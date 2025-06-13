from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

# Синхронные клавиатуры (без await)
def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Часто задаваемые вопросы")],
            [KeyboardButton(text="Контакты")],
            [KeyboardButton(text="Оставить отзыв")],
            [KeyboardButton(text="Связаться с оператором")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

def admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Просмотреть отзывы")],
            [KeyboardButton(text="В главное меню")]
        ],
        resize_keyboard=True
    )

def feedback_type_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="О магазине")],
            [KeyboardButton(text="О товаре")],
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True
    )

def products_kb(products):
    keyboard = [
        [KeyboardButton(text=product.name)] for product in products
    ]
    keyboard.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def faq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Как оформить заказ?", callback_data="faq_1")],
            [InlineKeyboardButton(text="Как отменить заказ?", callback_data="faq_2")],
            [InlineKeyboardButton(text="Как получить возврат?", callback_data="faq_3")],
            [InlineKeyboardButton(text="Сроки доставки?", callback_data="faq_4")],
            [InlineKeyboardButton(text="Гарантия на товар?", callback_data="faq_5")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ]
    )

def back_to_faq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад к вопросам", callback_data="back_to_faq")]
        ]
    )

# Асинхронные клавиатуры (с await)
async def store_city_kb():
    from main.models import Store
    
    cities = await sync_to_async(list)(Store.objects.values_list('city', flat=True).distinct())
    city_names = [dict(Store.CITY_CHOICES).get(city) for city in cities]
    
    keyboard = [
        [KeyboardButton(text=city)] for city in city_names
    ]
    keyboard.append([KeyboardButton(text="Отмена")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

async def stores_kb(city_code):
    from main.models import Store
    
    stores = await sync_to_async(list)(Store.objects.filter(city=city_code))
    
    keyboard = [
        [KeyboardButton(text=store.address)] for store in stores
    ]
    keyboard.append([KeyboardButton(text="Отмена")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def feedback_actions_keyboard(feedback_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Ответить", callback_data=f"reply_{feedback_id}")],
            [InlineKeyboardButton(text="➡️ Следующий", callback_data="next_feedback")]
        ]
    )