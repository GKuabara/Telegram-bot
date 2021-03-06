from telegram.ext import InlineQueryHandler, Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
# from env import TOKEN OWM_KEY
# from weather import clima
import pandas as pd
import rand_poke
import logging
import corona
import random
import animes
import json
import random as rd
import os
import imageio
import sys

from ping_pong import pong_join, pong_leave, pong_lobby
from ping_pong import CHOOSE_OPPONENT, RUN_GAME, pong_play, choose_opponent, run_game

TOKEN = "1140857640:AAGEEX5lP5uIxcJxxSAGPIT4HVO87i8Bxrg"

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

def randomSong(update, context):
    playlist = pd.read_csv("kulto.csv")
    songs = playlist["Track Name"] + ' - ' + playlist["Artist Name"]
    song = random.choice(songs)
    
    context.bot.sendMessage(chat_id=update.message.chat_id, text=f"Vamo de '{song}'")

sentImages = list()
def miranha(update, context):
    spiderJSON = open("JSON/miranha.json", "r")

    spider = json.loads(spiderJSON.read())
    rand_image = random.choice(list(spider.items()))

    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open(f"Homiranha/{rand_image[0]}", "rb"), caption=rand_image[1])
    spiderJSON.close()

def casosCorona(update, context):
    chatId = update.effective_chat.id

    states = ["ac", "al", "ap", "am", "ba", "ce", "es", "go", "ma", "mt", "ms", "mg", "pa", "pb", "pr", "pe", "pi", "rj", "rn", "rs", "ro", "rr", "sc", "sp", "se", "to"]
    wantedStates = set(context.args)
    if len(wantedStates) == 0:
        response = "Coloca a sigla de pelo menos um estado pra eu saber, pô"
        context.bot.sendMessage(parse_mode='HTML', chat_id=chatId, text=response)
        return

    for state in wantedStates:
        state = state.lower()
        if state not in states:
            context.bot.sendMessage(parse_mode='HTML', chat_id=chatId, text=f"Vish! Deu ruim... Que estado é '{state}'?")
        else:
            txt = corona.stateRequest(state)
            if txt != "":
                context.bot.sendMessage(parse_mode='HTML', chat_id=chatId, text=txt)
            else:
                context.bot.sendMessage(parse_mode='HTML', chat_id=chatId, text=f"Opa, deu ruim no request da '{state}'")
                return

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

def loadFile(filename):
    with open(filename, encoding="UTF-8") as f:
        content = [l.strip() for l in f]

    return content

def distort(imageIn, imageOut, dims, pct=50):

    print(f"{pct}%: {imageIn} -> {imageOut}")
    os.system(f"magick {imageIn} -liquid-rescale {pct}x{pct}%! -resize {dims[1]}x{dims[0]}! {imageOut}")

def deleteDirs(file, user_id):

    os.remove(f"{file[:-4]}{file[len(file) -  4::]}")


def sagadoku(update, context):

    image = "./pics/"
    filmeList = loadFile("filme.txt")
    user_id = update.message.from_user.id
    update.message.reply_text("já vai já vai")	

    pick = rd.choice(filmeList)
    position = filmeList.index(pick)
    image += f"pic{position}.jpg"
    dims = imageio.imread(image).shape
    imageOut = f"distorted{user_id}.jpg"
    distort(image, imageOut, dims)
    caption = pick.replace("{word}", "ku")
    print(caption)

    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open(imageOut, "rb"), caption=caption, parse_mode="html")

    deleteDirs(imageOut, user_id)


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    updater = Updater(token=TOKEN, use_context=True)	
    dp = updater.dispatcher


    dp.add_handler(CommandHandler("pokemon", pokemon))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("musica", randomSong))
    # dp.add_handler(CommandHandler("clima", clima))
    dp.add_handler(CommandHandler("sagadoku", sagadoku))
    dp.add_handler(CommandHandler("tiranota", tiranota))
    dp.add_handler(CommandHandler("corona", casosCorona))
    dp.add_handler(CommandHandler("miranha", miranha))
    dp.add_handler(CommandHandler("animealeatorio", animealeatorio))

    dp.add_handler(CommandHandler('pongjoin', pong_join))
    dp.add_handler(CommandHandler('pongleave', pong_leave))
    dp.add_handler(CommandHandler('ponglobby', pong_lobby))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pongplay', pong_play)],
        states={
            CHOOSE_OPPONENT: [CallbackQueryHandler(choose_opponent)],
            RUN_GAME: [MessageHandler(Filters.text, run_game)]
        },
        fallbacks=[]
    ))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    print("Bot Ass Hole Active")
    main()
    print("Bot Ass Hole was BANIDO")