
from telebot import TeleBot
from buttons import *
import database as db
from geopy import Photon
bot = TeleBot("7783979252:AAGzXkaSPhUExNGAA-XnzJxbcK00D-Jcd4I")

#db.add_product("Чикенбургер", 30000.0, "Вкусная булочка в булочке", 10,  "https://www.foodandwine.com/thmb/DI29Houjc_ccAtFKly0BbVsusHc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/crispy-comte-cheesburgers-FT-RECIPE0921-6166c6552b7148e8a8561f7765ddf20b.jpg")
#db.add_product("Даблбургер", 50000.0, "Две вкусно котлеты в булочке", 10,  "https://www.foodandwine.com/thmb/pwFie7NRkq4SXMDJU6QKnUKlaoI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Ultimate-Veggie-Burgers-FT-Recipe-0821-5d7532c53a924a7298d2175cf1d4219f.jpg")
#db.add_product("Хот-дог", 20000.0, "сосиска в булочке", 0, "https://d2j6dbq0eux0bg.cloudfront.net/images/14450072/1156014693.jpg")
# объект работающий с локацией
geolocator = Photon(user_agent="geo-locator", timeout=10)
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_bt())
    elif checker == False:
        bot.send_message(user_id, "Добро пожаловать в бот доставки!\n"
                                  "Пожалуйста, введите свое имя")
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f"Отлично, {name}. Пожалуйста, отправьте свой номер",
                     reply_markup=phone_number_bt())
    # отправляем его в функцию получения номера вместе с информацией об имени
    bot.register_next_step_handler(message, get_phone, name)
# принимаю это имя в параметр name
def get_phone(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        db.add_user(user_id, name, phone_number)
        bot.send_message(user_id, f"Вы успешно прошли регистрацию, {name}!\n"
                                  f"Ваш номер: {phone_number}")
        # bot.send_message(user_id, "Отправьте свою локацию", reply_markup=location_bt())
        # bot.register_next_step_handler(message, get_location)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку в меню.",
                         reply_markup=phone_number_bt())
        # отправляем пользователя в эту же функцию, пока он не отправить номер через кнопку
        bot.register_next_step_handler(message, get_phone, name)
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        # получаем долготу и широту
        longitude = message.location.longitude
        latitude = message.location.latitude
        # преобразуем данные в адрес
        address = geolocator.reverse((latitude, longitude)).address
        bot.send_message(user_id, f"Ваш адрес: {address}")
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку в меню",
                         reply_markup=location_bt())
        bot.register_next_step_handler(message, get_location)
@bot.callback_query_handler(lambda call: call.data in ["back", "cart"])
def calls(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_bt())
    elif call.data == "cart":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Ваша корзина:")


@bot.callback_query_handler(lambda call: "prod_" in call.data)
def prod(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    pr_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(pr_id)

    bot.send_photo(user_id, photo = product_info[3], caption=f"{product_info[0]}\n"
                   f"Цена:{product_info[1]}\n"
                   f"Описание:{product_info[2]}\n ",
                   reply_markup=plus_minus_in())


@bot.message_handler(content_types=["text"])
def text_func(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Меню":
        all_products = db.get_products_id_name()
        bot.send_message(user_id, "Выберите продукт: ", reply_markup=all_products_in(all_products))
    elif text == "Корзина":
        bot.send_message(user_id, "Ваша корзина")
    elif text == "Оставь отзыв":
        bot.send_message(user_id, "Напишите ваш отзыв")
        bot.register_next_step_handler(message, send_feedback)
    elif text == "Настройки":
        bot.send_message(user_id, "Что хотите изменить")

def send_feedback(message):
    user_id = message.from_user.id
    admin_id = -4742612458
    bot.send_message(admin_id, f"Новый отзыв от юзера с 10 {user_id}:\n \n"
                     f"{message.text}")


bot.infinity_polling()
