# telegram_bot.py
from telegram import Bot
from django.conf import settings
from asgiref.sync import sync_to_async

@sync_to_async
def send_telegram_notification_async(order_data):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHANNEL_ID

    bot = Bot(token=bot_token)

    message = f"New Order Received!\n\n"
    message += f"Name: {order_data['first_name']} {order_data['last_name']}\n"
    message += f"Address: {order_data['address']}, {order_data['apartment']}, {order_data['city']}, {order_data['postal_code']}\n"
    message += f"Phone: {order_data['phone']}\n\n"
    message += "Products:\n"
    for product in order_data['products']:
        message += f"- {product['title']} - Quantity: {product['quantity']}\n"
    message += f"\nTotal Price: ${order_data['total_price']}"

    bot.send_message(chat_id=chat_id, text=message)

# Wrap the asynchronous function with sync_to_async
send_telegram_notification = sync_to_async(send_telegram_notification_async, thread_sensitive=True)
