# modules/lang.py

LANGUAGES = {
    "en": "English",
    "uk": "Українська",
    "ru": "Русский",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "pl": "Polski",
    "nl": "Nederlands",
    "sv": "Svenska",
    "fi": "Suomi",
    "no": "Norsk",
    "da": "Dansk",
    "cs": "Čeština",
    "hu": "Magyar",
    "ro": "Română",
    "bg": "Български",
    "el": "Ελληνικά",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文",
    "ar": "العربية",
    "he": "עברית",
    "tr": "Türkçe",
}

TEXTS = {
    "welcome": {
        "en": "Welcome! Please choose your language.",
        "uk": "Ласкаво просимо! Виберіть вашу мову.",
        "ru": "Добро пожаловать! Пожалуйста, выберите язык.",
        "es": "¡Bienvenido! Por favor, elige tu idioma.",
        "fr": "Bienvenue ! Veuillez choisir votre langue.",
        "de": "Willkommen! Bitte wählen Sie Ihre Sprache.",
        "it": "Benvenuto! Per favore scegli la tua lingua.",
        "pt": "Bem-vindo! Por favor, escolha seu idioma.",
        "pl": "Witamy! Proszę, wybierz swój język.",
        "nl": "Welkom! Kies je taal.",
        "sv": "Välkommen! Vänligen välj ditt språk.",
        "fi": "Tervetuloa! Valitse kielesi.",
        "no": "Velkommen! Vennligst velg språket ditt.",
        "da": "Velkommen! Vælg venligst dit sprog.",
        "cs": "Vítejte! Vyberte si svůj jazyk.",
        "hu": "Üdvözlünk! Kérjük, válassz nyelvet.",
        "ro": "Bun venit! Te rugăm să alegi limba.",
        "bg": "Добре дошли! Моля, изберете език.",
        "el": "Καλώς ήρθατε! Επιλέξτε τη γλώσσα σας.",
        "ja": "ようこそ！言語を選んでください。",
        "ko": "환영합니다! 언어를 선택하세요.",
        "zh": "欢迎！请选择您的语言。",
        "ar": "مرحبًا! الرجاء اختيار لغتك.",
        "he": "ברוכים הבאים! בחר בבקשה את השפה שלך.",
        "tr": "Hoş geldiniz! Lütfen dilinizi seçin.",
    },
    "ask_time": {
        "en": "What time is it now for you? (HH:MM)",
        "uk": "Котра зараз година? (ГГ:ХХ)",
        "ru": "Который сейчас час? (ЧЧ:ММ)",
        "es": "¿Qué hora es ahora para ti? (HH:MM)",
        "fr": "Quelle heure est-il chez vous ? (HH:MM)",
        "de": "Wie spät ist es bei dir? (HH:MM)",
        "it": "Che ore sono adesso per te? (HH:MM)",
        "pt": "Que horas são agora para você? (HH:MM)",
        "pl": "Która jest teraz godzina? (GG:MM)",
        "nl": "Hoe laat is het nu bij jou? (UU:MM)",
        "sv": "Vad är klockan hos dig? (HH:MM)",
        "fi": "Paljonko kello on nyt sinulla? (HH:MM)",
        "no": "Hva er klokka hos deg nå? (HH:MM)",
        "da": "Hvad er klokken hos dig? (HH:MM)",
        "cs": "Kolik je u vás teď hodin? (HH:MM)",
        "hu": "Hány óra van nálad most? (HH:MM)",
        "ro": "Ce oră este acum la tine? (HH:MM)",
        "bg": "Колко е часът при теб? (HH:MM)",
        "el": "Τι ώρα είναι τώρα για εσένα; (ΩΩ:ΛΛ)",
        "ja": "今何時ですか？ (HH:MM)",
        "ko": "지금 몇 시인가요? (HH:MM)",
        "zh": "你现在几点了？(HH:MM)",
        "ar": "ما الوقت الآن لديك؟ (HH:MM)",
        "he": "מה השעה עכשיו אצלך? (HH:MM)",
        "tr": "Şu an saat kaç? (SS:DD)",
    },
    "limit_exceeded": {
        "en": "You've reached today's limit of surprises 😉",
        "uk": "Ви досягли ліміту сюрпризів на сьогодні 😉",
        "ru": "Вы достигли лимита сюрпризов на сегодня 😉",
        "es": "Has alcanzado el límite de sorpresas para hoy 😉",
        "fr": "Vous avez atteint la limite de surprises pour aujourd'hui 😉",
        "de": "Du hast das heutige Überraschungslimit erreicht 😉",
        "it": "Hai raggiunto il limite di sorprese per oggi 😉",
        "pt": "Você atingiu o limite de surpresas para hoje 😉",
        "pl": "Osiągnąłeś dzisiejszy limit niespodzianek 😉",
        "nl": "Je hebt de limiet voor verrassingen vandaag bereikt 😉",
        "sv": "Du har nått dagens gräns för överraskningar 😉",
        "fi": "Olet saavuttanut päivän yllätysrajan 😉",
        "no": "Du har nådd dagens overraskelsesgrense 😉",
        "da": "Du har nået dagens overraskelsesgrænse 😉",
        "cs": "Dosáhli jste dnešního limitu překvapení 😉",
        "hu": "Elérted a napi meglepetés limitet 😉",
        "ro": "Ai atins limita de surprize pentru azi 😉",
        "bg": "Достигнали сте лимита за изненади днес 😉",
        "el": "Έχετε φτάσει το όριο των εκπλήξεων για σήμερα 😉",
        "ja": "今日のサプライズの上限に達しました 😉",
        "ko": "오늘의 서프라이즈 한도에 도달했습니다 😉",
        "zh": "你已达到今天的惊喜限制 😉",
        "ar": "لقد وصلت إلى حد المفاجآت لليوم 😉",
        "he": "הגעת למגבלת ההפתעות היומית שלך 😉",
        "tr": "Bugünün sürpriz sınırına ulaştınız 😉",
    },
    "auto_surprise_text": {
        "en": "🎁 Your daily surprise!",
        "uk": "🎁 Ваш щоденний сюрприз!",
        "ru": "🎁 Ваш ежедневный сюрприз!",
        "es": "🎁 ¡Tu sorpresa diaria!",
        "fr": "🎁 Votre surprise quotidienne!",
        "de": "🎁 Deine tägliche Überraschung!",
        "it": "🎁 La tua sorpresa quotidiana!",
        "pt": "🎁 Sua surpresa diária!",
        "pl": "🎁 Twoja codzienna niespodzianka!",
        "nl": "🎁 Jouw dagelijkse verrassing!",
        "sv": "🎁 Din dagliga överraskning!",
        "fi": "🎁 Päivittäinen yllätyksesi!",
        "no": "🎁 Din daglige overraskelse!",
        "da": "🎁 Din daglige overraskelse!",
        "cs": "🎁 Tvůj denní překvapení!",
        "hu": "🎁 Napi meglepetésed!",
        "ro": "🎁 Surpriza ta zilnică!",
        "bg": "🎁 Вашата дневна изненада!",
        "el": "🎁 Η καθημερινή σου έκπληξη!",
        "ja": "🎁 あなたの毎日のサプライズ！",
        "ko": "🎁 당신의 일일 서프라이즈!",
        "zh": "🎁 你的每日惊喜！",
        "ar": "🎁 مفاجأتك اليومية!",
        "he": "🎁 ההפתעה היומית שלך!",
        "tr": "🎁 Günlük sürpriziniz!",
    },
}

