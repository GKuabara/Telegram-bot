from telegram.ext import InlineQueryHandler, Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from env import TOKEN
from ping_pong import pong_join, pong_leave, pong_lobby
from ping_pong import CHOOSE_OPPONENT, RUN_GAME, pong_play, choose_opponent, run_game

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")