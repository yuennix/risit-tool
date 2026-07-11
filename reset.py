#WEYN
import os
import random
from random import choice
from threading import Thread, Lock 
import requests
from user_agent import generate_user_agent
from hashlib import md5
from bs4 import BeautifulSoup
import base64
import secrets
from hashlib import md5
try:
    import requests
    import pyfiglet
    from rich.console import Console
    from cfonts import render, say
except ImportError:
    os.system("pip install requests telethon pyfiglet rich cfonts")


import time
b = random.randint(5,208)
bo = f'\x1b[38;5;{b}m'
ED='\x1b[38;5;208m'
BLUE = '\033[94m'
Z = '\033[1;31m' 
YELLOW = '\033[1;33m' 
import requests, random, string, uuid
from datetime import datetime
import base64
import json
J = '\033[2;36m'
N = '\033[1;37m'

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def banner():
    WDEH = render('{WEYN}', colors=['red', 'white'], align='center')
    print(f'''{J}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
 {N}DEV / @WEYN_DEAL_BOT{J}| {N} Ch:@WEYN_PY{J}| {N}PROGRAMMER /WEYN
{J}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
''')

banner()

config = load_config()

if config.get("chat_id") and config.get("bot_token"):
    print(f"{J}[✓] Using saved Chat ID and Bot Token.")
    chat_id = config["chat_id"]
    bot_token = config["bot_token"]
else:
    chat_id = input("Enter ID: ")
    print("\n")
    bot_token = input("Enter Your Token: ")
    save_config({"chat_id": chat_id, "bot_token": bot_token})
    print(f"{J}[✓] Saved! You won't be asked again.\n")

def send_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.json()
    except Exception as e:
        print("[-] Telegram send error:", e)
        return None

def generate_device_info(custom_password=None):
    ANDROID_ID = f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}"
    USER_AGENT = f"Instagram 394.0.0.46.81 Android ({random.choice(['28/9','29/10','30/11','31/12'])}; {random.choice(['240dpi','320dpi','480dpi'])}; {random.choice(['720x1280','1080x1920','1440x2560'])}; {random.choice(['samsung','xiaomi','huawei','oneplus','google'])}; {random.choice(['SM-G975F','Mi-9T','P30-Pro','ONEPLUS-A6003','Pixel-4'])}; intel; en_US; {random.randint(100000000,999999999)})"
    WATERFALL_ID = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    if custom_password:
        plain_password = custom_password
    else:
        rand_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        plain_password = f'WEYN@{rand_suffix}'
    PASSWORD = f'#PWD_INSTAGRAM:0:{timestamp}:{plain_password}'
    return ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD, plain_password

def make_headers(mid="", user_agent=""):
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "X-Mid": mid,
        "User-Agent": user_agent,
        "Content-Length": "9481"
    }

def id_user(user_id):
    try:
        url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
        headers = {"User-Agent": "Instagram 219.0.0.12.117 Android"}
        r = requests.get(url, headers=headers)
        try:
            username = r.json()["user"]["username"]
            return username
        except:
            print("Failed:", r.text)
    except:
        pass

def reset_instagram_password(reset_link, custom_password=None):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD, plain_password = generate_device_info(custom_password)
        uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
        token = reset_link.split("&token=")[1].split(":")[0]

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        data = {
            "source": "one_click_login_email",
            "uidb36": uidb36,
            "device_id": ANDROID_ID,
            "token": token,
            "waterfall_id": WATERFALL_ID
        }
        r = requests.post(url, headers=make_headers(user_agent=USER_AGENT), data=data)

        if "user_id" not in r.text:
            return {"success": False, "error": f"Error in reset request: {r.text}"}

        mid = r.headers.get("Ig-Set-X-Mid")
        resp_json = r.json()
        user_id = resp_json.get("user_id")
        cni = resp_json.get("cni")
        nonce_code = resp_json.get("nonce_code")
        challenge_context = resp_json.get("challenge_context")

        url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
        data2 = {
            "user_id": str(user_id),
            "cni": str(cni),
            "nonce_code": str(nonce_code),
            "bk_client_context": '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"}',
            "challenge_context": str(challenge_context),
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "get_challenge": "true"
        }
        r2 = requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data2).text

        challenge_context_final = r2.replace('\\', '').split(f'(bk.action.i64.Const, {cni}), "')[1].split('", (bk.action.bool.Const, false)))')[0]

        data3 = {
            "is_caa": "False",
            "source": "",
            "uidb36": "",
            "error_state": {"type_name":"str","index":0,"state_id":1048583541},
            "afv": "",
            "cni": str(cni),
            "token": "",
            "has_follow_up_screens": "0",
            "bk_client_context": {"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"},
            "challenge_context": challenge_context_final,
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "enc_new_password1": PASSWORD,
            "enc_new_password2": PASSWORD
        }

        requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data3)

        return {
            "success": True,
            "password": plain_password,
            "user_id": user_id
        }

    except Exception as e:
        return False


def main():
    print("\n")
    reset_link = input("Enter Reset Link: ")
    print("\n")
    custom_pw = input("Enter Custom Password (leave blank to auto-generate WEYN@...): ").strip()
    custom_password = custom_pw if custom_pw else None
    print("\n")
    result = reset_instagram_password(reset_link, custom_password)
    if result and result.get("success"):
        user_id = result.get("user_id")
        new_password = result.get("password")
        username = id_user(user_id)
        msg = f'''
╔   ─────━ ░ WEYN░ ━─────   ╗
⌦ [ info rest ] 

[+] Username: {username}
[+] Password: {new_password}

◢─────━ ░ WEYN░━──────◣
❝ By @WEYN_DEAL_BOT | @WEYN_PY❞
'''
        print(msg)
        send_telegram(bot_token, chat_id, msg)
        print("\nDone ✅")
    else:
        print("[-] Reset failed.")

main()
