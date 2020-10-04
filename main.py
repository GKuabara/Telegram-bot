from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters
from env import TOKEN, OWM_KEY
from weather import clima
import logging
import random
import json

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

def tiranota(update, context):
	casesFile = open("JSON/tiranota.json", "r")
	cases = casesFile.read()
	
	casesContent = json.loads(cases).values()
	phrase = "<i>" + random.choice(list(casesContent))
	gradeDiscount = random.randint(1, 10)
	if gradeDiscount == 10:
		response = phrase + "Zerou parceiro, até ano q vem</i>"
	else:
		response = phrase + f"Vou tirar {gradeDiscount} pontos da sua nota</i>"

	chatId = update.message.chat_id
	context.bot.sendMessage(parse_mode='HTML', chat_id = chatId, text = response)
	casesFile.close()

def main():
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
	
	updater = Updater(token=TOKEN, use_context=True)	
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
	dp.add_handler(CommandHandler("caps", caps))
	# dp.add_handler(CommandHandler("clima", clima))
	dp.add_handler(CommandHandler("tiranota", tiranota))
	dp.add_handler(MessageHandler(Filters.command, unknown))
	#commands:

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	print("Bot Ass Hole Active")
	main()
	print("Bot Ass Hole was BANIDO")