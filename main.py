from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters
from env import TOKEN # OWM_KEY
from weather import clima
import logging
import random
import json
import rand_poke
import animes

def start(update, context):
    send = "No worries people, KuBot has arrived!"
    update.message.reply_text(send)	

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

types1 = "'Grass', 'Fire', 'Water', 'Bug', 'Normal', 'Poison', 'Electric', 'Ground', 'Fairy', 'Fighting', 'Psychic', 'Rock', 'Ghost', 'Ice', 'Dragon', 'Dark', 'Steel', 'Flying'"
types2 = " 'Poison', 'None', 'Flying', 'Dragon', 'Ground', 'Fairy', 'Grass', 'Fighting', 'Psychic', 'Steel', 'Ice', 'Rock', 'Dark', 'Water','Electric', 'Fire', 'Ghost', 'Bug', 'Normal'"
def pokemon(update, context):
    text = context.args
    chatId = update.message.chat_id
    messageId = update.message.message_id
    username = update.message.from_user.username
    username = f"@{username}"
    msg = ""
    if len(text) < 1 or len(text) > 2:
        msg = f"{username}<i>, especifique o tipo primário (e secundario se quiser) do pokemon que deseja ser.\nTipos disponíveis: \nTipo 1:{types1}\nTipo 2: {types2}.</i>"	 
    else:
        poke = None
        text[0] = text[0].capitalize()		
        if text[0] not in types1:
            msg = f"{username}<i>, amigão, faz um favor, bota o tipo certinho em ingles, eu capitalizo pra ti, mas bota em americano.</i>"
        if len(text) == 2:
            text[1] = text[1].capitalize()
            if text[1] not in types2:
                msg = f"{username}<i>, amigão, faz um favor, bota o segundo tipo certinho em ingles, eu capitalizo pra ti, mas bota em americano.</i>"		

        if len(text) == 1: poke = rand_poke.random_pokemon(text[0])
        elif len(text) == 2: poke = rand_poke.random_pokemon(text[0], text[1])
        
        if poke: msg = f"<i>Boa</i> {username}<i>, teu pokemon capturado pseudoaleatoriamente é {poke}. Vai batalhar agora</i>"	
        elif not msg: msg = f"{username}<i>, errou a pokebola em campeão!!!!</i>"
    
    context.bot.sendMessage(parse_mode='HTML', chat_id = chatId, text = msg, reply_to_message_id = messageId)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, invalid command, @{}?".format(update.effective_user.username))

def animealeatorio(update, context):
    chatId = update.message.chat_id
    messageId = update.message.message_id

    infos = animes.randAnime()
    animeData = infos[1]
    id = list(animeData.keys())
    animeInfos = list(animeData[id[5]][0].keys())
    while True:
        animeId = random.randint(1, 305)
        try:
            link = animeData[id[5]][animeId][animeInfos[1]]
            name = animeData[id[5]][animeId][animeInfos[2]]
            break
        except:
            pass
    
    msg = f"Seu anime {name} é do ano {infos[0]}:\n {link}"
    context.bot.sendMessage(parse_mode='HTML', chat_id = chatId, text = msg, reply_to_message_id = messageId)

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    updater = Updater(token=TOKEN, use_context=True)	
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("pokemon", pokemon))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clima", clima))
    dp.add_handler(CommandHandler("tiranota", tiranota))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(CommandHandler("animealeatorio", animealeatorio))
    #commands:

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    print("Bot Ass Hole Active")
    main()
    print("Bot Ass Hole was BANIDO")