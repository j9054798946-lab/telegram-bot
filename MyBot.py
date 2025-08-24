# ЭТО БОТ ПО ТЕХНОЛОГИИ WEBHOOK:
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import logging
from flask import Flask, request, abort
import time
import requests
from telebot import apihelper

# Отключаем прокси (на Render.com не нужен)
# apihelper.proxy = None

# Включаем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота с токеном из переменной окружения
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logger.error("Токен не найден в переменных окружения!")
bot = telebot.TeleBot(TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Главное меню
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)

    # Первая кнопка на всю ширину
    video_button = InlineKeyboardButton("📹 Видеоматериалы", callback_data='video_menu')

    # Второй ряд
    contacts_button = InlineKeyboardButton("📞 Контакты", callback_data='contacts_menu')
    request_button = InlineKeyboardButton("✍️ Оставить заявку", callback_data='make_request')

    # Третий ряд
    reviews_button = InlineKeyboardButton("💬 Отзывы", callback_data='reviews_menu')
    faq_button = InlineKeyboardButton("❓ Частые вопросы", callback_data='faq_menu')

    # Четвертый ряд
    price_button = InlineKeyboardButton("💰 Прайс", callback_data='show_price')
    reserve_button = InlineKeyboardButton("🔒 Резерв", callback_data='reserve')

    markup.add(video_button)
    markup.add(contacts_button, request_button)
    markup.add(reviews_button, faq_button)
    markup.add(price_button, reserve_button)

    return markup

# Меню видеоматериалов
def video_menu():
    markup = InlineKeyboardMarkup(row_width=1)

    # Добавляем 5 условных ссылок
    for i in range(1, 6):
        button = InlineKeyboardButton(f"Ссылка {i}", callback_data=f'video_link_{i}')
        markup.add(button)

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')
    markup.add(back_button)

    return markup

# Меню контактов
def contacts_menu():
    markup = InlineKeyboardMarkup(row_width=1)

    # Кнопки контактов
    markup.add(InlineKeyboardButton("📍 Наш адрес", callback_data='contact_address'))
    markup.add(InlineKeyboardButton("📧 Email", callback_data='contact_email'))
    markup.add(InlineKeyboardButton("📱 Телефон", callback_data='contact_phone'))
    markup.add(InlineKeyboardButton("💬 Telegram", callback_data='contact_telegram'))
    markup.add(InlineKeyboardButton("🌐 Сайт", callback_data='contact_website'))

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')
    markup.add(back_button)

    return markup

# Меню отзывов
def reviews_menu():
    markup = InlineKeyboardMarkup(row_width=1)

    # Добавляем 5 условных ссылок
    for i in range(1, 6):
        button = InlineKeyboardButton(f"Отзыв {i}", callback_data=f'review_link_{i}')
        markup.add(button)

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')
    markup.add(back_button)

    return markup

# Меню частых вопросов
def faq_menu():
    markup = InlineKeyboardMarkup(row_width=1)

    # Добавляем вопросы
    questions = [
        "Как сделать заказ?",
        "Какие способы оплаты?",
        "Сколько идет доставка?",
        "Как вернуть товар?",
        "Есть ли скидки?"
    ]

    for i, question in enumerate(questions, 1):
        button = InlineKeyboardButton(f"Вопрос {i}: {question}", callback_data=f'faq_question_{i}')
        markup.add(button)

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')
    markup.add(back_button)

    return markup

# Меню оплаты
def payment_menu():
    markup = InlineKeyboardMarkup(row_width=2)

    # Варианты оплаты
    sbp_button = InlineKeyboardButton("💳 СБП (по номеру)", callback_data='payment_sbp')
    card_button = InlineKeyboardButton("💳 Банковская карта", callback_data='payment_card')

    markup.add(sbp_button, card_button)

    # Кнопка "Назад"
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')
    markup.add(back_button)

    return markup

# Меню прайс-листа с кнопкой "назад"
def price_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main_from_price')
    markup.add(back_button)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать! Выберите интересующий раздел:",
        reply_markup=main_menu()
    )

