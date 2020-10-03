from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler

import logging
from env import TOKEN

def start(update, context):
	send = "No worries people, KuBot is HERE"
    update.message.reply_text(send)


def main():
	logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

	updater = Updater(token=TOKEN, use_context=True)	
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	#commands:

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	print("Bot Ass Hole Active")
	main()
	print("Bot Ass Hole was BANIDO")