TEXTS.update({
    "welcome": {
        "en": "Welcome! Please choose your language.",
        "uk": "Ласкаво просимо! Виберіть вашу мову.",
        # ... остальные языки
    },
    "invalid_time_format": {
        "en": "Invalid time format. Please enter in HH:MM.",
        "uk": "Неправильний формат часу. Введіть у форматі ГГ:ХХ.",
        # ...
    },
    "time_saved": {
        "en": "Time saved successfully!",
        "uk": "Час успішно збережено!",
        # ...
    },
    "choose_action": {
        "en": "Choose an action:",
        "uk": "Оберіть дію:",
        # ...
    },
    "settings_text": {
        "en": "⚙ Settings",
        "uk": "⚙ Налаштування",
        # ...
    },
    "choose_language": {
        "en": "Choose your language:",
        "uk": "Оберіть вашу мову:",
        # ...
    },
    "unknown_command": {
        "en": "Unknown command.",
        "uk": "Невідома команда.",
        # ...
    },
})

def get_text(key: str, lang: str = "en") -> str:
    """
    Возвращает текст по ключу и языку.
    Если перевода нет, возвращает на английском или сам ключ.
    """
    if key not in TEXTS:
        return key
    return TEXTS[key].get(lang) or TEXTS[key].get("en") or key

def get_languages() -> dict:
    """
    Возвращает словарь доступных языков.
    """
    return LANGUAGES

from modules.lang import get_text, get_languages

print(get_text("welcome", "ru"))  # Добро пожаловать! Пожалуйста, выберите язык.
print(get_text("limit_exceeded", "fr"))  # Vous avez atteint la limite de surprises pour aujourd'hui 😉
print(get_text("auto_surprise_text", "ja"))  # 🎁 あなたの毎日のサプライズ！

print(get_languages())  # Словарь всех языков
