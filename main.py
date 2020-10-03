from telegram.ext import CommandHandler, Updater, MessageHandler

import logging
from env import TOKEN

def start(update, context):
	

def main():
	updater = Updater(token=TOKEN, use_context=True)	
	dp = updater.dispatcher

	#commands:

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	print("Bot Ass Hole Active")
	main()
	print("Bot Ass Hole was BANIDO")