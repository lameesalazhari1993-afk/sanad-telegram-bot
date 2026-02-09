import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
FILES_DIR = os.path.join(os.path.dirname(__file__), "files")

# ==========================================
# قائمة الأزرار الرئيسية (العنوان -> اسم الملف)
# ==========================================
FILE_BUTTONS = [
    ("🏫 نبذة عن المدرسة", "school_profile.docx"),
    ("📍 موقع المدرسة", "school_location.docx"),
    ("📞 أرقام التواصل", "contact_numbers.docx"),
    ("🛠️ الدعم الفني", "technical_support.docx"),
    ("♿ قسم التربية الخاصة", "special_education_department.docx"),
    ("✍️ التوقيع على ميثاق الشراكة", "partnership_charter_signature.docx"),
    ("📘 دليل مدرسة مدينة الشامخة", "alshamekha_school_guide.docx"),
    ("🗓️ التقويم الأكاديمي", "academic_calendar.docx"),
    ("✅ سياسة التقييم", "assessment_policy.docx"),
    ("⚖️ سياسة السلوك", "behavior_policy.docx"),
    ("🛡️ قانون حماية الطفل", "child_protection_policy.docx"),
    ("🚫 دليل الوالدين للوقاية من المخدرات", "parents_drug_prevention_guide.docx"),
    ("🔐 سياسة السلامة الرقمية", "digital_safety_policy.docx"),
    ("🧾 دليل الغش", "academic_dishonesty_guide.docx"),
]

def build_main_menu() -> InlineKeyboardMarkup:
    # ترتيب الأزرار: زر بكل سطر (أوضح للأهالي)
    keyboard = [
        [InlineKeyboardButton(text=title, callback_data=f"FILE:{filename}")]
        for title, filename in FILE_BUTTONS
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "مرحباً بكم 🌷\n"
        "هذا هو **سند – المساعد الافتراضي لمدرسة مدينة الشامخة**.\n"
        "يرجى اختيار الملف المطلوب من القائمة التالية:"
    )
    await update.message.reply_text(
        text,
        reply_markup=build_main_menu(),
        parse_mode="Markdown"
    )

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if not data.startswith("FILE:"):
        await query.message.reply_text("⚠️ أمر غير معروف. اكتب /start للعودة للقائمة.")
        return

    filename = data.replace("FILE:", "", 1)
    file_path = os.path.join(FILES_DIR, filename)

    if not os.path.exists(file_path):
        await query.message.reply_text(
            "⚠️ الملف غير متوفر حاليًا.\n"
            f"اسم الملف المطلوب: {filename}\n"
            "يرجى التأكد من رفعه داخل مجلد files."
        )
        return

    # إرسال الملف
    with open(file_path, "rb") as f:
        await query.message.reply_document(
            document=f,
            filename=filename,
            caption="✅ تفضلوا الملف"
        )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتبي /start لعرض قائمة الملفات.")

def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var (Render Secret)")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(on_click))
    app.run_polling()

if __name__ == "__main__":
    main()
