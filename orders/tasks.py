import requests
from django.conf import settings


def send_order_to_telegram(order):
    text = f"🛒 Yangi buyurtma!\n\n"
    text += f"👤 Foydalanuvchi: {order.user.username}\n"
    text += f"📞 Tel: {order.phone_number}\n"
    text += f"💳 To‘langan: {'✅' if order.is_paid else '❌'}\n"
    text += f"📦 Status: {order.status}\n\n"
    text += f"📚 Kitoblar:\n"

    total = 0
    for item in order.items.all():
        subtotal = item.quantity * item.book.price
        total += subtotal
        text += f"  • {item.book.title} — {item.quantity} × {item.book.price} = {subtotal} so‘m\n"

    text += f"\n💰 Umumiy: {total} so‘m"

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload, timeout=5)
    except requests.RequestException:
        pass
