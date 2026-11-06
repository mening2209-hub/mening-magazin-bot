import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# BotFather tokeningiz
TOKEN = "9129111266:AAE_xfqt0rsQv6mbt85i8qZsAWWBIg1DkV8"

# Sizning Telegram ID raqamingiz (Admin)
ADMIN_ID = 8788801606
ADMIN_USERNAME = "@sizning_usernameingiz"  # Admin useri
ADMIN_PHONE = "+998901234567"            # Admin telefoni

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Mijoz uchun asosiy menyu (Uzum style)
client_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Mahsulotlar katalogi"), KeyboardButton(text="🛒 Savatcham")],
        [KeyboardButton(text="📞 Biz bilan aloqa"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True
)

# 2. Admin uchun maxsus boshqaruv menyusi
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="➕ Mahsulot qo'shish")],
        [KeyboardButton(text="📢 Xabarnoma yuborish"), KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "Xush kelibsiz, Boss (Admin)! Siz uchun maxsus boshqaruv paneli:",
            reply_markup=admin_menu
        )
    else:
        await message.answer(
            f"Assalomu alaykum, {message.from_user.first_name}!\n"
            "🛒 **Uzum Market** uslubidagi internet-do'konimizga xush kelibsiz!\n"
            "Kerakli bo'limni tanlang:",
            reply_markup=client_menu,
            parse_mode="Markdown"
        )

# --- Mijoz menyusi: Katalog (Uzum uslubida rasmli) ---
@dp.message(F.text == "🛍 Mahsulotlar katalogi")
async def catalog_handler(message: types.Message):
    # Mahsulot 1 uchun inline tugmalar (Savatchaga qo'shish)
    kb_product1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Savatchaga qo'shish", callback_data="add_to_cart_1")]
        ]
    )
    
    # Namuna sifatida rasm bilan mahsulot yuborish (o'zingizning rasm havolangizni qo'yishingiz mumkin)
    await message.answer_photo(
        photo="https://images.unsplash.com/photo-1542291026-7eec264c27ff", # Misol uchun krossovka rasmi
        caption=(
            "👟 **Nike Air Max Krossovka**\n\n"
            "💰 Narxi: 250 000 so'm\n"
            "📝 Tavsif: Yuqori sifatli va qulay sport kiyimi."
        ),
        reply_markup=kb_product1,
        parse_mode="Markdown"
    )

# --- Savatchaga qo'shish tugmasi bosilganda ---
@dp.callback_query(F.data == "add_to_cart_1")
async def add_to_cart_callback(callback: types.CallbackQuery):
    # Bu yerda oddiy savatchaga saqlash logikasi ishlaydi
    kb_checkout = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Buyurtma berishga o'tish", callback_data="start_order")]
        ]
    )
    await callback.message.answer(
        "✅ Mahsulot savatchaga qo'shildi!\n\nBuyurtmani rasmiylashtirish uchun tugmani bosing:",
        reply_markup=kb_checkout
    )
    await callback.answer()

# --- Buyurtma berish jarayoni (Telefon va Lokatsiya so'rash) ---
@dp.callback_query(F.data == "start_order")
@dp.message(F.text == "🛒 Savatcham")
async def checkout_handler(event: types.Message | types.CallbackQuery):
    message = event.message if isinstance(event, types.CallbackQuery) else event
    
    # Telefon raqamni so'rash uchun maxsus tugma
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "📦 Savatchangizda 1 ta mahsulot bor.\n\n"
        "Buyurtmani yakunlash uchun iltimos, pastdagi tugmani bosib **telefon raqamingizni** yuboring:",
        reply_markup=phone_keyboard
    )
    if isinstance(event, types.CallbackQuery):
        await event.answer()

# --- Telefon raqam qabul qilinganda lokatsiya so'raladi ---
@dp.message(F.contact)
async def contact_received(message: types.Message):
    phone = message.contact.phone_number
    
    # Lokatsiyani so'rash uchun tugma
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        f"Raqamingiz qabul qilindi: `{phone}` ✅\n\n"
        "Endi yetkazib berish uchun **turgan joyingiz (lokatsiyangizni)** yuboring:",
        reply_markup=location_keyboard,
        parse_mode="Markdown"
    )
    # Bu yerda raqamni vaqtinchalik xotirada saqlab turishingiz mumkin

# --- Lokatsiya qabul qilinganda buyurtma Adminga boradi ---
@dp.message(F.location)
async def location_received(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    user_name = message.from_user.first_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "Username yo'q"
    
    admin_text = (
        f"🔔 **Yangi buyurtma tushdi!**\n\n"
        f"👤 Mijoz: {user_name}\n"
        f"🔗 Telegram: {user_username}\n"
        f"📦 Mahsulot: Nike Air Max Krossovka - 250 000 so'm"
    )
    
    try:
        # Adminga matnli xabar yuborish
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
        # Adminga xaritadagi lokatsiyani yuborish
        await bot.send_location(chat_id=ADMIN_ID, latitude=lat, longitude=lon)
        
        # Mijozga tasdiqlash xabari
        await message.answer(
            "✅ Buyurtmangiz muvaffaqiyatli qabul qilindi!\n"
            "Tez orada operatorimiz siz bilan bog'lanadi.",
            reply_markup=client_menu
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}", reply_markup=client_menu)

# --- Biz bilan aloqa (Admin haqida ma'lumot) ---
@dp.message(F.text == "📞 Biz bilan aloqa")
async def contact_admin_handler(message: types.Message):
    await message.answer(
        "📞 **Menejer bilan bog'lanish:**\n\n"
        f"👨‍💻 Admin Telegram: {ADMIN_USERNAME}\n"
        f"📱 Telefon raqam: {ADMIN_PHONE}\n\n"
        "Savollaringiz bo'lsa bemalol yozishingiz mumkin!",
        parse_mode="Markdown"
    )

@dp.message(F.text == "ℹ️ Biz haqimizda")
async def info_handler(message: types.Message):
    await message.answer("🛒 Bu bot orqali siz uyingizdan chiqmagan holda eng sara mahsulotlarni tez va qulay xarid qilishingiz mumkin.")

# --- Admin menyusi handlerlari ---
@dp.message(F.text == "📊 Statistika")
async def admin_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("📊 Bot statistikasi:\n\nJami buyurtmalar: 1 ta\nFaol foydalanuvchilar: Joyida")

@dp.message(F.text == "➕ Mahsulot qo'shish")
async def admin_add_product(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("➕ Yangi mahsulot qo'shish uchun mahsulot rasmi, nomi va narxini yuboring.")

@dp.message(F.text == "📢 Xabarnoma yuborish")
async def admin_broadcast(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("📢 Barcha mijozlarga yuboriladigan xabar matnini kiriting:")

@dp.message(F.text == "⚙️ Sozlamalar")
async def admin_settings(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("⚙️ Admin sozlamalari menyusi.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())