from typing import final
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from utiis import download_video , download_audio

load_dotenv()

BOT_USERNAME= os.getenv("PRIMEBOT_USERNAME")
TOKEN = os.getenv("PRIMETGAPI_TOKEN")
TERMS_MESSAGE = """
*📜 Introduction*
These Terms & Conditions govern your use of our Telegram bot. By using our bot, you agree to these terms. If you do not agree, please discontinue use immediately.

*📌 Use of Media and Copyright Notice*
We do not claim ownership of any media content saved or shared using our bot. All copyrights belong to their respective owners. We are not responsible for any unauthorized use of copyrighted material.

*🌐 Third-Party Associations*
We are not officially connected with any social media platform. Use at your own discretion.

*⬇️ Downloading Social Media Data*
We can only download publicly available data. Third-party services may be used to process links.

*⚠️ Service Disclaimer*
We aim for stability, but service may be interrupted or ended at any time. We’re not liable for damages resulting from service issues.

*🛡️ Indemnity*
You agree to hold us harmless from any claims related to your use of the bot.

*🔄 Changes to Terms*
We may update these at any time. Continued use means acceptance.

*📬 Contact*
For questions, contact: @PrimeSaverSupportBot
"""
PRIVACY_POLICY = """
🔒 *Privacy Policy*

*1. Introduction*  
This Privacy Policy explains how we collect, use, and protect your information when you use our Telegram bot. By using the bot, you agree to this policy.

*2. Information We Collect*  
• *Telegram User ID:* Collected to identify you as a user.  
• *General Data:* We may use data like your language to generate bot usage statistics.

*3. Cookies and Tracking*  
We do not use cookies or tracking technologies.

*4. Downloading Social Media Data*  
• *Public Data Only:* We only download publicly available content.  
• *Third-Party Services:* Media downloads are handled by external tools that do not receive your personal info—only media links.

*5. Data Storage & Security*  
• We do *not* store chat history.  
• Media may link to external sites. Review their privacy policies.  
• Ads may be shown occasionally. Clicking them leads outside the bot; we advise checking external policies.  
• We use modern encryption and best practices to protect your data.

*6. Payment Processing*  
Some features may require payment. We do not process payments ourselves—please review the privacy policy of the payment provider.

*7. Age Restriction*  
Our bot is intended for users aged *18 and above*. If you are under 18, please stop using the bot.

*8. Policy Changes*  
We may update this Privacy Policy. Please check periodically for changes.

*9. Contact Us*  
For any questions, contact us via [@PrimeSaverSupportBot](https://t.me/PrimeSaverSupportBot)

*10. Use of Media*  
This bot serves as a media bookmarking tool. We do not claim ownership of content saved or shared via this bot.

*11. Copyright Notice*  
All rights belong to original creators. Always seek permission before sharing content.
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Send your video URL here 🎥")
    await send_pinned_ad(update, context)

async def terms_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TERMS_MESSAGE, parse_mode=ParseMode.MARKDOWN )

async def privacy_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(PRIVACY_POLICY, parse_mode=ParseMode.MARKDOWN )

async def send_pinned_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    ad_text = "🔥 Want to make money online? Click the link below 👇\n[Ad] Earn from home 💸"
    ad_url = "https://www.profitableratecpm.com/q3kdk49ih?key=06f9eb9a496c602b5b0e39cba2d700cd" 

    #  Inline button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Check it out", url=ad_url)]
    ])

    # Send the ad message
    sent_message = await context.bot.send_message(
        chat_id=chat_id,
        text=ad_text,
        reply_markup=keyboard
    )

    # Pin it
    try:
        await context.bot.pin_chat_message(
            chat_id=chat_id,
            message_id=sent_message.message_id,
            disable_notification=True
        )
    except Exception as e:
        print(f"❌ Failed to pin message: {e}")



#responses
def handle_video_response(link: str) -> str:
   return download_video(link)

def handle_audio_response(link: str) -> str:
    return download_audio(link)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    link: str = update.message.text.strip()

    print(f"{update.message.chat.id} in {message_type}: {link}")

    #checking if the message was sent in a group and removing the bot name if it was tagged
    if message_type == 'group' and BOT_USERNAME in link:
        link = link.replace(BOT_USERNAME, '').strip()
    else:
        link = link

    #checking if the audio command was used 
    if '@toaudio' in link:
        link = link.replace('@toaudio', '').strip()
        link = link.replace('@toaudio', '').strip()
        file_path = handle_audio_response(link)
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as audio:
                    await context.bot.send_audio(
                            chat_id=update.message.chat_id,
                            audio=audio,
                            reply_to_message_id=update.message.message_id,
                            caption="This is the audio")
                          
            except Exception as e:
                await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"❌ Couldn't send the video: {e}",
                    reply_to_message_id=update.message.message_id
                )
            finally:
                os.remove(file_path)
    else:
        file_path = handle_video_response(link)

        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as video:
                    await context.bot.send_video(
                            chat_id=update.message.chat_id,
                            video=video,
                            reply_to_message_id=update.message.message_id)
            except Exception as e:
                await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"❌ Couldn't send the video: {e}",
                    reply_to_message_id=update.message.message_id
                )
            finally:
                os.remove(file_path)
                     
async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"{context.error}, was made")


if __name__ == '__main__' :
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('terms', terms_command))
    app.add_handler(CommandHandler('privacy', privacy_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    app.add_error_handler(error)
    print('Polling')
    app.run_polling(poll_interval=3)







