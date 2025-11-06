import telebot
from telebot import types
import json
import time
import os
from flask import Flask, request # Flask लाइब्रेरी अब ज़रूरी है

# --- CONFIGURATION (ज़रूरी बदलाव यहाँ करें) ---

# ⚠️ BOT_TOKEN को सीधे कोड में न डालें। Vercel में Environment Variable (जैसे 'BOT_TOKEN') से प्राप्त करें।
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found in environment variables.")
    # यह सिर्फ लोकल टेस्टिंग के लिए है, Vercel इसे स्वचालित रूप से सेट करेगा।
    # आप चाहें तो इसे यहाँ से हटा सकते हैं, या लोकल टेस्टिंग के लिए डिफ़ॉल्ट वैल्यू दे सकते हैं।
    # BOT_TOKEN = '8435173507:AAHvmzXt_ucIxXAMs3DNGqDg5-ugY_EAE7g' 

# आपका UPI ID
MY_UPI_ID = 'malikbadsha11@fam' 

# एडमिन चैट ID (जहाँ आपको UTR alerts चाहिए, आपका Personal Chat ID)
ADMIN_CHAT_ID = [8435173507] # इसे अपनी असली ID से बदलें। (Change this to your actual ID)

# डेटाबेस फ़ाइल का नाम
DB_FILE = 'users_data.json'
QR_CODE_PATH = 'QRcodespay.jpg' 

# --- POINTS & PRICING ---
POINTS_PER_RUPEE = 100 

# --- BOT INITIALIZATION ---
bot = telebot.TeleBot(BOT_TOKEN, threaded=False) # Webhook के लिए threaded=False

# --- DATABASE FUNCTIONS (पुराने कोड से) ---
# (load_data, save_data, get_user_data फंक्शन्स में कोई बदलाव नहीं)
def load_data():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_data(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            'balance': 0.0,
            'total_orders': 0.0,
            'total_deposits': 0.0,
            'order_history': [],
            'deposit_history': []
        }
        save_data(data)
    return data[user_id]

# --- KEYBOARD FUNCTIONS ---
# (get_main_menu_keyboard, get_order_menu_keyboard, आदि फंक्शन्स में कोई बदलाव नहीं)
def get_main_menu_keyboard():
    """Generates the main command reply keyboard (Video style)."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("💖 ACCOUNT"),
        types.KeyboardButton("🔥 ORDER NOW")
    )
    markup.add(
        types.KeyboardButton("📈 GUIDE"),
        types.KeyboardButton("✅ TRACK")
    )
    markup.add(
        types.KeyboardButton("🤖 BOT INFO"),
        types.KeyboardButton("📞 SUPPORT")
    )
    # Deposit बटन को मेन मेन्यू में जोड़ें (यह आपके पुराने कोड में हैंडलर में था, लेकिन कीबोर्ड में नहीं)
    markup.add(types.KeyboardButton("💰 DEPOSIT"))
    return markup

def get_order_menu_keyboard():
    """Generates the order section keyboard."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("100K OFFER"), 
        types.KeyboardButton("IG FOLLOW ⚡")
    )
    markup.add(
        types.KeyboardButton("INSTAGRAM 🔥"), 
        types.KeyboardButton("YOUTUBE 📺")
    )
    markup.add(
        types.KeyboardButton("FACEBOOK 💙"), 
        types.KeyboardButton("TELEGRAM 💬")
    )
    markup.add(
        types.KeyboardButton("TIK TOK 🎶"),
        types.KeyboardButton("🔙 Back to Main")
    )
    return markup

def get_instagram_menu_keyboard():
    """Generates the Instagram services keyboard."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Reels Views 🚀"),
        types.KeyboardButton("IG ~ LIKE 💖")
    )
    markup.add(
        types.KeyboardButton("REPOST ♻️"),
        types.KeyboardButton("SHARE 📢")
    )
    markup.add(
        types.KeyboardButton("COMMENT 💬"),
        types.KeyboardButton("🔙 Back to Orders")
    )
    return markup

def get_telegram_menu_keyboard():
    """Generates the Telegram services keyboard."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("TG Subscribe 🎯"),
        types.KeyboardButton("TG Like 💖")
    )
    markup.add(
        types.KeyboardButton("TG Post Views 👁️‍🗨️"),
        types.KeyboardButton("🔙 Back to Orders")
    )
    return markup


