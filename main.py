from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters

import logging
from env import TOKEN

def start(update, context):
	send = "No worries people, KuBot has arrived!"
	update.message.reply_text(send)

def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
	text_caps = ' '.join(context.args).upper()
	context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)	

def unknown(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, invalid command, @{}?".format(update.effective_user.username))

def main():
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
	
	updater = Updater(token=TOKEN, use_context=True)	
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
	dp.add_handler(CommandHandler("caps", caps))
	dp.add_handler(MessageHandler(Filters.command, unknown))
	#commands:

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	print("Bot Ass Hole Active")
	main()
	print("Bot Ass Hole was BANIDO")