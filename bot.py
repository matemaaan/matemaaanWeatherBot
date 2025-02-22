from config import TOKEN
from config import WTOKEN

import os
import datetime
import requests
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

@dp.message.handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid={WTOKEN}")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # продолжительность дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		
        # получаем значение погоды
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Посмотри в окно, я не понимаю, что там за погода..."
    except:
        await message.reply("Проверьте название города!")
    await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n" \
        f"Погода в городе: {city}\n Температура: {cur_weather}°C {wd}\n" \
        f"Влажность: {humidity}%\n Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n Ветер: {wind} м/с \n" \
        f"Восход солнца: {sunrise_timestamp}\n Закат солнца: {sunset_timestamp}\n Продолжительность дня: {length_of_the_day}\n" \
        f"Хорошего дня!")

if __name__ == "__main__":
	# С помощью метода executor.start_polling опрашиваем
     # Dispatcher: ожидаем команду /start
	executor.start_polling(dp)
