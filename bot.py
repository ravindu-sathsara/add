import telebot
from telebot import types

API_TOKEN = '7527474500:AAEXhDJqMYTU7fku4eeVsTx_liY8dQAlZ5w'
bot = telebot.TeleBot(API_TOKEN)

# Command to remove or ban all members
@bot.message_handler(commands=['banall'])
def ban_all_members(message):
    if message.chat.type == "supergroup" or message.chat.type == "group":
        bot_admins = bot.get_chat_administrators(message.chat.id)
        bot_admin_ids = [admin.user.id for admin in bot_admins]
        
        # Ensure the bot is an admin
        if bot.get_me().id in bot_admin_ids:
            bot.send_message(message.chat.id, "Bot is starting to ban all members!")
            
            # Get all members of the group
            for member in bot.get_chat_members(message.chat.id):
                try:
                    if member.user.id not in bot_admin_ids:  # Don't ban other admins
                        bot.ban_chat_member(message.chat.id, member.user.id)
                        bot.send_message(message.chat.id, f"Banned: {member.user.first_name}")
                except Exception as e:
                    bot.send_message(message.chat.id, f"Could not ban: {member.user.first_name} - {str(e)}")
        else:
            bot.send_message(message.chat.id, "I need to be an admin to ban members.")
    else:
        bot.send_message(message.chat.id, "This command works only in groups.")

# Start polling the bot
bot.infinity_polling()