# --- HANDLERS (Messages) ---
# (सभी @bot.message_handler, @bot.message_handler, और सहायक फंक्शन्स में कोई बदलाव नहीं)
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    get_user_data(message.chat.id)
    text = f"""
👋 HEY **{message.from_user.first_name}**! Welcome to the Bot! 

🚀 **This is The Most Advance Social Marketing Bot.**
Grow Your Social Media Faster With Our Powerful Services.

Select an option from the menu below:
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_menu_selection(message):
    user_id = message.chat.id
    text = message.text

    if text == "🔙 Back to Main":
        send_welcome(message)
    
    elif text == "🔥 ORDER NOW":
        bot.send_message(user_id, "Welcome To Order Section!\n\nCHOOSE YOUR SERVICE:", reply_markup=get_order_menu_keyboard())
    
    elif text == "🔙 Back to Orders":
        bot.send_message(user_id, "Welcome Back To Order Section!", reply_markup=get_order_menu_keyboard())
    
    # --- Main Menu Commands ---
    elif text == "💖 ACCOUNT":
        handle_account_info(message)
    
    elif text == "📈 GUIDE":
        handle_guide(message)

    elif text == "📞 SUPPORT":
        handle_support(message)
    
    elif text == "🤖 BOT INFO":
        handle_bot_info(message)
        
    elif text == "✅ TRACK":
        bot.send_message(user_id, "Enter the Order ID you want to track:")
        bot.register_next_step_handler(message, process_track_order)

    # --- Order Menus ---
    elif text == "INSTAGRAM 🔥":
        bot.send_message(user_id, "Welcome to Instagram Services", reply_markup=get_instagram_menu_keyboard())
        
    elif text == "TELEGRAM 💬":
        bot.send_message(user_id, "Welcome to Telegram Options", reply_markup=get_telegram_menu_keyboard())

    # --- Service Prompts ---
    elif text in ["100K OFFER", "IG FOLLOW ⚡", "Reels Views 🚀", "IG ~ LIKE 💖", "REPOST ♻️", "SHARE 📢", "COMMENT 💬", 
                  "TG Subscribe 🎯", "TG Like 💖", "TG Post Views 👁️‍🗨️"]:
        service_map = {
            "100K OFFER": '100k_offer', "IG FOLLOW ⚡": 'followers', 
            "Reels Views 🚀": 'reels_views', "IG ~ LIKE 💖": 'like', 
            "REPOST ♻️": 'ig_repost', "SHARE 📢": 'ig_share', 
            "COMMENT 💬": 'ig_comment', "TG Subscribe 🎯": 'tg_subscribe',
            "TG Like 💖": 'tg_like', "TG Post Views 👁️‍🗨️": 'tg_post_views'
        }
        service_name = service_map.get(text, 'unknown')
        send_service_details(message, service_name)

    # --- Deposit Handler (New) ---
    elif text == "💰 DEPOSIT":
        deposit_menu(message)
        
    elif text == "REFER 🎉": 
        bot.send_message(user_id, "Referral System is coming soon!")
    
    # --- Default Case ---
    else:
        bot.send_message(user_id, "I did not recognize that command. Please use the keyboard buttons.", reply_markup=get_main_menu_keyboard())

# (handle_account_info, handle_bot_info, handle_support, handle_guide, process_track_order, send_service_details, deposit_menu, process_utr_step, admin_add_points, process_quantity_step, process_link_step फंक्शन्स में कोई बदलाव नहीं)
def handle_account_info(message):
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "N/A"
    user_data = get_user_data(user_id)
    
    balance_in_rupees = user_data['balance'] / POINTS_PER_RUPEE
    deposit_in_rupees = user_data['total_deposits'] / POINTS_PER_RUPEE
    
    text = f"""