# Обработчик callback-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        # Главное меню
        if call.data == 'video_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "📹 Видеоматериалы:",
                reply_markup=video_menu()
            )
        
        # Контакты
        elif call.data == 'contacts_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "📞 Наши контакты:",
                reply_markup=contacts_menu()
            )
        
        # Оставить заявку
        elif call.data == 'make_request':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "✍️ Для оформления заявки на консультацию, пожалуйста, выберите способ оплаты:",
                reply_markup=payment_menu()
            )
        
        # Отзывы
        elif call.data == 'reviews_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💬 Отзывы наших клиентов:",
                reply_markup=reviews_menu()
            )
        
        # Частые вопросы
        elif call.data == 'faq_menu':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "❓ Частые вопросы:",
                reply_markup=faq_menu()
            )
        
        # Прайс (ИСПРАВЛЕННЫЙ БЛОК)
        elif call.data == 'show_price':
            bot.answer_callback_query(call.id)
            logger.info("Попытка отправить прайс-лист...")

            # Удаляем текущее сообщение с меню
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                logger.info("Сообщение с меню удалено")
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")

            # Небольшая задержка для надежности
            time.sleep(0.2)

            # Проверяем существование файла
            file_path = os.path.join(os.path.dirname(__file__), 'price.xlsx')
            if os.path.exists(file_path):
                logger.info("Файл price.xlsx найден")
                try:
                    with open(file_path, 'rb') as price_file:
                        bot.send_document(
                            call.message.chat.id,
                            price_file,
                            caption="💰 Актуальный прайс-лист на консультации",
                            reply_markup=price_menu()  # Добавляем кнопку "назад"
                        )
                    logger.info("Прайс-лист успешно отправлен")
                except Exception as e:
                    logger.error(f"Ошибка при отправке файла: {e}")
                    bot.send_message(
                        call.message.chat.id,
                        "❌ Произошла ошибка при отправке прайс-листа. Пожалуйста, попробуйте позже.",
                        reply_markup=main_menu()
                    )
            else:
                logger.error("Файл price.xlsx НЕ найден!")
                logger.error(f"Ищем файл по пути: {file_path}")
                logger.error(f"Текущая директория: {os.getcwd()}")
                logger.error(f"Файлы в директории: {os.listdir()}")
                bot.send_message(
                    call.message.chat.id,
                    "❌ Файл прайс-листа не найден. Пожалуйста, сообщите администратору.",
                    reply_markup=main_menu()
                )
        
        # Резерв
        elif call.data == 'reserve':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "🔒 Функция резервирования временно недоступна. Мы работаем над её внедрением!",
                reply_markup=main_menu()
            )
        
        # Возврат в главное меню
        elif call.data == 'back_to_main':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "👋 Главное меню:",
                reply_markup=main_menu()
            )
        
        # Возврат из прайс-листа
        elif call.data == 'back_to_main_from_price':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                logger.info("Сообщение с прайсом удалено")
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения с прайсом: {e}")
                bot.send_message(
                    call.message.chat.id,
                    "⚠️ Не удалось удалить предыдущее сообщение",
                    reply_markup=main_menu()
                )
                return
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "👋 Главное меню:",
                reply_markup=main_menu()
            )
        
        # Ссылки на видео
        elif call.data.startswith('video_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"📹 Вот ссылка {link_num}: [Перейти](https://example.com/video{link_num})", parse_mode='Markdown')
        
        # Ссылки на отзывы
        elif call.data.startswith('review_link_'):
            link_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"💬 Вот отзыв {link_num}: [Читать](https://example.com/review{link_num})", parse_mode='Markdown')
        
        # Вопросы FAQ
        elif call.data.startswith('faq_question_'):
            q_num = call.data.split('_')[-1]
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"❓ Ответ на вопрос {q_num}: Ответ")
        
        # Контакты
        elif call.data.startswith('contact_'):
            contact_type = call.data.split('_')[-1]
            contact_info = {
                'address': '📍 Наш адрес: г. Москва, ул. Примерная, д. 1, офис 123',
                'email': '📧 Email: info@yourcompany.com',
                'phone': '📱 Телефон: +7 905 479-89-46',
                'telegram': '💬 Telegram: @yourcompany',
                'website': '🌐 Сайт: https://yourcompany.com'
            }
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, contact_info.get(contact_type, "Информация недоступна"))
        
        # Оплата СБП
        elif call.data == 'payment_sbp':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💳 *Оплата через Систему Быстрых Платежей (СБП)*\n\n"
                "Для оплаты консультации:\n"
                "1. Откройте приложение вашего банка\n"
                "2. Перейдите в раздел «Платежи» → «СБП»\n"
                "3. Введите номер телефона: `+7 905 479-89-46`\n"
                "4. Укажите сумму согласно прайсу\n"
                "5. В комментарии укажите: `Консультация Telegram`\n\n"
                "После оплаты отправьте нам скриншот чека для подтверждения.",
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
        
        # Оплата картой
        elif call.data == 'payment_card':
            bot.answer_callback_query(call.id)
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                logger.error(f"Ошибка удаления сообщения: {e}")
            
            time.sleep(0.1)
            
            bot.send_message(
                call.message.chat.id,
                "💳 *Оплата банковской картой*\n\n"
                "Для оплаты консультации:\n"
                "1. Перейдите по ссылке для оплаты: [Оплатить картой](https://example.com/payment)\n"
                "2. Укажите сумму согласно прайсу\n"
                "3. В комментарии укажите: `Консультация Telegram`\n\n"
                "После оплаты отправьте нам скриншот чека для подтверждения.",
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
    
    except Exception as e:
        logger.error(f"Ошибка в обработчике callback: {e}")
        bot.answer_callback_query(call.id, text="Произошла ошибка. Пожалуйста, попробуйте позже.", show_alert=True)

# Вебхук для Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            logger.info(f"JSON: {json_string}")
            
            # Используем альтернативный способ обработки
            import telebot
            update = telebot.util.update_de_json(json_string)
            bot.process_new_updates([update])
            
            return ''
        else:
            abort(403)
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        return "Error", 500

# Установка вебхука
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    # Динамически определяем URL текущего приложения
    from flask import request
    webhook_url = request.url_root + 'webhook'
    
    logger.info(f"Установка webhook на URL: {webhook_url}")
    
    bot.remove_webhook()
    s = bot.set_webhook(url=webhook_url)
    
    if s:
        logger.info(f"Webhook успешно установлен на {webhook_url}")
        return f"Webhook set to {webhook_url}"
    else:
        logger.error("Не удалось установить webhook")
        return "Failed to set webhook"

# Главная страница для проверки
@app.route('/')
def index():
    return "Hello, this is a Telegram bot!"

# Обработчик для удаления вебхука
@app.route('/remove_webhook', methods=['GET', 'POST'])
def remove_webhook():
    bot.remove_webhook()
    return "Webhook removed"

# Запуск без SSL для локальной разработки
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # ... весь предыдущий код ...

# Маршрут для запуска polling (альтернатива webhook)
@app.route('/start_polling', methods=['GET'])
def start_polling():
    try:
        # Удаляем webhook, если он был установлен
        bot.remove_webhook()
        logger.info("Webhook удален")
        
        # Запускаем polling в отдельном потоке
        def polling_worker():
            logger.info("Запуск polling...")
            bot.infinity_polling()
        
        # Запускаем поток как демон (чтобы не мешать основному приложению)
        polling_thread = threading.Thread(target=polling_worker, daemon=True)
        polling_thread.start()
        
        logger.info("Polling запущен в фоновом режиме")
        return "✅ Polling started successfully"
        
    except Exception as e:
        logger.error(f"Ошибка при запуске polling: {e}")
        return f"❌ Error starting polling: {e}", 500