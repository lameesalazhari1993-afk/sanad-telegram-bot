import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
FILES_DIR = os.path.join(os.path.dirname(__file__), "files")

# =========================
# 1) عدّلي النصوص هنا فقط
# =========================

INFO_TEXTS = {
    "INFO:about_school": (
        "🏫 **نبذة عن مدرسة مدينة الشامخة**\n\n"
        "اكتبي هنا نبذة رسمية قصيرة عن المدرسة (الرؤية/الرسالة/المراحل/القيم...)\n"
        "—\n"
        "ملاحظة: يمكن تحديث هذا النص في أي وقت."
    ),
    "INFO:school_location": (
        "📍 **موقع المدرسة**\n\n"
        "ضعي رابط الموقع (Google Maps) هنا.\n"
        "مثال:\n"
        "https://maps.app.goo.gl/XXXXXXXXXXXX\n\n"
        "ويمكن إضافة وصف مختصر لطريقة الوصول."
    ),
    "INFO:contact_numbers": (
        "📞 **أرقام التواصل**\n\n"
        "☎️ هاتف المدرسة: ____\n"
        "📠 فاكس (إن وجد): ____\n"
        "📧 البريد الإلكتروني: ____\n"
        "⏰ أوقات التواصل: ____\n\n"
        "يمكن إضافة أرقام الأقسام (شؤون الطلبة/الارشاد/التربية الخاصة...)."
    ),
    "INFO:tech_support": (
        "🛠️ **الدعم الفني**\n\n"
        "للمساعدة التقنية (الدخول للمنصات/المشاكل التقنية):\n"
        "📧 بريد الدعم: ____\n"
        "📱 رقم/واتساب: ____\n"
        "⏰ ساعات الدعم: ____\n\n"
        "يرجى ذكر اسم الطالب/الصف ووصف المشكلة عند التواصل."
    ),
    "INFO:special_ed": (
        "♿ **قسم التربية الخاصة**\n\n"
        "اكتبي هنا معلومات القسم:\n"
        "• الخدمات المقدمة\n"
        "• آلية التواصل\n"
        "• ساعات استقبال أولياء الأمور\n"
        "• نماذج مهمة (تتوفر في قسم السياسات والأدلة)\n"
    ),
}

# =========================
# 2) القوائم (أزرار)
# =========================

MAIN_MENU = [
    ("🏫 نبذة عن المدرسة", "INFO:about_school"),
    ("📍 موقع المدرسة", "INFO:school_location"),
    ("📞 أرقام التواصل", "INFO:contact_numbers"),
    ("🛠️ الدعم الفني", "INFO:tech_support"),
    ("♿ قسم التربية الخاصة", "INFO:special_ed"),
    ("📚 السياسات والأدلة", "MENU:policies"),
]

POLICIES_MENU = [
    ("🗓️ التقويم الأكاديمي (Word)", "FILE:academic_calendar.docx"),
    ("📝 سياسة التقييم (Word)", "FILE:assessment_policy.docx"),
    ("⚖️ سياسة السلوك (Word)", "FILE:behavior_policy.docx"),
    ("🛡️ قانون حماية الطفل (Word)", "FILE:child_protection_law.docx"),
    ("🚫 دليل الوالدين للوقاية من المخدرات (Word)", "FILE:parent_drug_prevention_guide.docx"),
    ("🔒 سياسة السلامة الرقمية (Word)", "FILE:digital_safety_policy.docx"),
    ("📌 دليل الغش (Word)", "FILE:cheating_guide.docx"),
]

MENUS = {
    "MENU:main": MAIN_MENU,
    "MENU:policies": POLICIES_MENU,
}

def build_menu(menu_key: str, include_back: bool = True) -> InlineKeyboardMarkup:
    buttons = []
    for title, callback in MENUS.get(menu_key, []):
        buttons.append([InlineKeyboardButton(text=title, callback_data=callback)])

    if include_back and menu_key != "MENU:main":
        buttons.append([InlineKeyboardButton(text="⬅️ رجوع", callback_data="MENU:main")])

    return InlineKeyboardMarkup(buttons)

# =========================
# 3) أوامر البوت
# =========================

WELCOME_TEXT = (
    "مرحباً بكم 🌷\n"
    "هذا هو **سند – المساعد الافتراضي لمدرسة مدينة الشامخة**.\n"
    "يرجى اختيار الخدمة من القائمة:"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=build_menu("MENU:main", include_back=False),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # فتح قائمة
    if data.startswith("MENU:"):
        if data == "MENU:main":
            await query.message.edit_text(
                "القائمة الرئيسية — اختاري الخدمة:",
                reply_markup=build_menu("MENU:main", include_back=False),
                disable_web_page_preview=True
            )
            return

        if data == "MENU:policies":
            await query.message.edit_text(
                "📚 السياسات والأدلة — اختاري الملف المطلوب:",
                reply_markup=build_menu("MENU:policies", include_back=True),
                disable_web_page_preview=True
            )
            return

    # إرسال نص معلومات
    if data.startswith("INFO:"):
        text = INFO_TEXTS.get(data, "⚠️ لا توجد معلومات لهذا الخيار حالياً.")
        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    # إرسال ملف Word
    if data.startswith("FILE:"):
        filename = data.replace("FILE:", "", 1)
        file_path = os.path.join(FILES_DIR, filename)

        if not os.path.exists(file_path):
            await query.message.reply_text(
                "⚠️ الملف غير متوفر حالياً.\n"
                f"اسم الملف المطلوب: {filename}\n"
                "يرجى رفعه داخل مجلد files بنفس الاسم تماماً."
            )
            return

        await query.message.reply_document(
            document=open(file_path, "rb"),
            filename=filename,
            caption="✅ تفضلوا الملف"
        )
        return

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتبي /start لعرض القائمة.")

def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(on_click))
    app.run_polling()

if __name__ == "__main__":
    main()
