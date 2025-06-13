from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards import back_to_faq_keyboard, faq_keyboard, feedback_actions_keyboard
from bot.keyboards import main_kb, feedback_type_kb, cancel_kb, store_city_kb, stores_kb, products_kb, admin_kb

class FeedbackStates(StatesGroup):
    choosing_type = State()
    choosing_city = State()
    choosing_store = State()
    entering_product_name = State()
    choosing_product = State()
    choosing_rating = State()
    writing_text = State()
    forwarding_to_operator = State()

class AdminStates(StatesGroup):
    viewing_feedbacks = State()
    replying_to_feedback = State()

async def cmd_start(message: types.Message):
    await message.answer(
        "Вас приветствует компания ЕМЕХ-авто!\n"
        "Здесь вы можете узнать ответы на вопросы или оставить отзыв.",
        reply_markup=main_kb()
    )

# Обработчик FAQ
async def cmd_faq(message: types.Message):
    await message.answer(
        "Выберите интересующий вас вопрос:",
        reply_markup=faq_keyboard()
    )

# Обработчик нажатия на вопрос FAQ
async def show_faq_answer(callback: types.CallbackQuery):
    question_id = callback.data.split("_")[1]
    answers = {
        "1": "🔹 Как оформить заказ?\n\nВы можете оформить заказ:\n1. На нашем сайте через личный кабинет\n2. По телефону +7 (123) 456-7890\n3. В любом из наших магазинов",
        "2": "🔹 Как отменить заказ?\n\nЗаказ можно отменить:\n1. В личном кабинете на сайте (если статус заказа 'В обработке')\n2. По телефону +7 (123) 456-7890\n3. Через Telegram-бота",
        "3": "🔹 Как получить возврат?\n\nДля возврата товара:\n1. Сохраните чек и упаковку\n2. Обратитесь в сервисный центр\n3. Заполните заявление на возврат\nСрок рассмотрения - 3 рабочих дня",
        "4": "🔹 Сроки доставки?\n\nДоставка осуществляется в течение 1-5 рабочих дней в зависимости от региона:\n- Москва: 1-2 дня\n- Регионы: 3-5 дней\nСамовывоз - в день заказа",
        "5": "🔹 Гарантия на товар?\n\nГарантия предоставляется на срок от 6 до 36 месяцев в зависимости от категории товара. Подробности уточняйте у продавца."
    }
    
    await callback.message.edit_text(
        answers.get(question_id, "Информация обновляется"),
        reply_markup=back_to_faq_keyboard()
    )

# Возврат к списку вопросов
async def back_to_faq(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите интересующий вас вопрос:",
        reply_markup=faq_keyboard()
    )