👤 ᴜsᴇʀ : **{message.from_user.first_name}**
👋 ᴜsᴇʀɴᴀᴍᴇ : @{username}
🆔 ᴜsᴇʀ ɪᴅ : `{user_id}`

💸 **ʙᴀʟᴀɴᴄᴇ** : **{user_data['balance']:.1f}** ᴘᴏɪɴᴛs ~ ₹{balance_in_rupees:.2f}

🧾 ʏᴏᴜʀ ᴛᴏᴛᴀʟ ᴏʀᴅᴇʀ - {user_data['total_orders']:.1f} ᴘᴏɪɴᴛs

💸 ᴛᴏᴛᴀʟ ᴅᴇᴘᴏsɪᴛs :- {user_data['total_deposits']:.1f} ~ ₹{deposit_in_rupees:.2f} 
"""
    bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())

def handle_bot_info(message):
    data = load_data()
    total_order_points_demo = 63725178.0 # Static data from your video
    total_order_rupees_demo = total_order_points_demo / POINTS_PER_RUPEE
    
    text = f"""
📈 **100% Live Accurate Statistics**

🤵 Total Members : **{len(data)}** Users (Video: 1938 Users)

📑 Total Service Order Points : {total_order_points_demo:.0f} ~ ₹{total_order_rupees_demo:.0f} 

 💸 You Total Order : {get_user_data(message.chat.id)['total_orders']:.1f} Points ~ ₹{get_user_data(message.chat.id)['total_orders'] / POINTS_PER_RUPEE:.2f}
 
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

