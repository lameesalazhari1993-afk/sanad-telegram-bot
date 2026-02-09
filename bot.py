import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
FILES_DIR = os.path.join(os.path.dirname(__file__), "files")

# =========================
# القوائم
# =========================

MAIN_MENU = [
    ("🏫 نبذة عن المدرسة", "MENU:about"),
    ("📍 موقع المدرسة", "MENU:location"),
    ("📘 الدليل الإرشادي لمدرسة مدينة الشامخة", "MENU:guide"),
    ("🗓️ التقويم الأكاديمي", "MENU:calendar"),
    ("📞 تواصل", "MENU:contact"),
    ("⚖️ سياسات", "MENU:policies"),
]

ABOUT_MENU = [
    ("📄 نبذة عن المدرسة", "FILE:school_profile.docx"),
]

LOCATION_MENU = [
    ("📄 موقع المدرسة", "FILE:school_location.docx"),
]

GUIDE_MENU = [
    ("📄 الدليل الإرشادي لمدرسة مدينة الشامخة", "FILE:alshamekha_school_guide.docx"),
]

CALENDAR_MENU = [
    ("📄 التقويم الأكاديمي", "FILE:academic_calendar.docx"),
]

CONTACT_MENU = [
    ("📄 أرقام التواصل", "FILE:contact_numbers.docx"),
    ("📄 الدعم الفني", "FILE:technical_support.docx"),
]

POLICIES_MENU = [
    ("📄 سياسة التقييم", "FILE:assessment_policy.docx"),
    ("📄 سياسة السلوك", "FILE:behavior_policy.docx"),
    ("📄 قانون حماية الطفل", "FILE:child_protection_policy.docx"),
    ("📄 دليل الوالدين للوقاية من المخدرات", "FILE:parents_drug_prevention_guide.docx"),
    ("📄 سياسة السلامة الرقمية", "FILE:digital_safety_policy.docx"),
    ("📄 دليل الغش", "FILE:academic_dishonesty_guide.docx"),
]

MENUS = {
    "MENU:main": MAIN_MENU,
    "MENU:about": ABOUT_MENU,
    "MENU:location": LOCATION_MENU,
    "MENU:guide": GUIDE_MENU,
    "MENU:calendar": CALENDAR_MENU,
    "MENU:contact": CONTACT_MENU,
    "MENU:policies": POLICIES_MENU,
}

# =========================
# أدوات مساعدة
# =========================

def build_menu(menu_key: str, back: bool = True):
    buttons = []
    for title, callback in MENUS.get(menu_key, []):
        buttons.append([InlineKeyboardButton(text=title, callback_data=callback)])

    if back and menu_key != "MENU:main":
        buttons.append([InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="MENU:main")])

    return InlineKeyboardMarkup(buttons)

# =========================
# أوامر البوت
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "مرحباً بكم 🌷\n"
        "هذا هو **سند – المساعد الافتراضي لمدرسة مدينة الشامخة**.\n"
        "يرجى اختيار القسم المطلوب:"
    )
    await update.message.reply_text(
        text,
        reply_markup=build_menu("MENU:main", back=False),
        parse_mode="Markdown"
    )

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # فتح قائمة
    if data.startswith("MENU:"):
        await query.message.edit_text(
            "يرجى اختيار المطلوب:",
            reply_markup=build_menu(data)
        )
        return

    # إرسال ملف
    if data.startswith("FILE:"):
        filename = data.replace("FILE:", "", 1)
        file_path = os.path.join(FILES_DIR, filename)

        if not os.path.exists(file_path):
            await query.message.reply_text("⚠️ الملف غير متوفر حالياً.")
            return

        with open(file_path, "rb") as f:
            await query.message.reply_document(
                document=f,
                filename=filename,
                caption="✅ تفضلوا الملف"
            )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتبي /start لعرض القائمة الرئيسية.")

def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(on_click))
    app.run_polling()

if __name__ == "__main__":
    main()
