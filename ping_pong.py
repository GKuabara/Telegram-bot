from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from random import randint

CHOOSE_OPPONENT, RUN_GAME = range(2)

class Match:
    def __init__(self, p1, p2=None):
        self.p1 = p1
        self.p2 = p2
        self.pongs1 = None
        self.pongs2 = None
        self.winner = None

class Lobby():
    def __init__(self, name):
        self.name = name
        self.match = None
        self.players = dict()

    def join_lobby(self, response, username, user_id):
        if username not in self.players.keys():
            self.players[username] = user_id
            response.append(f"Bem vinde {username}!")
        else:
            response.append("Tu já tá aqui!")

    def leave_lobby(self, response, username):
        if username in self.players.keys():
            response.append(f"Flw {username}!")
            del self.players[username]
        else:
            response.append("Tu não tá no lobby!")

    def print_lobby(self, response):
        if self.players:
            response.append(f"★ {self.name}'s Lobby ★")
            for username in self.players.keys():
                response.append(f"- {username}")
        else:
            response.append("O lobby tá vazio :(")

    def create_match(self, response, p1_username):
        if p1_username not in self.players.keys():
            response.append("Tu não tá no lobby! da /pongjoin antes ae ...")
            return False

        if self.match:
            response.append("Tem uma partida rolando, pera um tico!") 
            return False

        self.match = Match(p1_username)
        return True

    def get_opponents(self, response, p1_username):
        opponents = list(self.players.keys())
        opponents.remove(p1_username)

        if not opponents:
            response.append("Só tu tá no lobby! Solitarie ...")
            self.match = None

        return opponents

    def _gen_match_result(self, response, match):
        response.append("Caboooou!\n")
        response.append(f"{match.p1} {match.pongs1} x {match.pongs2} {match.p2}\n")
        if match.pongs1 == match.pongs2:
            response.append(f"Empatou que merda!")
        else:
            match.winner = match.p1 if match.pongs1 > match.pongs2 else match.p2
            response.append(f"{match.winner} taxou, nice!")


    def run_match(self, response, bot):
        print("lobby.run_match ...\n")
        p1_id = self.players[self.match.p1]
        p2_id = self.players[self.match.p2]
        match = self.match

        # try:
        #     bot.send_message(chat_id=p1_id, text="eae player 1")
        # except:
        #     response.append(f"{match.p1} vai na minha dm e clica em start na moral...")
        #     match = None
        #     return

        # try:
        #     bot.send_message(chat_id=p2_id, text="eae player 2")
        # except:
        #     response.append(f"{match.p2} vai na minha dm e clica em start na moral...")
        #     match = None
        #     return

        match.pongs1 = randint(0, 50)
        match.pongs2 = randint(0, 50)
        self._gen_match_result(response, match)

        self.match = None

def pong_join(update, context):
    registered_lobbys = context.chat_data
    curr_msg = update.message
    curr_chat_id = curr_msg.chat.id

    if curr_chat_id not in registered_lobbys.keys():
        chat_name = curr_msg.chat.title
        registered_lobbys[curr_chat_id] = Lobby(chat_name.split()[0])
        context.bot.send_message(chat_id=curr_chat_id, text="Novo chat foi registrado com sucesso!\n")

    user_id = curr_msg.from_user.id
    username = f"@{curr_msg.from_user.username}"

    response = list()
    registered_lobbys[curr_chat_id].join_lobby(response, username, user_id)
    curr_msg.reply_text("\n".join(response))

def pong_leave(update, context):
    registered_lobbys = context.chat_data
    curr_msg = update.message
    curr_chat_id = curr_msg.chat.id

    response = list()
    if curr_chat_id not in registered_lobbys.keys():
        response.append("Chat não registrado! Manda um /pongjoin antes...")
    else:
        username = f"@{curr_msg.from_user.username}"
        registered_lobbys[curr_chat_id].leave_lobby(response, username)

    curr_msg.reply_text("\n".join(response))

def pong_lobby(update, context):
    registered_lobbys = context.chat_data
    curr_msg = update.message
    curr_chat_id = curr_msg.chat.id

    response = list()
    if curr_chat_id not in registered_lobbys.keys():
        response.append("Chat não registrado! Manda um /pongjoin antes...")
    else:
        registered_lobbys[curr_chat_id].print_lobby(response)

    curr_msg.reply_text("\n".join(response))

def choose_opponent(update, context):
    query = update.callback_query
    curr_chat_id = query.message.chat.id
    registered_lobbys = context.chat_data

    query.answer()

    match = registered_lobbys[curr_chat_id].match
    match.p2 = query.data

    query.edit_message_text(text=f"{match.p1} responde aqui pra começar contra o {match.p2} pls...\n")

    return RUN_GAME

def _set_match(curr_msg, p1_username, lobby):
    response = list()
    if not lobby.create_match(response, p1_username):
        curr_msg.reply_text("\n".join(response))
        return ConversationHandler.END

    opponents = lobby.get_opponents(response, p1_username)
    if not opponents:
        curr_msg.reply_text("\n".join(response))
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton(opp, callback_data=opp)] for opp in opponents]
    reply_markup = InlineKeyboardMarkup(keyboard)

    response.append("Contra quem esse x1?")
    curr_msg.reply_text("\n".join(response), reply_markup=reply_markup)

    return CHOOSE_OPPONENT

def pong_play(update, context):
    registered_lobbys = context.chat_data
    curr_msg = update.message
    curr_chat_id = curr_msg.chat.id

    if curr_chat_id not in registered_lobbys.keys():
        curr_msg.reply_text("Chat não registrado! Manda um /pongjoin antes...")
        return ConversationHandler.END

    lobby = registered_lobbys[curr_chat_id]
    if not lobby:
        curr_msg.reply_text("O lobby tá vazio :(")
        return ConversationHandler.END

    p1_username = f"@{curr_msg.from_user.username}"
    return _set_match(curr_msg, p1_username, lobby)

def run_game(update, context):
    registered_lobbys = context.chat_data
    curr_msg = update.message
    curr_chat_id = curr_msg.chat.id

    response = list()
    registered_lobbys[curr_chat_id].run_match(response, context.bot)

    context.bot.send_message(chat_id=curr_chat_id, text="\n".join(response))

    return ConversationHandler.END