async def cmd_contacts(message: types.Message):
    contact_info = (
        "📞 Контакты:\n\n"
        "Телефон: +7 (123) 456-7890\n"
        "Email: info@emex-auto.ru\n"
        "Адрес: г. Москва, ул. Автозапчастей, 15\n\n"
        "Часы работы:\n"
        "Пн-Пт: 9:00 - 20:00\n"
        "Сб-Вс: 10:00 - 18:00"
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
    from main.models import Store
    
    city_code = None
    city_choices = await sync_to_async(list)(Store.CITY_CHOICES)
    for code, name in city_choices:
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
    from main.models import Store
    
    data = await state.get_data()
    city_code = data['city']
    
    store = await sync_to_async(Store.objects.get)(city=city_code, address=message.text)
    await state.update_data(store_id=store.id)
    
    await state.set_state(FeedbackStates.choosing_rating)
    await message.answer("Оцените магазин от 1 до 5:", reply_markup=cancel_kb())

async def process_product_name(message: types.Message, state: FSMContext):
    from goods.models import Products
    
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
    from goods.models import Products
    
    data = await state.get_data()
    product_name = message.text
    
    product = await sync_to_async(Products.objects.get)(name=product_name)
    await state.update_data(product_id=product.id)
    
    await state.set_state(FeedbackStates.choosing_rating)
    await message.answer("Оцените товар от 1 до 5:", reply_markup=cancel_kb())

async def process_rating(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 1 <= int(message.text) <= 5:
        await message.answer("Пожалуйста, введите число от 1 до 5")
        return

    await state.update_data(rating=int(message.text))
    await state.set_state(FeedbackStates.writing_text)
    await message.answer("Напишите ваш отзыв:", reply_markup=cancel_kb())

async def process_feedback_text(message: types.Message, state: FSMContext, bot):
    from bot.services import save_feedback_to_db, notify_operator
    
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
    
    await message.answer(
        "🙏 Спасибо за ваш отзыв! Мы ценим ваше мнение и обязательно учтем его в нашей работе.\n\n"
        "Если у вас есть вопросы, вы можете связаться с оператором.",
        reply_markup=main_kb()
    )
    
    await notify_operator(feedback, bot)
    await state.clear()

async def forward_to_operator(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackStates.forwarding_to_operator)
    await message.answer(
        "Опишите ваш вопрос или проблему, которую нужно передать оператору:",
        reply_markup=cancel_kb()
    )

async def process_operator_message(message: types.Message, state: FSMContext, bot):
    from bot.services import save_operator_request
    
    request = await save_operator_request(
        message.from_user.id,
        message.from_user.full_name,
        message.text
    )
    
    await bot.send_message(
        chat_id=settings.TELEGRAM_OPERATOR_CHAT_ID,
        text=f"✉️ Новое обращение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}"
    )
    
    await message.answer(
        "Ваше сообщение передано оператору. Ожидайте ответа в этом чате.",
        reply_markup=main_kb()
    )
    await state.clear()

# Просмотр отзывов администратором
async def admin_view_feedbacks(message: types.Message, state: FSMContext):
    from bot.services import get_pending_feedbacks
    
    feedbacks = await get_pending_feedbacks()
    
    if not feedbacks:
        await message.answer("Нет отзывов для просмотра.", reply_markup=admin_kb())
        return
    
    await state.set_state(AdminStates.viewing_feedbacks)
    await state.update_data(feedbacks=feedbacks, current_index=0)
    await show_feedback(message, state)

# Отображение отзыва
async def show_feedback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    feedbacks = data['feedbacks']
    current_index = data['current_index']
    
    if current_index >= len(feedbacks):
        await message.answer("Просмотр отзывов завершен.", reply_markup=admin_kb())
        await state.clear()
        return
    
    feedback = feedbacks[current_index]
    feedback_text = await format_feedback(feedback)
    
    await message.answer(
        feedback_text,
        reply_markup=feedback_actions_keyboard(feedback.id)
    )

# Обработчик кнопки "Ответить"
async def admin_reply_to_feedback(callback: types.CallbackQuery, state: FSMContext):
    feedback_id = int(callback.data.split("_")[1])
    await state.set_state(AdminStates.replying_to_feedback)
    await state.update_data(feedback_id=feedback_id)
    
    await callback.message.answer(
        "Введите ваш ответ пользователю:",
        reply_markup=types.ReplyKeyboardRemove()
    )

# Обработчик ответа администратора
async def process_admin_reply(message: types.Message, state: FSMContext, bot):
    from bot.services import save_admin_reply, get_feedback_by_id
    
    if not message.text:
        await message.answer("Пожалуйста, введите текст ответа")
        return
    
    data = await state.get_data()
    feedback_id = data['feedback_id']
    
    try:
        # Сохраняем ответ
        feedback = await save_admin_reply(feedback_id, message.text)
        
        # Отправляем ответ пользователю
        await bot.send_message(
            chat_id=feedback.telegram_user_id,
            text=f"📩 Ответ администратора на ваш отзыв:\n\n{message.text}"
        )
        
        # Уведомляем администратора
        await message.answer(
            "✅ Ответ успешно отправлен пользователю.",
            reply_markup=admin_kb()
        )
        
        # Переходим к следующему отзыву
        feedbacks = data.get('feedbacks', [])
        current_index = data.get('current_index', 0) + 1
        
        if current_index < len(feedbacks):
            await state.update_data(current_index=current_index)
            await show_feedback(message, state)
        else:
            await message.answer("Больше нет отзывов для просмотра.", reply_markup=admin_kb())
            await state.clear()
            
    except Exception as e:
        await message.answer(
            f"❌ Ошибка при отправке ответа: {str(e)}",
            reply_markup=admin_kb()
        )
        await state.clear()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
        
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_kb())

async def format_feedback(feedback):
    feedback_type = "магазин" if feedback.feedback_type == "shop" else "товар"
    target = ""
    
    if feedback.feedback_type == "shop" and feedback.store:
        target = f"📍 Магазин: {feedback.store.address}\n"
    elif feedback.feedback_type == "product" and feedback.product:
        target = f"🛒 Товар: {feedback.product.name}\n"
    
    return (
        f"📝 Отзыв о {feedback_type}\n\n"
        f"{target}"
        f"⭐ Оценка: {feedback.rating}/5\n"
        f"📅 Дата: {feedback.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"👤 Пользователь: {feedback.username} (ID: {feedback.telegram_user_id})\n\n"
        f"📄 Текст отзыва:\n{feedback.text}"
    )