def handle_support(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Contact Me 📞", url='https://t.me/TRADERVIP11102'))
    bot.send_message(message.chat.id, "Support Information\n\n💰 If you have any order or deposit-related issue, click the button below 👇:", reply_markup=markup)

def handle_guide(message):
    text = "📚 **GUIDE SECTION**\n\nHere you can find tutorials and frequently asked questions about how to use the services and deposit funds."
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

def process_track_order(message):
    order_id = message.text.strip()
    bot.send_message(message.chat.id, f"Tracking Order ID `{order_id}`...\n\nStatus: Pending. Your order will be processed shortly.", parse_mode='Markdown', reply_markup=get_main_menu_keyboard())

def send_service_details(message, service_name):
    SERVICE_DETAILS = {
        'like': {
            'text': "➪ Iɴsᴛᴀɢʀᴀᴍ Pᴏsᴛ-Rᴇᴇʟ Lɪᴋᴇs 💞 \n➪ Pʀɪᴄᴇ: **₹2.5 = 100 Lɪᴋᴇs** (250 Pᴏɪɴᴛs)\n100% Iɴᴅɪᴀɴ 🇮🇳 Wɪᴛʜ DP & Sᴛᴏʀʏ 💗\n•Mɪɴɪᴍᴜᴍ Oʀᴅᴇʀ : 100 ( 250 Pᴏɪɴᴛ)\n🚀 Sᴘᴇᴇᴅ • 𝐁𝐔𝐋𝐄𝐓 \n\n**Enter IG Post Link** (𝐌𝐨𝐬𝐭 𝐁ᴇ 𝐏𝐮ʙʟɪᴄ 🖇️)",
            'cost_per_unit': 250, 'unit': 100
        },
        'followers': { 
            'text': "IG ~ FOLLOW (NON DROP) 💖 \n\n💸 Price : **₹18 per 100 Followers** (1800 Points)\n⚡ SPEED : ( MIDIUM 2 FAST )\n⏳ START TIME: 0~1 HOUR\nQUALITY : Old Accounts\n\n⚠️ **NOTE:** Your Account Most Be Public. \n\n**Send the Instagram profile link (must be public):**",
            'cost_per_unit': 1800, 'unit': 100
        },
        'ig_repost': {
            'text': "➪ Sᴇʀᴠɪᴄᴇ : 𝐈𝐆 ~ 𝐑𝐄𝐏𝐎𝐒𝐓 ♻️\n\n•**100 Rᴇᴘᴏsᴛ Oɴʟʏ ~ 6.Rs** (600 Points)\n• Mɪɴɪᴍᴜᴍ 100 Mᴀxx 10K \n•Sᴘᴇᴇᴅ (𝐅𝐀𝐒𝐓)\n\n**️Sᴇᴅɴ Mᴇ Yᴏᴜʀ Rᴇᴇʟ Lɪɴᴋ ( 𝗠𝗼𝘀𝘁 𝗕𝗲 𝗣𝘂ʙʟɪᴄ )**",
            'cost_per_unit': 600, 'unit': 100
        },
        'reels_views': {
            'text': "𝗜𝗚 ~ 𝗥𝗲𝗲𝗹𝘀 𝗩𝗶𝗲𝘄𝘀 𝗨𝗹𝗿𝘁𝗮 𝗙𝗮𝘀𝘁 🚀\n\n💸 Price : **₹5 = 10K** (500 Points)\n𝗨𝗹𝘁𝗿𝗮 𝗙𝗮𝘀𝘁 **1 𝗠𝗶𝗻𝘂𝘁𝗲** 𝗗𝗼𝗲𝗻 ✅\n🔰 Minimum Order : 5000 Views\n\n**Enter Reel Link (𝗠𝗼𝘀𝘁 𝗕𝗲 𝗣𝘂ʙʟɪᴄ)🖇️**",
            'cost_per_unit': 500, 'unit': 10000
        },
        '100k_offer': {
            'text': "➪ **100𝐊 𝐑𝐄𝐄𝐋 𝐕𝐈𝐄𝐖'𝐒** 🔥\n✨ 𝐁𝐈𝐆 𝐃𝐈𝐖𝐀𝐋𝐈 𝐎𝐅𝐅𝐄𝐑 ✨\n➪ Pʀɪᴄᴇ: Oɴʟʏ **₹15 Pᴇʀ 100𝐊 𝐕𝐈𝐄𝐖'𝐒** (1500 Pᴏɪɴᴛs)\n\n•Dʀᴏᴘ ( 𝐍𝐎𝐍 𝐃𝐑𝐎𝐏 ) 💧\n\n**Enter IG Post Link** (𝐌𝐨𝐬ᴛ 𝐁ᴇ 𝐏𝐮ʙʟɪᴄ 🖇️)",
            'cost_per_unit': 1500, 'unit': 100000
        },
        'tg_subscribe': {
            'text': "Service: Telegram Subscribe 🎯\n\nPrice: **₹8 per 100 Subs** → 800 Points\nMinimum Order: 100\nQuality: Instant Start, Top Quality.\n\n**Please send the Telegram channel link (must be public):**",
            'cost_per_unit': 800, 'unit': 100
        },
        'tg_post_views': {
            'text': "Service: Telegram Post Views 👁️‍🗨️\n\nPrice: **₹2 per 1000 Views** → 200 Points\nMinimum Order: 1000\nSpeed: ULTRA FAST Delivery\n\n**Please send a valid Telegram Post link:**",
            'cost_per_unit': 200, 'unit': 1000
        },
        'ig_share': {'text': "Share Service Details: Price ₹2 per 1000 Shares (200 Points). Enter link:", 'cost_per_unit': 200, 'unit': 1000},
        'tg_like': {'text': "TG Like Service Details: Price ₹8 per 1000 Likes (800 Points). Enter link:", 'cost_per_unit': 800, 'unit': 1000},
        
    }

    details = SERVICE_DETAILS.get(service_name, {'text': f"Details for {service_name.upper()} are not set yet.", 'cost_per_unit': 0})
    
    bot.send_message(message.chat.id, details['text'], parse_mode='Markdown')
    
    if details['cost_per_unit'] > 0:
        msg = bot.send_message(message.chat.id, f"Enter the quantity (Min: {details['unit']}):")
        bot.register_next_step_handler(msg, process_quantity_step, service_name, details)

def deposit_menu(message):
    user_id = message.chat.id
    try:
        qr_file = open(QR_CODE_PATH, 'rb')
        
        caption_text = f"""
**𝗘𝗻𝘁𝗲𝗿 𝗧𝗵𝗲 𝗔𝗺𝗼𝘂𝗻𝘁 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗗𝗲𝗽𝗼𝘀𝗶𝘁** 💰

**पेमेंट के निर्देश:**
1. **QR Code:** ऊपर दिए गए QR Code को स्कैन करें।
2. **UPI ID (Alternate):** `{MY_UPI_ID}`
3. **अमाउंट:** ₹10, ₹20, ₹30, ₹70 or any amount. (₹10 = 1000 Points)
4. **पेमेंट करें:** अपना UPI ऐप खोलें और पेमेंट करें।

*नोट: पेमेंट के बाद, कृपया **UTR/Transaction ID** नीचे चैट में भेजें।*
"""
        bot.send_photo(user_id, qr_file, caption=caption_text, parse_mode='Markdown')
        qr_file.close()

    except FileNotFoundError:
        caption_text = f"""
**𝗘𝗻𝘁𝗲𝗿 𝗧𝗵𝗲 𝗔𝗺𝗼𝘂𝗻𝘁 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗗𝗲𝗽𝗼𝘀𝗶𝘁** 💰

⚠️ **QR Code not found!** Ensure '{QR_CODE_PATH}' is available.

**पेमेंट के निर्देश:**
1. **UPI ID:** `{MY_UPI_ID}`
2. **अमाउंट:** ₹10, ₹20, ₹30, ₹70 or any amount. (₹10 = 1000 Points)
3. **पेमेंट करें:** अपना UPI ऐप खोलें और पेमेंट करें।

*नोट: पेमेंट के बाद, कृपया **UTR/Transaction ID** नीचे चैट में भेजें।*
"""
        bot.send_message(user_id, caption_text, parse_mode='Markdown')

    msg_utr = bot.send_message(user_id, "**Send your UTR NUMBER here:**")
    bot.register_next_step_handler(msg_utr, process_utr_step)

def process_utr_step(message):
    utr = message.text.strip()
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "N/A"
    
    if not utr.isdigit() or len(utr) < 8: 
        bot.send_message(user_id, "⚠️ Invalid UTR format. Please send the correct UTR/Transaction ID or use the menu buttons.", reply_markup=get_main_menu_keyboard())
        return
        
    admin_alert = f"""
🚨 **NEW DEPOSIT ALERT - UTR Verification**
👤 **User:** `{user_id}` (@{username})
🔢 **UTR:** `{utr}`
🔗 **Profile:** [Link to User](tg://user?id={user_id})

⚠️ **Action:** Verify and add points using /addpoints.
"""
    for admin_id in ADMIN_CHAT_ID:
        try:
            bot.send_message(admin_id, admin_alert, parse_mode='Markdown')
        except Exception:
            pass

    user_conf_text = f"""
✅ **UTR Received!**
Your UTR (`{utr}`) has been sent for verification.

Your points will be credited to your account **manually** after admin verification. Thank you for your patience!
"""
    bot.send_message(user_id, user_conf_text, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())

@bot.message_handler(commands=['addpoints'])
def admin_add_points(message):
    if message.chat.id not in ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "❌ Access Denied.")
        return
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(message.chat.id, "Usage: /addpoints <user_id> <points_to_add>")
            return
        target_user_id = parts[1]
        points_to_add = float(parts[2])
        data = load_data()
        if target_user_id not in data:
            bot.send_message(message.chat.id, f"User ID {target_user_id} not found.")
            return

        data[target_user_id]['balance'] += points_to_add
        data[target_user_id]['total_deposits'] += points_to_add
        data[target_user_id]['deposit_history'].append({'time': time.strftime("%Y-%m-%d %H:%M:%S"), 'points': points_to_add})
        save_data(data)

        bot.send_message(message.chat.id, f"✅ **{points_to_add:.1f} Points** added to User ID `{target_user_id}`.")
        try:
            bot.send_message(target_user_id, f"🥳 **{points_to_add:.1f} Points** added. New Balance: **{data[target_user_id]['balance']:.1f}** Points.", parse_mode='Markdown')
        except Exception:
            pass
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

