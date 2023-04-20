import telebot
import pyowm
from telebot import types

bot = telebot.TeleBot('6285665537:AAEm_dKcuu3EnfQ-3r4GTfuXL7d3gtS7Ets')
owm = pyowm.OWM('42ed9c06bb9bfeb86f37662f6f8f5f7f')
place = 'Миколаїв'

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton(text="Погода")
    button2 = types.KeyboardButton(text="Введіть місто")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Виберіть:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True if message.text == "Погода" else False)
def weather_command(message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    wind_speed = w.wind()['speed']
    wind_deg = w.wind()['deg']
    pressure = w.pressure['press']
    direction = _get_direction(wind_deg)
    pressure_mmhg = round(pressure / 1.333, 2)
    bot.send_message(message.chat.id, f"Погода в {place}: температура {temperature}°C, "
                                      f"вітер {wind_speed} м/с, {direction}, "
                                      f"тиск {pressure} гПа ({pressure_mmhg} мм рт. ст.)")

@bot.message_handler(func=lambda message: True if message.text == "Ввести город" else False)
def city_command(message):
    bot.send_message(message.chat.id, "Введіть місто:")

@bot.message_handler(func=lambda message: True if message.text else False)
def get_city(message):
    global place
    place = message.text
    bot.send_message(message.chat.id, f"Місто: {place}")

def _get_direction(degree):
    directions = ['Пн', 'ПнСх', 'Сх', 'ПдСх', 'Пд', 'ПдЗх', 'Зх', 'ПнЗх']
    i = int((degree + 22.5) / 45) % 8
    return directions[i]

bot.polling(none_stop=True)
