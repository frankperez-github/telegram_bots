import telebot
import datetime
from telegram import BotCommand

today = datetime.datetime.today()

def getUserById(id):
    for user in users:
        if user['id'] == id:
            return user
        
def getWeekDay(day):
    match day.lower():
        case "hoy":
            return today.weekday()
        case "mañana":
            return today.weekday()+1
        case "lunes":
            return 0
        case "martes":
            return 1
        case "miércoles":
            return 2
        case "miercoles":
            return 2
        case "jueves":
            return 3
        case "viernes":
            return 4
        case "sábado":
            return 5
        case "sabado":
            return 5
        case "domingo":
            return 6
        case _:
            return -1


BOT_TOKEN = "6472890380:AAHR5mZ2mSRNn-5vz_-zaxjrGMiLwIaMUMk"

users = [
    {
        "id": 1120511499,
        "name": "frankperez24",
        "week":[
            [
                {
                    "hour": "00:00",
                    "description": "LP zzzz"
                }
            ],
            ["Martes"],
            ["Miércoles"],
            ["Jueves"],
            ["Viernes"],
            ["Sábado"],
            ["Domingo"]
        ],
        "events":[
            {
                "date": "2024-3-7",
                "description": "Cumple Shanik hoy"
            }
        ],
        "isAdding": False,
        "editingActivity": {
            "editingDay": False,
            "editingHour": False,
            "editingDescr": False,
            "activity":{
                "day": "",
                "hour": "",
                "description": ""
            }
        }
    }
]

bot = telebot.TeleBot(BOT_TOKEN)
commands = [
    telebot.types.BotCommand("/start", "the game begins"), 
    telebot.types.BotCommand("/delete_schedule", "deletes old schedule"), 
    telebot.types.BotCommand("/add_activity", "adds an activity to a specific day of your week"),
    telebot.types.BotCommand("/create_event", "creates an event, events will be set in a specific date of the year"),
    telebot.types.BotCommand("/cancel_adding", "cancels an event or activity creation")
]
bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
def start(message):
    for user in users:
        if user['id'] == message.from_user.id:
            bot.reply_to(message, "Ya tienes un horario comenzado, no necesitas volver a iniciar. Si quieres borrar tu horario anterior presiona /delete_schedule")
            bot.send_message(text="Para conocer tu horario escribeme un dia de la semana", chat_id=user['id'])
            return
    bot.reply_to(message, "Hola "+message.from_user.username)
    users.append({
        "id": message.from_user.id,
        "name": message.from_user.username,
        "week":[
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
            ["No hay nada programado aún"],
        ],
        "events":[
            {
                "date": "00-00-0000",
                "description": "No hay eventos"
            }
        ]
    })

@bot.message_handler(commands=['delete_schedule'])
def deleteAll(message):
    for user in users: 
        if(user['id'] == message.from_user.id):
            user['week'] = [
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
                ["No hay nada programado aún"],
            ]
            user['events'] = [{
                "date": "00-00-0000",
                "description": "No hay eventos"
            }]
    bot.reply_to(message, "Horario reestablecido, puedes comenzar todo desde cero ahora")



@bot.message_handler(commands=['add_activity'])
def addActivity(message):
    if not getUserById(message.from_user.id)['isAdding']:
        for user in users:
            if user['id'] == message.from_user.id:
                user['isAdding'] = True
        bot.reply_to(message, "Para crear su actividad presione /set_day")
    else:
        bot.reply_to(message, "Ya estabas creando un evento o actividad, si quieres dejar de crear presiona /cancel_adding")

@bot.message_handler(commands=['cancel_adding'])
def cancelAdding(message):
    for user in users:
            if user['id'] == message.from_user.id:
                user['isAdding'] = False
    bot.reply_to(message, "Adición cancelada, ya puedes seguir usando las demas funcionalidades")

@bot.message_handler(commands=['set_day'])
def setDay(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    bot.send_message(chat_id=message.from_user.id, text="Introduce el horario de la actividad con el formato hh:mm")

@bot.message_handler(commands=['set_hour'])
def setHour(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    bot.send_message(chat_id=message.from_user.id, text="Introduce el horario de la actividad con el formato hh:mm")


@bot.message_handler(commands=['editar_hora'])
def edit_h(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    for user in users:
        if user['id'] == message.from_user.id:
            user['editingActivity']['editingHour'] = True
    bot.reply_to(message, "Introduce la hora")

@bot.message_handler(commands=['aceptar_hora'])
def accept_h(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    for user in users:
        if user['id'] == message.from_user.id:
            user['editingActivity']['editingHour'] = False
    bot.reply_to(message, "Introduce el nombre de tu actividad")

@bot.message_handler(commands=['editar'])
def edit(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    for user in users:
        if user['id'] == message.from_user.id:
            user['editingActivity']['editingDescr'] = True
    bot.reply_to(message, "Introduce el nombre de la actividad")

@bot.message_handler(commands=['aceptar'])
def accept(message):
    if not getUserById(message.from_user.id)['isAdding']:
        bot.reply_to(message, "Primero comienza a crear una actividad o evento")
        return 
    for user in users:
        if user['id'] == message.from_user.id:
            user['editingActivity']['editingDescr'] = False
            user["isAdding"] = False
    user = getUserById(message.from_user.id)
    bot.reply_to(message, "Agregado:\n"+user['editingActivity']['activity']['hour']+"->"+user['editingActivity']['activity']['description'])

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user = getUserById(message.from_user.id)
    if(user['isAdding']):
        if user['editingActivity']['activity']['hour'] == "" or user['editingActivity']['editingHour']:
            hour = message.json['text'].split(':')[0]
            try:
                minutes = message.json['text'].split(':')[1]
            except IndexError:
                minutes = "00"
            bot.reply_to(message, "Hora de la actividad: "+hour+":"+minutes+". Puedes /aceptar_hora o /editar_hora")
            for user in users:
                if user['id'] == message.from_user.id:
                    user['editingActivity']['activity']['hour'] = hour+":"+minutes
            return
        bot.reply_to(message, "Nombre de la actividad: \""+message.json['text']+"\". Puedes /aceptar o /editar")
        for user in users:
            if user['id'] == message.from_user.id:
                user['editingActivity']['activity']['description'] = message.json['text']
        return            
    try:
        userInfo = user
    except(TypeError):
        print("Error")
        
    horario = userInfo['week'][getWeekDay(message.json['text'])]

    if getWeekDay(message.json['text']) == -1:
        horario = "No conozco ese día :("
    else:
        horario = userInfo['week'][getWeekDay(message.json['text'])]

    bot.reply_to(message, horario)

    
    


bot.infinity_polling()
