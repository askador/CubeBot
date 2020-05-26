import telebot


token = '996503468:AAE8aR09qP8uPdF-322GSr1DTtJUmUBAhmo'
bot = telebot.TeleBot(token)




@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Временные технические шоколадки...")


@bot.message_handler(commands=['rules'])
def rules_for_player(message):
    bot.send_message(message.chat.id, "Временные технические шоколадки...")

@bot.message_handler(commands=['help'])
def help_for_player(message):
    bot.send_message(message.chat.id, "Временные технические шоколадки...")


@bot.message_handler(commands=['kosti'])
@bot.message_handler(content_types=['text'], regexp='Кости')
def start_game(message):
    global Game, Shake
    if len(message.text.split()) == 1 and ''.join(list(message.text.lower())[:5]) == "кости":
        bot.send_message(message.chat.id, "Временные технические шоколадки...")

@bot.message_handler(commands=['lave'])
@bot.message_handler(content_types=['text'], regexp='Лавэ')
def usermoney(message):
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, "Временные технические шоколадки...")


bonusmesid = {}
@bot.message_handler(commands=['bonuslave'])
@bot.message_handler(content_types=['text'], regexp='Бонус')
def bonus(message):
    global bonusmesid, lavebonus, mnozitel, numbonus, bonusdate, bonuserid, bonnums, value
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, "Временные технические шоколадки...")


@bot.message_handler(content_types=['text'], regexp='!рейтинг')
def top(message):
    pass

@bot.message_handler(content_types=['text'], regexp='!статистика')
def statuser(message):
    pass



bot.polling(none_stop=False, interval=0, timeout=100)