def process_quantity_step(message, service_name, details):
    try:
        quantity = int(message.text.strip())
        if quantity < details.get('unit', 1): 
            bot.send_message(message.chat.id, f"Minimum order is {details.get('unit', 1)}. Please enter a valid quantity.", reply_markup=get_main_menu_keyboard())
            return
    except ValueError:
        bot.send_message(message.chat.id, "Invalid quantity. Please enter a valid number.", reply_markup=get_main_menu_keyboard())
        return

    points_needed = (quantity / details['unit']) * details['cost_per_unit']
        
    user_data = get_user_data(message.chat.id)
    
    if user_data['balance'] < points_needed:
        bot.send_message(message.chat.id, f"❌ **Insufficient Balance!** You need **{points_needed:.1f}** points but have only **{user_data['balance']:.1f}** points.", parse_mode='Markdown', reply_markup=get_main_menu_keyboard())
        return
        
    bot.send_message(message.chat.id, f"✅ Balance Check OK. Cost: **{points_needed:.1f}** Points.\n\nNow, please send the **Link** (Post/Profile) for the {service_name.upper()} order:", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_link_step, service_name, quantity, points_needed)

def process_link_step(message, service_name, quantity, points_needed):
    link = message.text.strip()
    user_id = str(message.chat.id)
    
    data = load_data()
    data[user_id]['balance'] -= points_needed
    data[user_id]['total_orders'] += points_needed
    data[user_id]['order_history'].append({
        'time': time.strftime("%Y-%m-%d %H:%M:%S"),
        'service': service_name,
        'quantity': quantity,
        'cost': points_needed,
        'link': link
    })
    save_data(data)
    
    confirmation_text = f"""
🎉 **ORDER PLACED SUCCESSFULLY!**

Service: **{service_name.upper()}**
Quantity: **{quantity}**
Cost: **{points_needed:.1f}** Points
Link: `{link}`

⏳ Your order is being processed. New Balance: **{data[user_id]['balance']:.1f}** Points.
"""
    bot.send_message(message.chat.id, confirmation_text, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())


