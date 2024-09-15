import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext

# Bot Token from Environment Variable (Heroku will set this later)
TOKEN = os.environ.get('BOT_TOKEN')
GROUP_A_ID = os.environ.get('GROUP_A_ID')  # ID of Group A (where members will be fetched)
GROUP_B_ID = os.environ.get('GROUP_B_ID')  # ID of Group B (where members will be added)

bot = Bot(token=TOKEN)

# Command to fetch members and send invites
def fetch_members(update: Update, context: CallbackContext):
    # Fetch up to 100 members from Group A
    chat_id = GROUP_A_ID
    members = bot.get_chat_administrators(chat_id)[:100]
    
    for member in members:
        try:
            # Generate invite link for Group B and send to user
            invite_link = bot.export_chat_invite_link(chat_id=GROUP_B_ID)
            bot.send_message(chat_id=member.user.id, text=f"Join Group B: {invite_link}")
        except Exception as e:
            update.message.reply_text(f"Failed to invite {member.user.username}: {e}")
    
    update.message.reply_text("Invites sent to selected members!")

# Setting up the bot and command handler
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for fetching members
    dispatcher.add_handler(CommandHandler('fetch_members', fetch_members))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
