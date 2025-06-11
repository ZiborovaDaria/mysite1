from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async


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

async def store_city_kb():
    from main.models import Store  # Локальный импорт
    
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
    from main.models import Store  # Локальный импорт
    
    stores = await sync_to_async(list)(Store.objects.filter(city=city_code))
    
    keyboard = [
        [KeyboardButton(text=store.address)] for store in stores
    ]
    keyboard.append([KeyboardButton(text="Отмена")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
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