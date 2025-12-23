import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("8144798730:AAFueF0jwbI1eYF9IEoxmuFNUbUGPknC9A0")

USD_KURS = 12200
OY = 12
USTAMA = 1.575


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [["💵 USD"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "💱 Telefon narxi USD’da kiritiladi:",
        reply_markup=reply_markup
    )


async def valyuta_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["kurs"] = USD_KURS
    context.user_data["step"] = "price"

    await update.message.reply_text(
        "📱 Telefon narxini USD’da kiriting:"
    )


async def matn_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")

    # 1️⃣ Telefon narxi (USD)
    if step == "price":
        try:
            narx_usd = float(update.message.text.replace(" ", "").replace(",", ""))
            context.user_data["narx_som"] = narx_usd * USD_KURS
            context.user_data["step"] = "downpayment"

            await update.message.reply_text(
                "💰 Boshlang‘ich to‘lovni kiriting (so‘mda).\n"
                "Agar yo‘q bo‘lsa, 0 yozing:"
            )
        except:
            await update.message.reply_text("❌ Telefon narxini to‘g‘ri kiriting!")

    # 2️⃣ Boshlang‘ich to‘lov
    elif step == "downpayment":
        try:
            bosh_tolov = float(update.message.text.replace(" ", "").replace(",", ""))
            narx_som = context.user_data["narx_som"]

            if bosh_tolov > narx_som:
                await update.message.reply_text(
                    "❌ Boshlang‘ich to‘lov telefon narxidan katta bo‘lishi mumkin emas!"
                )
                return

            qolgan = narx_som - bosh_tolov
            umumiy = qolgan * USTAMA
            oylik = umumiy / OY

            await update.message.reply_text(
                f"📱 Telefon narxi: {int(narx_som):,} so‘m\n"
                f"💰 Boshlang‘ich to‘lov: {int(bosh_tolov):,} so‘m\n"
                f"📆 Muddat: 12 oy\n"
                f"💳 Oylik to‘lov: {int(oylik):,} so‘m"
            )

            context.user_data.clear()

        except:
            await update.message.reply_text("❌ Boshlang‘ich to‘lovni to‘g‘ri kiriting!")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("USD"), valyuta_tanlash))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, matn_qabul))

    print("🤖 USD-only bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