# --- WEBHOOK SETUP (Vercel के लिए मुख्य बदलाव) ---
app = Flask(__name__)

# Vercel द्वारा प्रदान किए गए URL का उपयोग करें
@app.route('/', methods=['GET'])
def index():
    # यह सिर्फ यह जांचने के लिए है कि Vercel पर ऐप चल रहा है या नहीं
    return "Telegram Bot is running! Use the webhook route."

# यह वह रूट है जहाँ Telegram मेसेज भेजेगा
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.method == "POST":
        # Telegram से प्राप्त JSON डेटा को प्रोसेस करें
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    return "OK", 200

# मुख्य भाग (जो Vercel पर एक बार चलता है)
# Vercel/क्लाउड होस्टिंग के लिए, हम Webhook सेट करते हैं
def set_up_webhook():
    # Vercel आपको एक URL देगा, जैसे: https://my-bot-name.vercel.app
    # सुनिश्चित करें कि आपने Vercel पर अपने ऐप का सही डोमेन नाम इस्तेमाल किया है
    WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST', 'YOUR_VERCEL_APP_URL.vercel.app') 
    
    # यह वह रूट है जो Telegram को पता होगा
    WEBHOOK_URL = f"https://{WEBHOOK_HOST}/{BOT_TOKEN}"
    
    # यदि BOT_TOKEN उपलब्ध है, तो Webhook सेट करें
    if BOT_TOKEN:
        bot.remove_webhook()
        time.sleep(1) # प्रतीक्षा करें
        bot.set_webhook(url=WEB