"""
texts.py — Saare messages ka content yahan hai. Wording change karni ho
(kisi bhi panel ki), bas yahi file edit karo — logic files (commands.py,
welcome.py) ko touch karne ki zarurat nahi.
"""
from config import BOT_NAME


def start_private_text(first_name: str) -> str:
    return (
        f"Heyyy {first_name}! 🙈✨\n\n"
        f"Main **{BOT_NAME}** hoon — tumhari thodi flirty, thodi sweet AI dost 💕\n\n"
        "Mujhe kisi group mein add karo aur wahan **@mention** ya **reply** karo, "
        "main turant chat karungi. Yahan DM mein bhi seedha kuch bhi bol sakte ho, "
        "main hamesha yahin hoon 😊"
    )


def start_group_text() -> str:
    return (
        f"Hiii, main **{BOT_NAME}** hoon! Is group mein aa gayi 🎉\n\n"
        "Bas mujhe **@mention** karo ya mere kisi message pe **reply** karo — "
        "main chat karna shuru kar dungi 💬"
    )


def thanks_for_adding_text(group_title: str) -> str:
    return (
        f"Heyyy! Mujhe **{group_title}** mein add karne ke liye dhanyavaad! 🎉💕\n\n"
        f"Main **{BOT_NAME}** hoon. Bas mujhe **@mention** karo ya mere kisi message "
        "pe **reply** karo, main chat karna shuru kar dungi!\n\n"
        "Admin ho toh ek baar check kar lena ki mera **privacy mode disable** hai "
        "(@BotFather → /setprivacy), warna main group ke normal messages nahi dekh paungi."
    )


def help_text() -> str:
    return (
        "**Commands:**\n"
        "/start — Intro panel\n"
        "/help — Ye message\n"
        "/reset — Is chat ki memory clear karo\n\n"
        "**Kaise chat karein:**\n"
        f"Group mein @mention ya reply karo, DM mein seedha kuch bhi likho — {BOT_NAME} "
        "respond karegi 💬"
    )
