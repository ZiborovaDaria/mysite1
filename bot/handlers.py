from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hbold

from bot.keyboards import main_kb, feedback_type_kb, cancel_kb, store_city_kb, stores_kb, products_kb


class FeedbackStates(StatesGroup):
    choosing_type = State()
    choosing_city = State()
    choosing_store = State()
    entering_product_name = State()
    choosing_product = State()
    choosing_rating = State()
    writing_text = State()
    forwarding_to_operator = State()

async def cmd_start(message: types.Message):
    await message.answer(
        "Вас приветствует компания ЕМЕХ-авто!\n"
        "Здесь вы можете узнать ответы на вопросы или оставить отзыв.",
        reply_markup=main_kb()
    )

async def cmd_faq(message: types.Message):
    faq_text = (
        "Часто задаваемые вопросы:\n"
        "1. Как оформить заказ? - Через сайт или по телефону\n"
        "2. Как отменить заказ? - В личном кабинете или по телефону\n"
        "3. Как получить возврат? - Обратитесь в сервисный центр\n"
        "4. Сроки доставки? - От 1 до 5 рабочих дней\n"
    )
    await message.answer(faq_text)

async def cmd_contacts(message: types.Message):
    contact_info = (
        "Контакты:\n"
        "Телефон: +7 (123) 456-7890\n"
        "Email: info@emex-auto.ru\n"
        "Адрес: г. Москва, ул. Автозапчастей, 15"
    )
    await message.answer(contact_info)

async def start_feedback(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackStates.choosing_type)
    await message.answer(
        "О чем вы хотите оставить отзыв?",
        reply_markup=feedback_type_kb()
    )

async def process_feedback_type(message: types.Message, state: FSMContext):
    if message.text not in ["О магазине", "О товаре"]:
        await message.answer("Пожалуйста, выберите тип отзыва из кнопок ниже")
        return

    feedback_type = "shop" if message.text == "О магазине" else "product"
    await state.update_data(feedback_type=feedback_type)
    
    if feedback_type == "shop":
        await state.set_state(FeedbackStates.choosing_city)
        await message.answer("Выберите город:", reply_markup=await store_city_kb())
    else:
        await state.set_state(FeedbackStates.entering_product_name)
        await message.answer("Введите название товара для поиска:", reply_markup=cancel_kb())

async def process_city(message: types.Message, state: FSMContext):
    from main.models import Store  # Локальный импорт
    
    city_code = None
    for code, name in Store.CITY_CHOICES:
        if name == message.text:
            city_code = code
            break
    
    if not city_code:
        await message.answer("Пожалуйста, выберите город из списка")
        return
        
    await state.update_data(city=city_code)
    await state.set_state(FeedbackStates.choosing_store)
    await message.answer(
        "Выберите магазин:", 
        reply_markup=await stores_kb(city_code)
    )

async def process_store(message: types.Message, state: FSMContext):
    from main.models import Store  # Локальный импорт
    from asgiref.sync import sync_to_async

    data = await state.get_data()
    city_code = data['city']
    
    store = await sync_to_async(Store.objects.get)(city=city_code, address=message.text)
    await state.update_data(store_id=store.id)
    
    await state.set_state(FeedbackStates.choosing_rating)
    await message.answer("Оцените магазин от 1 до 5:", reply_markup=cancel_kb())

async def process_product_name(message: types.Message, state: FSMContext):
    from goods.models import Products  # Локальный импорт
    from asgiref.sync import sync_to_async

    query = message.text
    products = await sync_to_async(list)(Products.objects.filter(name__icontains=query)[:5])
    
    if not products:
        await message.answer("Товары не найдены. Уточните запрос:")
        return
        
    await state.update_data(product_query=query)
    await state.set_state(FeedbackStates.choosing_product)
    await message.answer(
        "Выберите товар:", 
        reply_markup=products_kb(products)
    )

async def process_product_choice(message: types.Message, state: FSMContext):
    from goods.models import Products  # Локальный импорт
    from asgiref.sync import sync_to_async

    data = await state.get_data()
    product_name = message.text
    
    product = await sync_to_async(Products.objects.get)(name=product_name)
    await state.update_data(product_id=product.id)
    
    await state.set_state(FeedbackStates.choosing_rating)
    await message.answer("Оцените товар от 1 до 5:", reply_markup=cancel_kb())

async def process_feedback_text(message: types.Message, state: FSMContext):
    from bot.services import save_feedback_to_db, notify_operator  # Локальный импорт
    
    data = await state.get_data()
    
    feedback_data = {
        'telegram_user_id': message.from_user.id,
        'username': message.from_user.full_name,
        'feedback_type': data.get('feedback_type'),
        'rating': data.get('rating'),
        'text': message.text,
        'store_id': data.get('store_id'),
        'product_id': data.get('product_id'),
    }
    
    feedback = await save_feedback_to_db(feedback_data)

async def process_rating(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 1 <= int(message.text) <= 5:
        await message.answer("Пожалуйста, введите число от 1 до 5")
        return

    await state.update_data(rating=int(message.text))
    await state.set_state(FeedbackStates.writing_text)
    await message.answer("Напишите ваш отзыв:", reply_markup=cancel_kb())


async def forward_to_operator(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackStates.forwarding_to_operator)
    await message.answer("Опишите проблему, которую нужно передать оператору:", reply_markup=cancel_kb())

async def process_operator_message(message: types.Message, state: FSMContext):
    # Здесь можно сохранить обращение к оператору в базу
    await message.answer("Ваше сообщение передано оператору. Ожидайте ответа.", reply_markup=main_kb())
    await state.clear()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
        
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_kb())