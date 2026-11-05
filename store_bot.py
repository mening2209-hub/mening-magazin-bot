import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# BotFather tokeningiz
TOKEN = "9129111266:AAE_xfqt0rsQv6mbt85i8qZsAWWBIg1DkV8"

# Sizning Telegram ID raqamingiz
ADMIN_ID = 8788801606

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Asosiy menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Katalog"), KeyboardButton(text="🛒 Buyurtma berish")],
        [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    print(f"DEBUG: {message.from_user.first_name} /start bosdi!")
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        "Do'konimiz botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )

@dp.message(lambda msg: msg.text and "Katalog" in msg.text)
async def catalog_handler(message: types.Message):
    print(f"DEBUG: {message.from_user.first_name} Katalog bosdi!")
    await message.answer(
        "📦 Bizning mahsulotlar:\n\n"
        "1. Krossovka - 250 000 so'm\n"
        "2. Xudi (Tolstovka) - 180 000 so'm\n\n"
        "Buyurtma berish uchun pastdagi '🛒 Buyurtma berish' tugmasini bosing."
    )

@dp.message(lambda msg: msg.text and "Buyurtma berish" in msg.text)
async def order_handler(message: types.Message):
    print(f"DEBUG: {message.from_user.first_name} BUYURTMA BERISH TUGMASINI BOSDI!")
    
    user_name = message.from_user.first_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "Username yo'q"
    user_id = message.from_user.id

    admin_text = (
        f"🔔 Yangi buyurtma tushdi!\n\n"
        f"👤 Mijoz: {user_name}\n"
        f"🔗 Telegram: {user_username}\n"
        f"🆔 ID raqami: {user_id}\n"
        f"📦 Tanlangan mahsulot: Krossovka - 250 000 so'm"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        await message.answer("✅ Buyurtmangiz muvaffaqiyatli qabul qilindi! Tez orada operatorimiz siz bilan bog'lanadi.")
        print("DEBUG: Admin'ga xabar muvaffaqiyatli yuborildi!")
    except Exception as e:
        print(f"XATOLIK CHIQDI: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {e}")

@dp.message(lambda msg: msg.text and "Aloqa" in msg.text)
async def contact_handler(message: types.Message):
    await message.answer("Menejer bilan aloqa: @sizning_usernameingiz")

@dp.message(lambda msg: msg.text and "Biz haqimizda" in msg.text)
async def info_handler(message: types.Message):
    await message.answer("Bu bot mahsulotlarni qulay va tezkor ko'rish uchun yaratilgan.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())