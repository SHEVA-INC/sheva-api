import os

import requests
from prettytable import PrettyTable

def send_telegram_message(order):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    info_table = PrettyTable()
    info_table.field_names = ["Поле", "Дані"]
    info_fields = [
        ("Номер замовлення", order.id),
        ("Повне ім'я", order.full_name),
        ("Телефон", order.phone_number),
        ("Email", order.email),
        ("Регіон", order.region),
        ("Місто/Село", order.city_town),
        ("Номер відділення", order.post_office_number),
        ("Спосіб доставки", order.payment_method),
        ("Дата створення", order.created_at.strftime('%Y-%m-%d %H:%M')),
        ("Сума", order.total_price)
    ]
    for field, data in info_fields:
        info_table.add_row([field, data])

    cart_table = PrettyTable()
    cart_table.field_names = ["Назва", "Розмір", "Кількість"]
    for cart_product in order.cart.cartproduct_set.all():
        product = cart_product.product
        sizes = product.sizes.all()
        for size in sizes:
            cart_table.add_row([product.name, size.size, cart_product.quantity])

    text = (
        f"<b>Деталі замовлення:</b>\n<pre>{info_table.get_string()}</pre>\n"
        f"<b>Деталі кошика:</b>\n<pre>{cart_table.get_string()}</pre>"
    )

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(url, data=data)
    return response.json()