from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time, os, functools

# Bot Configuration
API_ID = 27494064
API_HASH = "11cf76e59c9078d70d1df0eb6c68804c"
BOT_TOKEN = "7420121486:AAFiqvCpwU6L0fB1QnhDsbpMSN7dlOkvP6U"
CHANNEL_ID = -1002297260726
CHANNEL_USERNAME = "@Sazuz_Modz"
ADMIN_PASSWORD = "1830"

# Initialize Bot
app = Client("SazuzModz_ManagerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Admin Login System
admin_logged_in = False

def check_admin(func):
    """Decorator to check if admin is logged in before executing commands."""
    @functools.wraps(func)
    def wrapper(client, message):
        global admin_logged_in
        if not admin_logged_in:
            message.reply_text("❌ Access Denied! Please login first using /loginsazuz")
            return
        return func(client, message)
    return wrapper

@app.on_message(filters.command("loginsazuz"))
def login_admin(client, message):
    global admin_logged_in
    message.reply_text("🔑 Enter the admin password:")

@app.on_message(filters.text & filters.private)
def check_password(client, message):
    global admin_logged_in
    if message.text == ADMIN_PASSWORD:
        admin_logged_in = True
        message.reply_text("✅ Login Successful! Admin Panel Unlocked.")
    else:
        message.reply_text("❌ Incorrect Password! Try Again.")

# Rank-Based Link System
link_storage = {}

@app.on_message(filters.command("generate_link"))
@check_admin
def generate_link(client, message):
    message.reply_text("📌 Enter the custom alias for the mod:")

@app.on_message(filters.text & filters.private)
def get_alias(client, message):
    alias = message.text
    link_storage[alias] = {}
    message.reply_text("✅ Alias set! Now provide the download links tier-wise.")

    client.send_message(
        message.chat.id,
        "🎯 Link for Tier 1 (2 Shorten Links):",
    )

@app.on_message(filters.text & filters.private)
def get_tier1_link(client, message):
    alias = list(link_storage.keys())[-1]  # Get last added alias
    link_storage[alias]["tier1"] = message.text
    message.reply_text(f"✔ Tier 1 Link Saved: {message.text}")

    client.send_message(
        message.chat.id,
        "🎯 Link for Tier 2 & 3 (1 Shorten Link):",
    )

@app.on_message(filters.text & filters.private)
def get_tier23_link(client, message):
    alias = list(link_storage.keys())[-1]
    link_storage[alias]["tier23"] = message.text
    message.reply_text(f"✔ Tier 2 & 3 Link Saved: {message.text}")

    client.send_message(
        message.chat.id,
        "🎯 Link for Tier 4 & 5 (Premium Download):",
    )

@app.on_message(filters.text & filters.private)
def get_tier45_link(client, message):
    alias = list(link_storage.keys())[-1]
    link_storage[alias]["tier45"] = message.text
    message.reply_text(f"✔ Tier 4 & 5 Link Saved: {message.text}")

    client.send_message(
        message.chat.id,
        "🎯 Link for Tier 6 (Direct Download):",
    )

@app.on_message(filters.text & filters.private)
def get_tier6_link(client, message):
    alias = list(link_storage.keys())[-1]
    link_storage[alias]["tier6"] = message.text
    message.reply_text(f"✔ Tier 6 Link Saved: {message.text}\n✅ Link Generation Complete!")

# Welcome Message for New Members
@app.on_chat_member_updated()
def welcome_new_users(client, update):
    if update.new_chat_member:
        client.send_message(
            update.new_chat_member.user.id,
            "🤖 Welcome to SazuzModz! Enjoy full mod access and stay updated.",
        )

# Channel Management & Badge System
@app.on_message(filters.command("user_rank"))
@check_admin
def check_rank(client, message):
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    rank = "Cyber Agent"  # Example rank, you can replace it with actual logic
    message.reply_text(f"🏅 {message.from_user.first_name}'s Rank: {rank}")

# Bot Start
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "🤖 Welcome to SazuzModz Manager Bot!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Explore Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("🔐 Login as Admin", callback_data="admin_login")]
        ]),
    )

# Run Bot
app.run()