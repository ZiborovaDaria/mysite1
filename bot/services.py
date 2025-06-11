from django.conf import settings
from asgiref.sync import sync_to_async

@sync_to_async
def save_feedback_to_db(feedback_data):
    from bot.models import Feedback  # Локальный импорт
    
    return Feedback.objects.create(
        telegram_user_id=feedback_data['telegram_user_id'],
        username=feedback_data['username'],
        feedback_type=feedback_data['feedback_type'],
        rating=feedback_data['rating'],
        text=feedback_data['text'],
        store_id=feedback_data.get('store_id'),
        product_id=feedback_data.get('product_id')
    )

async def notify_operator(feedback, bot):
    from bot.models import Feedback  # Локальный импорт
    from asgiref.sync import sync_to_async
    
    operator_chat_id = settings.TELEGRAM_OPERATOR_CHAT_ID
    
    # Перезагружаем объект с отношениями
    full_feedback = await sync_to_async(Feedback.objects.select_related('store', 'product').get)(id=feedback.id)
    
    message_text = (
        "⚠️ Новый отзыв требует внимания!\n"
        f"Пользователь: {full_feedback.username}\n"
        f"Оценка: {full_feedback.rating}/5\n"
        f"Тип: {full_feedback.get_feedback_type_display()}\n"
    )
    
    if full_feedback.feedback_type == 'shop' and full_feedback.store:
        message_text += f"Магазин: {full_feedback.store.address}\n"
    elif full_feedback.feedback_type == 'product' and full_feedback.product:
        message_text += f"Товар: {full_feedback.product.name}\n"
    
    message_text += f"Текст: {full_feedback.text}"
    
    await bot.send_message(
        chat_id=operator_chat_id,
        text=message_text
    )
    
    # Обновляем статус
    full_feedback.forwarded_to_operator = True
    await sync_to_async(full_feedback.save)()