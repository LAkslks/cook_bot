import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from googletrans import Translator
import aiohttp

TOKEN = '7053645873:AAGKn6GFRBexTF4AZpnoG4Y0-z4SZT6nJhM'
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start')) 
async def hello(message: Message):
    await message.answer("Привет\nя помогу тебе выбрать блюда на ужин, если не можешь определиться\nНажми на: /dinner")

@dp.message(Command('dinner'))
async def random_meal(message: types.Message):
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Обработка возможных ошибок HTTP
                meal_detail = await response.json()
                meal = meal_detail['meals'][0]  # Исправлен ключ: должен быть 'meals'

                translator = Translator()
                menu_name = translator.translate(meal.get("strMeal", "Неизвестно"), dest='ru').text
                menu_category = translator.translate(meal.get("strCategory", "Неизвестно"), dest='ru').text
                menu_tags = translator.translate(meal.get("strTags", "Неизвестно"), dest='ru').text
                menu_country = translator.translate(meal.get("strArea", "Неизвестно"), dest='ru').text
                menu_instruction = translator.translate(meal.get("strInstructions", "Никаких инструкций нет."), dest='ru').text

                # Форматируем ответное сообщение
                response_message = (f"Название: {menu_name}\n"
                                    f"Категория: {menu_category}\n"
                                    f"Теги: {menu_tags}\n"
                                    f"Страна: {menu_country}\n"
                                    f"Инструкции: {menu_instruction}\n"
                                    '\nEсли хочешь другой рецепт нажми на: /dinner ')
                await message.answer(response_message)
    except Exception as e:
        await message.answer("Произошла ошибка при получении рецепта.")
        print(f"Ошибка: {e}")
async def main():
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())