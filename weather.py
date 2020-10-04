import datetime as dt
from env import OWM_KEY
from googletrans import Translator
from pyowm import OWM
from telegram.ext import Updater, Dispatcher, CommandHandler

owm = OWM(OWM_KEY)
mgr = owm.weather_manager()

observation = mgr.weather_at_place("Sao Carlos, BR")
w = observation.weather

translator = Translator()

def format_weather_info(weather):
    response = {'captions': []}
    
    response['icon']= f"./icons/{weather.weather_icon_name}.png"

    temp = weather.temperature('celsius')
    time = translator.translate(dt.datetime.today().strftime("%A, %d. %B %Y %I:%M%p"), dest='pt').text
    response['captions'].append(f"{time}")
    response['captions'].append(f"Temperatura atual: {temp['temp']}")
    response['captions'].append(f"Max: {temp['temp_max']} | Min: {temp['temp_min']}")
    
    return response
    

print(format_weather_info(w))

def clima(update, context):
    print("sup")
    city = " ".join(context.args)
    
    if not city:
        update.message.reply_text("Mai de qual cidade tu quer ver o clima?")
        return

    try:
        w = mgr.weather_at_place(f"{city}, BR").weather
        response = format_weather_info(w)
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(response['icon'], "rb"),
            caption="\n".join(response['captions'])
        )

    except:
        update.message.reply_text("Grrrr insira uma cidade válida se não vou chamar o kibon")
        