from django.conf import settings
from asgiref.sync import sync_to_async
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models import Feedback

@sync_to_async
def save_feedback_to_db(feedback_data):
    from bot.models import Feedback
    
    return Feedback.objects.create(
        telegram_user_id=feedback_data['telegram_user_id'],
        username=feedback_data['username'],
        feedback_type=feedback_data['feedback_type'],
        rating=feedback_data['rating'],
        text=feedback_data['text'],
        store_id=feedback_data.get('store_id'),
        product_id=feedback_data.get('product_id')
    )

async def notify_operator(feedback, bot: Bot):
    from bot.models import Feedback
    
    full_feedback = await sync_to_async(Feedback.objects.select_related('store', 'product').get)(id=feedback.id)
    
    message_text = (
        "⚠️ Новый отзыв требует внимания!\n\n"
        f"Тип: {full_feedback.get_feedback_type_display()}\n"
        f"Оценка: {full_feedback.rating}/5\n"
        f"Пользователь: {full_feedback.username} (ID: {full_feedback.telegram_user_id})\n"
    )
    
    if full_feedback.feedback_type == 'shop' and full_feedback.store:
        message_text += f"Магазин: {full_feedback.store.address}\n"
    elif full_feedback.feedback_type == 'product' and full_feedback.product:
        message_text += f"Товар: {full_feedback.product.name}\n"
    
    message_text += f"\nТекст отзыва:\n{full_feedback.text}"
    
    await bot.send_message(
        chat_id=settings.TELEGRAM_OPERATOR_CHAT_ID,
        text=message_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Ответить пользователю",
                callback_data=f"admin_reply_{full_feedback.id}"
            )]
        ])
    )

@sync_to_async
def get_all_feedbacks():
    from bot.models import Feedback
    return list(Feedback.objects.select_related('store', 'product').order_by('-created_at'))

@sync_to_async
def get_pending_feedbacks():
    return list(Feedback.objects.filter(admin_reply__isnull=True).order_by('-created_at'))

@sync_to_async
def get_feedback_by_id(feedback_id):
    return Feedback.objects.get(id=feedback_id)

@sync_to_async
def save_admin_reply(feedback_id, reply_text):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.admin_reply = reply_text
    feedback.is_answered = True
    feedback.save()
    return feedback

@sync_to_async
def save_operator_request(user_id, username, message):
    from bot.models import OperatorRequest
    return OperatorRequest.objects.create(
        user_id=user_id,
        username=username,
        message=message
    )