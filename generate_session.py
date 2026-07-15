"""
generate_session.py — Assistant/Userbot ke liye SESSION_STRING banane ka script.

Chalane ka tareeka:
    python generate_session.py

Phone number + OTP (aur agar 2FA on hai toh password) maangega.
Jo string milega, use .env file mein SESSION_STRING= ke aage paste kar do.

Note: Ye apna PERSONAL Telegram account use karega (jo bhi number doge),
bot token wala account nahi. Isi account se assistant chalega.
"""
import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

if not api_id:
    api_id = input("API_ID daalo (https://my.telegram.org se): ").strip()
if not api_hash:
    api_hash = input("API_HASH daalo: ").strip()

with Client("session_gen", api_id=int(api_id), api_hash=api_hash, in_memory=True) as app:
    session_string = app.export_session_string()
    print("\n✅ Ye raha tumhara SESSION_STRING — .env file mein paste karo:\n")
    print(session_string)
    print("\n⚠️  Ise kisi ke saath share mat karna — ye tumhare account ki full access deta hai.")
