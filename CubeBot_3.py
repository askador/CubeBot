from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import numpy as np
from aiogram.dispatcher import Dispatcher
import psycopg2
import asyncio
import random
import datetime
import time

from aiogram.utils.exceptions import BadRequest, ConflictError, Unauthorized, RetryAfter

bot = Bot(token='996503468:AAE8aR09qP8uPdF-322GSr1DTtJUmUBAhmo', parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

Gifs = ['CgACAgQAAxkBAAIYLV6jKaDrig_qR_Vgw_AvQgGuruadAAItAgAC5N51UOsPf1ouSS4zGQQ',
        'CgACAgQAAxkBAAIYLl6jKaIkGk1Evh4-e8Xy6wQyux-DAAJaAgACb7ntUutpUszjF0COGQQ',
        'CgACAgIAAxkBAAIYL16jKabyMhMqejWNaXKYnD9ejG6JAAJiBAACn94RSMkn7AO4qNgMGQQ',
        'CgACAgQAAxkBAAIYMF6jKahWwvj-S_jMHnNXM3M8CwABtgACFQIAAj3r_FKtfLDEEE_JGhkE',
        'CgACAgQAAxkBAAIYMV6jKarED9koopdgh5T4AQnePVOYAAORAAKHGWQH9PG0ucr3uIkZBA',
        'CgACAgQAAxkBAAIYMl6jKatmTlt7OIkjaNIwfMjH1EelAAL5AQACd2lFU1qxqx5bO0StGQQ',
        'CgACAgQAAxkBAAIYM16jKa4_6XmB4cFcyFVr6DR37ftTAALhAQACp1_0UsLTIm4ovJNYGQQ']

delayed_start_dict = {}
shakeit = {}
auto_start_dict = {}

new_gifs = {
    '1': "CAACAgIAAxkBAAJZql7ayF5WyrAbxpL-Bz_oTWKDEzjoAAIBAANUuGEfPmqAh5BwGhAaBA",
    '2': "CAACAgIAAxkBAAJZq17ayF81w4yxhLHFR3nye4OXTy-gAAICAANUuGEfK2gY72jzewEaBA",
    '3': "CAACAgIAAxkBAAJZrF7ayGAO0LUNNB4xUyPymibtpeX2AAIDAANUuGEf8iIAAdrNC94gGgQ",
    '4': "CAACAgIAAxkBAAJZrV7ayGFgfMOHrMWs79Zbv_xpgWacAAIEAANUuGEfKVMcA499XU0aBA",
    '5': "CAACAgIAAxkBAAJZrl7ayGJeNsu2OxFgSClBaw4DnSK2AAIFAANUuGEf0QqpjTqu_T8aBA",
    '6': "CAACAgIAAxkBAAJZr17ayGPsMtBIfrD6meVqB9TywgqOAAIGAANUuGEf7T2hVkEE40waBA"
}
bonus_gif = 'CAACAgIAAxkBAAJZsF7ayGQo1aCENzBjuSqMjH-LIrhZAAIHAANUuGEf5o6jSM3m8uIaBA'
while_choosing = 'CAACAgIAAxkBAAJZsV7ayGXpk_acwimP5EuoReTilPGIAAIIAANUuGEf-V_Xn2Xia24aBA'

conn = psycopg2.connect(
    "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
    "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
cur = conn.cursor()


@dp.message_handler(commands=['start'])
async def start_message(message):
    userid = message.from_user.id
    chatid = message.chat.id
    if chatid == userid:
        startkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtna = types.KeyboardButton('Кости')
        trasti = types.KeyboardButton('Трясти')
        startkb.add(itembtna, trasti)
        await bot.send_message(message.chat.id, "Добро пожаловать, в Cube Bot!\n"
                                                "Испытай удачу, бросив кубик 🎲\n"
                                                "Делай ставочки, угадывай числа\n"
                                                "Выигрывай лавэ💰\n"
                                                "\n"
                                                "Основные функции:\n"
                                                "/help - команды бота\n"
                                                "/rules - правила игры\n"
                                                "/kosti - начать игру\n"
                                                "/tryasti - бросить кубик\n"
                                                "/lave - просмотреть баланс\n"
                                                "/bonuslave - бонус\n"
                                                "/advice [текст] - предложение для доработок", reply_markup=startkb)
    else:
        await bot.send_message(message.chat.id, "Добро пожаловать, в Cube Bot!\n"
                                                "Испытай удачу, бросив кубик 🎲\n"
                                                "Делай ставочки, угадывай числа\n"
                                                "Выигрывай лавэ💰\n"
                                                "\n"
                                                "Основные функции:\n"
                                                "/help - команды бота\n"
                                                "/rules - правила игры\n"
                                                "/kosti - начать игру\n"
                                                "/trasti - бросить кубик\n"
                                                "/lave - просмотреть баланс\n"
                                                "/bonuslave - бонус\n"
                                                "/advice [текст] - предложение для доработок")


@dp.message_handler(commands=['rules'])
async def rules_for_player(message):
    if message.from_user.id == message.chat.id:
        await message.answer("Угадай число от 1 до 6🎲\n\n"
                             "Последовательность:\n"
                             "• отправьте сообщение Кости или нажмите на кнопку 'Кости' для запуска игры\n"
                             "• сделайте ставку\n"
                             "• отправьте сообщение Трясти или нажмите на кнопку 'Трясти' для броска кубика\n"
                             "\n"
                             "Ставки имеют вид:\n"
                             "(сколько) (число(а) кубика)\n"
                             "Пример:\n"
                             " 30 5-6 | 50 2")
    else:
        await message.reply("Используйте эту команду в личке с ботом")


@dp.message_handler(commands=['help'])
async def help_for_player(message):
    if message.from_user.id == message.chat.id:
        await message.answer("<b>Игровые команды:</b>\n\n"
                             "<b>Кости</b> - запустить игру\n\n"
                             "<b>Трясти</b> - бросить кубик\n\n"
                             "<b>Отмена</b> - отмена ставок\n\n"
                             "<b>Лавэ</b> - зырнуть наличные\n\n"
                             "<b>Бонус</b> - забрать бонус (раз в 2 часа)\n\n"
                             "<b>Ставки</b> - зырнуть шо поставил\n\n"
                             "<b>логи</b> - зырнуть на историю выпадения чисел(10 значений)\n\n"
                             "<b>+г [сколько] (ответ на смс в чатах)</b> - передать денюжку\n\n"
                             "<b>!рейтинг | !рейтинг 10</b> - рейтинг игроков\n\n"
                             "<b>!стата</b> - личная статистика\n\n"
                             "<b>!раздача [сколько]</b> - раздача лавэ (раз в час, не меньше 100 000"
                             " и не больше 10 000 000 000)\n\n"
                             "<b>%п</b> - повторить ставку с прошлой игры\n\n"
                             "<b>%у</b> - удвоить ставки\n\n"
                             "\n"
                             "<b>Автор идеи: </b><a href='tg://user?id=547400918'><b>Миша</b></a>\n"
                             "<b>Создатель: </b><a href='tg://user?id=526497876'><b>Серый</b></a>")
    else:
        await message.reply("Используйте эту команду в личке с ботом")


@dp.message_handler(regexp="!достижение ([0-9]+)")
async def achieve(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        userid = int(message.text.split()[1])
        achieve = str(' '.join(message.text.split()[2:]))

        try:
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES (%i, '%s')" % (userid, achieve))
        except Exception as e:
            await message.reply("Не удалось добавить")
        else:
            conn.commit()
            await message.answer(f"Achievement {achieve} was added to {userid}")
            cur.execute("SELECT Name, LastName FROM Users WHERE UserID = %i" % userid)
            name = cur.fetchall()
            if name[0][1] != "None":
                name = name[0][0] + ' ' + name[0][1]
            else:
                name = name[0][0]
            await bot.send_message(userid, "Сириус стал ярче")
            await asyncio.sleep(2)
            await bot.send_message(userid, "Кукушка услышала пение")
            await asyncio.sleep(2)
            await bot.send_message(userid, f"{name} получает достижение\n"
            f"<b>{achieve}</b>")


@dp.message_handler(regexp="!у достижение ([0-9]+)")
async def achieve(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:

        try:
            userid = int(message.text.split()[2])
            achieve = str(' '.join(message.text.split()[3:]))
        except Exception:
            await message.reply("Not correct!\n!у достижение id achievement")
        else:
            cur.execute("SELECT Achieve FROM ACHIVES WHERE UserId = %i AND Achieve = '%s'" % (userid, achieve))
            can_del = cur.fetchall()
            if can_del:
                cur.execute("DELETE FROM ACHIVES WHERE Achieve = '%s' AND UserId = %i" % (achieve, userid))
                conn.commit()
                await message.answer(f"Achievement {achieve} was removed from {userid}")
            else:
                await message.answer("Проверьте правильность ID и названия достижения")


@dp.message_handler(regexp="!скрыть стату")
async def hide_stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        try:
            whoid = int(message.text.split()[2])
        except Exception:
            await message.reply("Not correct input\n!скрыть стату ID")
        else:
            try:
                cur.execute("UPDATE Users set Show_stat = False WHERE UserId = %i" % whoid)
            except Exception as e:
                await message.reply("Not correct Id")
            else:
                conn.commit()
                #  Achevement Неуловимый
                await message.reply("Стата %i скрыта" % whoid)

                cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES (%i, 'Неуловимый')" % whoid)

                conn.commit()
                await message.answer(f"Achievement Неуловимый was added to {whoid}")
                cur.execute("SELECT Name, LastName FROM Users WHERE UserID = %i" % whoid)
                name = cur.fetchall()
                if name[0][1] != "None":
                    name = name[0][0] + ' ' + name[0][1]
                else:
                    name = name[0][0]
                await bot.send_message(whoid, "Сириус стал ярче")
                await asyncio.sleep(2)
                await bot.send_message(whoid, "Кукушка услышала пение")
                await asyncio.sleep(2)
                await bot.send_message(whoid, f"{name} получает достижение\n<b>Неуловимый</b>")


@dp.message_handler(regexp="!открыть стату")
async def hide_stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        try:
            whoid = int(message.text.split()[2])
        except Exception:
            await message.reply("Not correct input\n!открыть стату ID")
        else:
            try:

                cur.execute("UPDATE Users set Show_stat = True WHERE UserId = %i" % whoid)
            except Exception as e:
                await message.reply("Not correct Id")
            else:
                conn.commit()

                await message.reply("Стата %i открыта" % whoid)


@dp.message_handler(lambda msg: msg.reply_to_message is not None and msg.text == "getid")
async def s(message):
    try:
        await message.reply(message.reply_to_message.from_user.id)
    except Exception:
        pass


@dp.message_handler(commands=['statslog'])
async def stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918 and message.text == '/statslog':
        cur.execute("SELECT WON FROM STATS")
        won = cur.fetchall()[0][0]
        cur.execute("SELECT LOST FROM STATS")
        lost = cur.fetchall()[0][0]
        cur.execute("SELECT PLAYS FROM STATS")
        plays = cur.fetchall()[0][0]
        await message.answer("WON: %s\nLOST: %s\nPLAYS: %s" % (won, lost, plays))
    try:
        if message.from_user.id == 526497876 and message.text.split()[1] == "сбросить":
            cur.execute("UPDATE STATS set WON = 0, LOST = 0, PLAYS = 0")
            conn.commit()
            await message.answer("Сброшено")
    except Exception:
        pass


@dp.message_handler(commands=['setmoney'])
async def setmoney(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        papaid = message.from_user.id
        howmch = (''.join((message.text.split()[1]).split(',')))
        towho = message.text.split()[2]
        try:
            if howmch.isdigit() is True and towho.isdigit() is True and howmch[0] != '+':
                if 0 <= int(howmch) < 10 ** 18:
                    cur.execute("UPDATE USERS set Money = %i WHERE UserId = %i" % (int(howmch), int(towho)))
                    conn.commit()
                    await bot.send_message(papaid, "SET completed")

                else:
                    await bot.send_message(papaid, "Не-а")

        except Exception as e:
            pass

        try:
            if howmch[0] == '+':
                if 0 < int(howmch) < 10 ** 18:
                    if len(message.text.split()) >= 4:
                        note = ' '.join(message.text.split()[3:])
                        cur.execute(
                            "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                        conn.commit()
                        await bot.send_message(papaid, "ADDed")
                        await bot.send_message(towho, "Бонус %s💰\n%s" % (makegoodview(howmch[1:]), note))

                    else:
                        if 0 < int(howmch) < 10 ** 18:
                            cur.execute(
                                "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                            conn.commit()
                            await bot.send_message(papaid, "ADDed")
                            await bot.send_message(towho, "Бонус %s💰" % makegoodview(howmch[1:]))
                else:
                    await bot.send_message(papaid, "Не-а")
        except Exception as e:
            pass

        await check_limit_money(int(towho))


async def anti_spam_advice(message, *args, **kwargs):
    await message.reply("Не спамь")


@dp.message_handler(commands=['advice'])
@dp.throttled(anti_spam_advice, rate=10)
async def advice(message):
    chatid = -443076596
    if message.chat.type == 'private':
        if len(message.text.split()) != 1:
            await bot.send_message(chatid, "Oт @%s, %s\n\n%s" %
                                   (message.from_user.username, message.from_user.full_name, message.text))

            await message.reply("Принято")
        else:
            await message.answer("Совет не может быть пустым")
    else:
        await message.reply("Используйте эту команду в личке с ботом")


#  |  ЗАПУСК ИГРЫ  |
@dp.message_handler(commands=['kosti'])
@dp.message_handler(lambda message: message.text.lower() == 'кости')
async def start_game(message):
    global shakeit
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    userid = message.from_user.id
    chatid = int(message.chat.id)

    await alldataCHAT(chatid)
    await alldataUSERS(name, lastname, username, userid, chatid)

    #  ЗАПУСТИТЬ ИГРУ
    try:
        cur.execute("SELECT Game FROM Game WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()
    except Exception:
        await message.reply("Oops, something went wrong")
    else:
        if Game:
            mes3 = await message.reply("Игра уже запущена")
            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                        (chatid, mes3.message_id))
            conn.commit()
        elif not Game:
            try:
                if shakeit[chatid] is True:
                    mes3 = await message.reply("Игра уже запущена")
                    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                (chatid, mes3.message_id))
            except Exception:
                shakeit.update([(chatid, False)])
                await message.reply("Oops, something went wrong. Try again")
            else:
                conn.commit()
                if shakeit[chatid] is False:
                    cur.execute("INSERT INTO Game (Game, Shake, IDChat, Time) VALUES (True, False, %i, %i)" %
                                (chatid, int(message.date.timestamp())))
                    conn.commit()

                    await start_game_message(chatid)

                    # /tryasti antispam
                    shakeit.update([(chatid, False)])

                    # delayed start
                    delayed_start_dict.update([(message.chat.id, (int(message.date.timestamp()) + 20))])

                    # autostart
                    loop_autostrt = asyncio.get_event_loop()
                    await loop_autostrt.create_task(autostart(chatid))


#  БРОСИТЬ КУБИКИ
@dp.message_handler(commands=['tryasti'])
@dp.message_handler(lambda message: message.text.lower() == 'трясти')
@dp.message_handler(lambda message: message.text.lower() == 'го')
async def shake_game(message):
    global shakeit, auto_start_dict
    chatid = message.chat.id
    userid = message.from_user.id

    #   ВЫГРУЗКА ПАРАМЕТРА GAME
    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = '%i'" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as exc:
        Game = False

    try:
        cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i" % chatid)
        user_in_bets = cur.fetchall()
        if user_in_bets and (userid,) in user_in_bets:
            cur.execute("UPDATE GAME set Shake = True WHERE IDChat = '%i'" % chatid)
    except Exception as exc:
        pass
    else:
        conn.commit()

    try:
        cur.execute("SELECT Shake FROM GAME WHERE IDChat = '%i'" % chatid)
        Shake = cur.fetchall()[0][0]
    except Exception as exc:
        Shake = False

    # |  БРОСИТЬ КУБИКИ  |  Проверка на антиспам "Трясти"  |   Отстрочка в 30 секунд запуска в группах
    try:
        if Game is True and Shake is True and shakeit[chatid] is False:

            try:
                if int(delayed_start_dict[chatid]) - int(message.date.timestamp()) < 0 or chatid == userid:
                    cur.execute("DELETE FROM GAME WHERE IDChat = %i" % chatid)
                    conn.commit()
                    shakeit.update([(chatid, True)])
                    name = message.from_user.first_name
                    await shake(name, userid, chatid)
                    shakeit.update([(chatid, False)])
                else:
                    await message.answer("Бросить можно через %s сек" %
                                         str(delayed_start_dict[chatid] - int(message.date.timestamp())))
            except Exception as e:
                cur.execute("DELETE FROM GAME WHERE IDChat = %i" % chatid)
                conn.commit()
                shakeit.update([(chatid, True)])
                name = message.from_user.first_name
                await shake(name, userid, chatid)
                shakeit.update([(chatid, False)])

        # ЕСЛИ НЕ СДЕЛАЛ СТАВКУ
        if Game is True and Shake is False:
            await message.reply("Сначала сделай ставку")
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
        shakeit.update([(chatid, False)])


#  Ставки игрока
@dp.message_handler(lambda message: message.text.lower() == 'ставки')
async def userbets(message):
    chatid = message.chat.id

    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        if Game is True:
            userid = message.from_user.id
            chatid = message.chat.id

            cur.execute("SELECT Bet FROM BETS WHERE UserId = %i AND IDChat = %i AND Bet != 0" % (userid, chatid))
            allbets = cur.fetchall()

            cur.execute("SELECT Name FROM USERS WHERE UserId = %i" % userid)
            Name = str(cur.fetchall()[0][0])
            Stavki = ''

            try:
                if allbets:
                    cur.execute("SELECT Numbers FROM BETS WHERE UserId = %i AND IDChat = %i AND Bet != 0" %
                                (userid, chatid))
                    allnums = cur.fetchall()
                    for i in range(len(allbets)):
                        bets = str(allbets[i][0])
                        nums = str(allnums[i][0])
                        if nums[0] == "с":
                            Stavki += makegoodview(bets) + ' грыв на сумму ' + nums[1:] + '\n'
                        else:
                            Stavki += makegoodview(bets) + ' грыв на ' + nums + '\n'
                    await message.answer("Ставочки %s:\n%s" % (Name, Stavki))
                else:
                    await message.answer("%s, нэма ставок" % Name)
            except Exception as e:
                await message.reply("Oops. something went wrong. Try again.")


# canceling all user bets
@dp.message_handler(lambda msg: msg.text.lower() == 'отмена')
async def cancelbets(message):
    global shakeit
    chatid = message.chat.id
    userid = message.from_user.id

    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        if Game is True:
            try:
                if shakeit[chatid] is False:
                    cur.execute("SELECT count(Bet) FROM BETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
                    useringame = cur.fetchall()[0][0]
                    if useringame > 0:
                        name = message.from_user.first_name
                        chatid = message.chat.id
                        cur.execute("SELECT Bet FROM BETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
                        Bet = cur.fetchall()
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
                        Num = cur.fetchall()
                        try:
                            if Bet != [] and Num != []:
                                cur.execute("DELETE FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (userid, chatid))
                                for i in range(len(Bet)):
                                    cur.execute(
                                        "UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Bet[i][0], userid))
                                    conn.commit()
                                cancel = await message.reply("<a href='tg://user?id=%i'>%s</a> отмэныл ставки" % (
                                    userid, name))
                                cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                            (chatid, cancel.message_id))
                            else:
                                message.reply("Отменять нечего")
                        except Exception as e:
                            await message.reply("Oops. something went wrong. Try again.")
            except Exception:
                await message.reply("Oops. something went wrong. Try again.")
                shakeit.update([(chatid, False)])


#  БАЛАНС ИГРОКА
@dp.message_handler(commands=['lave'])
@dp.message_handler(lambda message: message.text.lower() == 'лавэ')
async def usermoney(message):
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    userid = message.from_user.id
    chatid = message.chat.id
    await alldataUSERS(name, lastname, username, userid, chatid)
    try:
        cur.execute("SELECT Money From USERS Where UserId = '%i'" % userid)
        mon = cur.fetchall()[0][0]
        await message.reply("%s грывень" % makegoodview(mon))
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


# all chat logs
@dp.message_handler(lambda msg: msg.text.lower() == 'логи')
async def logsgame(message):
    chatid = message.chat.id
    await alldataCHAT(chatid)

    LOG = ''
    namedb = 'logchat' + str(abs(chatid))
    try:
        cur.execute("SELECT Log FROM %s" % namedb)
        logs = cur.fetchall()
        for i in range(len(logs)):
            LOG += "🎲  %s\n" % logs[i][0]
        if LOG != '':
            await message.answer(LOG)
        else:
            await message.answer("Лог пустой")
    except Exception as e:
        await message.reply("Oops, something went wrong")


@dp.message_handler(commands=['bonuslave'])
@dp.message_handler(lambda message: message.text.lower() == 'бонус')
async def bonus(message):
    chatid = message.chat.id
    name = message.from_user.first_name
    bonuserid = message.from_user.id
    username = message.from_user.username
    lastname = message.from_user.last_name
    await alldataUSERS(name, lastname, username, bonuserid, chatid)

    try:
        cur.execute("SELECT BONUSTIME FROM USERS WHERE UserId = %s" % bonuserid)
        bonustime = int(cur.fetchall()[0][0])
    except Exception:
        await message.reply("Oops, something went wrong")
    else:
        ostalos = bonustime - message.date.timestamp()

        if bonuserid != 526497876 and bonuserid != 547400918 and ostalos > 0:
            value = datetime.datetime.fromtimestamp(ostalos).strftime('%H:%M:%S')
            await message.reply("Бонусное лавэ можно получить через %s" % value)

        elif bonuserid == 526497876 or bonuserid == 547400918 or bonustime == 0 or ostalos <= 0:
            keybonus = types.InlineKeyboardMarkup()
            bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить")
            keybonus.add(bonusik)

            lavebonus = int(random.randrange(400, 800))

            numbonus = ''.join([str(np.random.randint(1, 7, 1)[0]) for i in range(3)])

            cur.execute("DELETE FROM BONUS WHERE USERID = %s" % bonuserid)
            conn.commit()

            cur.execute(
                "INSERT INTO BONUS (UserId, BONCOEF, BONNUMS, LAVE, START_LAVE) VALUES (%i, 1, %s, %i, %i)"
                % (bonuserid, numbonus, lavebonus, lavebonus))
            conn.commit()

            bonusmes = await message.answer("<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                            "Лавэ %i, коеффициент = 1.0\n\n"
                                            "           🎲 : 🎲 : 🎲 \n" % (bonuserid, name, lavebonus),
                                            reply_markup=keybonus)

            punkt = int(message.date.timestamp()) + 7200
            cur.execute("UPDATE USERS set BONUSTIME = %i, Bonus_mes_id = '%i' WHERE UserId = %i" %
                        (punkt, bonusmes.message_id, bonuserid))
            conn.commit()

            loop_bonus = asyncio.get_event_loop()
            await loop_bonus.create_task(start_bonus(name, bonuserid, chatid))


async def start_bonus(name, userid, chatid):
    await asyncio.sleep(300)

    try:
        cur.execute("SELECT Lave FROM Bonus WHERE UserId = %i" % userid)
        lave = cur.fetchall()
        if lave:
            cur.execute("SELECT Bonus_mes_id FROM USERS WHERE UserId = %i" % userid)
            id_of_mes = cur.fetchall()[0][0]
            try:
                await bot.edit_message_text(chat_id=chatid, message_id=id_of_mes,
                                            text="<a href='tg://user?id=%i'>%s</a> забирает свой бонус %s " %
                                                 (userid, name, lave[0][0]))

                cur.execute("DELETE FROM BONUS WHERE UserId = %i" % userid)
                conn.commit()
            except Exception:
                pass
            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (lave[0][0], userid))
            conn.commit()
    except Exception:
        pass


#  users stats
@dp.message_handler(text='!стата')
async def statuser(message):
    try:
        chatid = message.chat.id
        if message.text.lower() == "!стата":
            if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is False:
                userid = message.reply_to_message.from_user.id

                cur.execute("SELECT Show_stat FROM Users WHERE UserId = %i" % userid)
                Show_stat = cur.fetchall()[0][0]

                if Show_stat is True or message.from_user.id == 526497876 or message.from_user.id == 547400918:
                    await user_profile(userid, chatid)

                else:
                    await message.reply("На такое лучше не смотреть")

            else:
                userid = message.from_user.id
                await user_profile(userid, chatid)

    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


@dp.message_handler(text='!стата сбросить')
async def drop_stats(message):
    try:
        if message.text.lower().split()[0] == '!стата' and message.text.lower().split()[1] == "сбросить":
            userid = message.from_user.id
            cur.execute("UPDATE USERS set WON = 0, LOST = 0, Plays = 0 WHERE UserId = %i" % userid)
            await message.answer("Стата сброшена")
            conn.commit()
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


# профиль игрока
async def user_profile(userid, chatid):
    cur.execute("SELECT Name, LastName, Money, Won, Lost, plays FROM Users WHERE UserId = %i" % userid)
    usstat = cur.fetchall()
    cur.execute("SELECT Achieve FROM Achives WHERE UserId = %i" % userid)
    achives = cur.fetchall()

    ach = ''
    profile = ''

    try:
        for i in range(len(achives)):
            ach += '\n' + str(achives[i][0])
    except Exception as e:
        pass

    if usstat[0][1] == 'None':
        Name = str(usstat[0][0])
    else:
        Name = str(usstat[0][0]) + ' ' + str(usstat[0][1])
    Lave = makegoodview(usstat[0][2])
    Won = makegoodview(str(usstat[0][3]))
    Lost = makegoodview(str(usstat[0][4]))
    Plays = usstat[0][5]

    profile += "<b>Имя: </b>%s\n" \
               "<b>Лавэ: </b>%s\n" \
               "<b>Выиграно: </b>%s\n" \
               "<b>Проиграно: </b>%s\n" \
               "<b>Игр сыграно: </b>%s\n" \
               "<b>Достижения: </b>%s\n" \
               "\n" \
               "<b>Id: </b>%i" % (Name, Lave, Won, Lost, Plays, ach, userid)
    await bot.send_message(chatid, profile)


@dp.message_handler(regexp="!стата сбросить ([0-9]+)")
async def drop_smbdy_stats(message):
    try:
        if message.text.split()[2].isdigit():
            userid = message.text.split()[2]
            cur.execute("UPDATE USERS set WON = 0, LOST = 0, Plays = 0 WHERE UserId = %i" % int(userid))
            await bot.send_message(message.chat.id, "Стата сброшена %s" % userid)
            conn.commit()
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


@dp.message_handler(text='!рейтинг')
async def top(message):
    if message.chat.id != message.from_user.id:

        try:
            rate = []
            chatid = message.chat.id
            cur.execute("SELECT UserId FROM chatusers WHERE IDChat = %i" % chatid)
            topofchat = cur.fetchall()
            topchik = ""
            q = 0
            for i in topofchat:
                cur.execute("SELECT UserId, Name, LastName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    # if top[k][0] != 547400918 and top[k][0] != 526497876:
                    if i[0] == top[k][0]:
                        rate.append(top[k][1:])
            ratesort = sorted(rate, key=lambda money: money[2])[::-1]

            if len(ratesort) <= 30:
                for i in range(len(ratesort)):
                    q += 1
                    if ratesort[i][1] == 'None':
                        topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + makegoodview(ratesort[i][2]) + '\n'
                    else:
                        topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + str(ratesort[i][1]) + ' ' + \
                                   makegoodview(ratesort[i][2]) + '\n'
            else:
                for i in range(30):
                    q += 1
                    if ratesort[i][1] == 'None':
                        topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + makegoodview(ratesort[i][2]) + '\n'
                    else:
                        topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + str(ratesort[i][1]) + ' ' + \
                                   makegoodview(ratesort[i][2]) + '\n'

            await message.answer(topchik)
        except Exception as e:
            await message.reply("Oops, something went wrong")


@dp.message_handler(text='!рейтинг 10')
async def top(message):
    if message.chat.id != message.from_user.id:

        try:
            rate = []
            chatid = message.chat.id
            cur.execute("SELECT UserId FROM chatusers WHERE IDChat = %i" % chatid)
            topofchat = cur.fetchall()
            topchik = ""
            q = 0
            for i in topofchat:
                cur.execute("SELECT UserId, Name, LastName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    # if top[k][0] != 547400918 and top[k][0] != 526497876:
                    if i[0] == top[k][0]:
                        rate.append(top[k][1:])
            ratesort = sorted(rate, key=lambda money: money[2])[::-1]

            for i in range(10):
                q += 1
                if ratesort[i][1] == 'None':
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + makegoodview(ratesort[i][2]) + '\n'
                else:
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + str(ratesort[i][1]) + ' ' + \
                               makegoodview(ratesort[i][2]) + '\n'

            await message.answer(topchik)
        except Exception as e:
            message.reply("Oops, something went wrong")


async def giveaway_timer(give_mes_id, userid, chatid):
    start_in = 300

    cur.execute(f"SELECT FullName FROM GIVEAWAY%s WHERE UserId = %s" % (abs(chatid), userid))
    starter = str(cur.fetchall()[0][0])

    cur.execute(f"SELECT How_many From GIVEAWAY{abs(chatid)} WHERE UserId = {userid}")
    how_many_proc = int(cur.fetchall()[0][0])

    while start_in > 0:
        await asyncio.sleep(3)
        start_in -= 3
        try:

            cur.execute(f"SELECT FullName, Value FROM GIVEAWAY{abs(chatid)}"
                        f" WHERE Value IS NOT NULL ORDER BY VALUE DESC")
            giveaway_data = cur.fetchall()

            list_for_giveaway = ''

            for i in range(len(giveaway_data)):
                FullName = str(giveaway_data[i][0])
                Value = str(giveaway_data[i][1])
                list_for_giveaway += FullName + ' ' + Value + '🏅\n'

            giveaway_bt_procc = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='+ 1🏅', callback_data="раздача")
            giveaway_bt_procc.add(button)

            await bot.edit_message_text(chat_id=chatid, message_id=give_mes_id, text=
            f"<a href='tg://user?id={userid}'>{starter}</a> "
            f"устраивает раздачу лавэ {makegoodview(how_many_proc)}\n"
            f"Правила:\n"
            f"Нажимайте на кнопку, набирайте больше всех очков\n"
            f"Награда распределится по количеству набранных очков\n"
            f"Раздача лавэ через {datetime.datetime.fromtimestamp(start_in).strftime('%M:%S')}"
            f"\n\n"
            f"{list_for_giveaway}",
                                        reply_markup=giveaway_bt_procc)
        except Exception:
            pass
    else:
        pass
        await bot.delete_message(chatid, give_mes_id)

        await asyncio.sleep(2)

        cur.execute(f"SELECT FullName, Value, UserId FROM GIVEAWAY{abs(chatid)} WHERE Value > 0 ORDER BY Value DESC")
        final = cur.fetchall()
        if final:
            final_list = ''
            all_values = 0

            for i in range(len(final)):
                all_values += int(final[i][1])

            for j in range(len(final)):
                users_score = int(final[j][1])
                fullname = str(final[j][0])

                money = int(int(how_many_proc / all_values) * users_score)

                final_list += "<a href='tg://user?id=%i'>%s</a>" % (final[j][2], fullname) + ' получил ' + \
                              str(makegoodview(money)) + '\n'

                cur.execute(f"UPDATE USERS SET Money = Money + {money} WHERE UserId = {final[j][2]}")
                conn.commit()

            await bot.send_message(chatid, f"Итоги раздачи от <a href='tg://user?id={userid}'>{starter}</a>:\n"
            "\n" + final_list)

            cur.execute(f"DROP TABLE GIVEAWAY{abs(chatid)}")
            conn.commit()
        else:
            cur.execute(f"UPDATE USERS Set Money = Money + {how_many_proc} WHERE UserId = {userid}")
            await bot.send_message(chatid, "Раздача не состоялась, некому раздавать лавэ")
            cur.execute(f"DROP TABLE GIVEAWAY{abs(chatid)}")
            conn.commit()


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'раздача')
@dp.throttled(rate=1.3)
async def scores(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.full_name
    name1 = callback_query.from_user.first_name
    lastname = callback_query.from_user.last_name
    username = callback_query.from_user.username

    try:
        cur.execute(f"SELECT UserId FROM GIVEAWAY{abs(chatid)} WHERE How_many IS NOT NULL")
        not_for_him = cur.fetchall()[0][0]
        if userid != not_for_him:
            await alldataUSERS(name1, lastname, username, userid, chatid)
            cur.execute(f"SELECT count(Value) FROM GIVEAWAY{abs(chatid)} WHERE UserId = {userid}")
            to_count = int(cur.fetchall()[0][0])
            if to_count == 1:
                cur.execute(f"UPDATE GIVEAWAY{abs(chatid)} set Value = Value + 1 WHERE UserId = {userid}")
                conn.commit()
            elif to_count < 1:
                cur.execute(f"INSERT INTO GIVEAWAY{abs(chatid)} (FullName, UserId, Value)"
                            f" VALUES ('{name}', {userid}, 1)")
                conn.commit()
            await bot.answer_callback_query(callback_query.id)
        else:
            await bot.answer_callback_query(callback_query.id, "Ты организатор")
    except Exception:
        pass


@dp.message_handler(regexp='!раздача ([0-9]+)')
async def giveaway(message):
    userid = message.from_user.id
    chatid = message.chat.id
    if userid != chatid:
        if int(message.text.split()[1]) >= 100000:

            cur.execute(f"SELECT Giveaway_time FROM Users WHERE UserId = {userid}")
            time_for_giveaway = int(cur.fetchall()[0][0])

            if int(message.date.timestamp()) > time_for_giveaway or time_for_giveaway == 0:
                if int(message.text.split()[1]) <= 10 ** 10:
                    name = str(message.from_user.full_name)
                    how_many = int(message.text.split()[1])

                    try:

                        cur.execute(f"CREATE TABLE GIVEAWAY{abs(chatid)}("
                                    "Id Serial,"
                                    "UserId              BIGINT,"
                                    "How_many            BIGINT,"
                                    "FullName              TEXT,"
                                    "value                  INT,"
                                    "PRIMARY KEY(Id));")
                    except Exception as e:

                        await message.reply("Раздача лавэ уже начата")
                    else:
                        conn.commit()

                        cur.execute(f"INSERT INTO GIVEAWAY{abs(chatid)} (UserId, How_many, FullName)"
                                    f" Values ('{userid}', '{how_many}', '%s')" % name)
                        conn.commit()

                        cur.execute(f"UPDATE USERS SET Giveaway_time = '{int(message.date.timestamp()) + 3600}', "
                                    f"Money = Money - {how_many} "
                                    f"WHERE UserId = {userid}")
                        conn.commit()

                        giveaway_bt = types.InlineKeyboardMarkup()
                        button = types.InlineKeyboardButton(text='+ 1🏅', callback_data="раздача")
                        giveaway_bt.add(button)

                        giveaway_mes = await message.answer(f"<a href='tg://user?id={userid}'>{name}</a> "
                                                            f"устраивает раздачу лавэ {makegoodview(how_many)}\n"
                                                            f"Правила:\n"
                                                            f"Нажимайте на кнопку, набирайте больше всех очков\n"
                                                            f"Награда распределится по количеству набранных очков\n"
                                                            f"Раздача лавэ через 5:00",
                                                            reply_markup=giveaway_bt)

                        Loop = asyncio.get_event_loop()
                        await Loop.create_task(giveaway_timer(giveaway_mes.message_id, userid, chatid))

                else:
                    await message.reply("Раздать можно не больше 10 миллиардов")
            else:
                await message.reply("Устраивать раздачу можно раз в 1 час")
        else:
            await message.reply("Минимальная сумма для раздачи 100 000")
    else:
        await message.reply("Устраивайте раздачу лавэ в группах")


async def trottled(callback_query, *args, **kwargs):
    await bot.answer_callback_query(callback_query.id, "Не торопись")


async def bet_trottled(message, *args, **kwargs):
    await message.reply("Не торопись")


# processing callback
@dp.callback_query_handler(lambda call: call.data == '1' or call.data == '2' or call.data == '3' or call.data == '3'
                                        or call.data == '4' or call.data == '5' or call.data == '6'
                                        or call.data == '1-3' or call.data == '4-6' or call.data == '1-2'
                                        or call.data == '3-4' or call.data == '5-6')
@dp.throttled(trottled, rate=1.2)
async def process_callback_game_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    lastname = callback_query.from_user.last_name
    username = callback_query.from_user.username

    bet = 5
    num = str(callback_query.data)
    #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
    try:
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
    except Exception:
        await bot.answer_callback_query(callback_query.id)
    else:
        if groshi >= bet:
            await confirmbets(name, lastname, username, userid, chatid, num, bet)
            await bot.answer_callback_query(callback_query.id)

        else:
            mes1 = await callback_query.message.answer(
                "<a href='tg://user?id=%i'>%s</a>, нету столько" % (userid, name))
            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                        (chatid, mes1.message_id))
            conn.commit()
            await bot.answer_callback_query(callback_query.id)


#  processing bonus callback
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить')
@dp.throttled(rate=1)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить1")
    keybonus.add(bonusik)

    try:
        cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % userid)
        bonususermes = cur.fetchall()[0][0]
    except Exception:
        pass
    else:
        if bonususermes == mesid:
            cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
            paluchi = cur.fetchall()[0][0]

            cur.execute("SELECT bonnums from bonus where userid = %i" % userid)
            bonnums = cur.fetchall()[0][0]

            try:
                await bot.edit_message_text(chat_id=chatid, message_id=bonususermes,
                                            text="<a href='tg://user?id=%s'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                                 "Лавэ %s, коеффициент = %.1f\n\n"
                                                 "             <b>%s</b> : 🎲 : 🎲 \n" %
                                                 (userid, name, paluchi, 1, bonnums[0]), reply_markup=keybonus)
                await bot.answer_callback_query(callback_query.id)
            except Exception as e:
                pass
        else:
            await callback_query.answer("Не твоё")


#  processing bonus second click step callback  --> def coef()
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить1')
@dp.throttled(rate=1)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus1 = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить2")
    keybonus1.add(bonusik)

    try:
        cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % userid)
        bonususermes = cur.fetchall()[0][0]
    except Exception:
        pass
    else:
        if bonususermes == mesid:
            cur.execute("SELECT bonnums from bonus where userid = %i" % userid)
            bonnums2 = cur.fetchall()[0][0]

            try:
                if bonnums2[0] == bonnums2[1]:
                    await coef(bonnums2[0], userid)

                cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi3 = cur.fetchall()[0][0]

                cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % userid)
                boncoef = cur.fetchall()[0][0]

                await bot.edit_message_text(chat_id=chatid, message_id=bonususermes,
                                            text="<a href='tg://user?id=%s'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                                 "Лавэ %s, коеффициент = %.1f\n\n"
                                                 "               <b>%s</b> : <b>%s</b> : 🎲 \n" %
                                                 (userid, name, paluchi3, boncoef, bonnums2[0], bonnums2[1]),
                                            reply_markup=keybonus1)
                await bot.answer_callback_query(callback_query.id)
            except Exception:
                pass

        else:
            await callback_query.answer("Не твоё")


async def coef(bonnum, userid):
    if bonnum == '1':
        mnozitel = 1.5
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()
    if bonnum == '2':
        mnozitel = 2.3
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()
    if bonnum == '3':
        mnozitel = 3.1
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()
    if bonnum == '4':
        mnozitel = 3.9
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()
    if bonnum == '5':
        mnozitel = 4.7
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()
    if bonnum == '6':
        mnozitel = 5.5
        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
        paluchi5 = cur.fetchall()[0][0]
        paluchi5 = paluchi5 * mnozitel
        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
        conn.commit()


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить2')
@dp.throttled(rate=1)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus2 = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="финал")
    keybonus2.add(bonusik)

    try:
        cur.execute("SELECT Bonus_mes_id FROM USERS WHERE UserId = %i" % userid)
        bonususermes = cur.fetchall()[0][0]
    except Exception:
        pass
    else:
        if bonususermes == mesid:

            cur.execute("SELECT bonnums from bonus where userid = %i" % userid)
            bonnums3 = cur.fetchall()[0][0]

            try:
                if bonnums3[0] == bonnums3[2] or bonnums3[1] == bonnums3[2] and len(list(set(bonnums3))) != 1:
                    await coef(bonnums3[2], userid)

                if len(list(set(bonnums3))) == 1:
                    if bonnums3[0] == '1':
                        mnozitel2 = 25
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()
                    elif bonnums3[0] == '2':
                        mnozitel2 = 28
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()
                    elif bonnums3[0] == '3':
                        mnozitel2 = 33
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()
                    elif bonnums3[0] == '4':
                        mnozitel2 = 38
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()
                    elif bonnums3[0] == '5':
                        mnozitel2 = 45
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()
                    elif bonnums3[0] == '6':
                        mnozitel2 = 50
                        cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                        cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                        paluchi5 = cur.fetchall()[0][0]
                        paluchi5 = paluchi5 * mnozitel2
                        cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                        conn.commit()

                cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi0 = cur.fetchall()[0][0]

                cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (paluchi0, userid))
                conn.commit()
                await check_limit_money(userid)

                cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % userid)
                boncoef5 = cur.fetchall()[0][0]

                await bot.edit_message_text(chat_id=chatid, message_id=bonususermes,
                                            text="<a href='tg://user?id=%s'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                                 "Лавэ %s, коеффициент = %.1f\n\n"
                                                 "               <b>%s</b> : <b>%s</b> : <b>%s</b> \n" %
                                                 (userid, name, paluchi0, boncoef5, bonnums3[0], bonnums3[1],
                                                  bonnums3[2]),
                                            reply_markup=keybonus2)

                await bot.answer_callback_query(callback_query.id)

                try:
                    bonus_achievement = await achieves_bonus(bonnums3, userid)
                    for i in range(len(bonus_achievement)):
                        gift = bonus_achievement[i][1]
                        title = bonus_achievement[i][0]
                        await bot.send_message(chatid, f"⭐️ {name} получает достижение "
                        f"\n<b>{title}</b>\n"
                        f"Держи награду +{gift}")
                except Exception as e:
                    pass

                await asyncio.sleep(2)
                await bot.edit_message_text(chat_id=chatid, message_id=bonususermes,
                                            text="<a href='tg://user?id=%i'>%s</a> забирает свой бонус %s " %
                                                 (userid, name, paluchi0))

                cur.execute("DELETE FROM BONUS WHERE UserId = %i" % userid)
                conn.commit()
            except Exception:
                pass

        else:
            await callback_query.answer("Не твоё")


# %п ПОВТОР СТАВОК
@dp.message_handler(text='%п')
async def repeat_bet(message):
    global shakeit
    chatid = message.chat.id

    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        #   ПРОВЕРКА НА СТАВКУ
        if Game is True:
            try:
                if shakeit[chatid] is False:
                    userid = message.from_user.id
                    name = message.from_user.first_name
                    lastname = message.from_user.last_name
                    username = message.from_user.username
                    cur.execute(
                        "SELECT Bet, Numbers FROM PREVBETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
                    prev = cur.fetchall()
                    if prev:
                        PrevBets = ''
                        a = []
                        b = []
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                            userid, chatid))
                        UsNum = cur.fetchall()
                        for i in range(len(prev)):
                            Bet = prev[i][0]
                            if len(str(prev[i][1])) == 2:
                                Num = str(list(prev[i][1])[0]) + '-' + str(list(prev[i][1])[1])
                            else:
                                Num = str(prev[i][1])
                            a.append(Num)
                            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                            groshi1 = cur.fetchall()[0][0]
                            if groshi1 >= int(Bet):
                                if (Num,) in UsNum:
                                    PrevBets += str(makegoodview(Bet)) + ' ' + 'на' + ' ' + str(Num) + '\n'
                                    b.append(Num)

                                    cur.execute(
                                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                        "AND Numbers = '%s'" % (Bet, userid, chatid, Num))
                                    conn.commit()

                                    cur.execute(
                                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                        "WHERE UserId = '%i'" % (name, lastname, username, Bet, userid))
                                    conn.commit()

                                else:
                                    PrevBets += str(makegoodview(Bet)) + ' ' + 'на' + ' ' + str(Num) + '\n'
                                    b.append(Num)
                                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, Bet, Num, chatid))

                                    cur.execute(
                                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                        "WHERE UserId = '%i'" % (name, lastname, username, Bet, userid))
                                    conn.commit()

                        if a == b:
                            bet_mes = await message.answer("%s повтор с прошлой игры:\n%s" % (name, PrevBets))
                            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                        (chatid, bet_mes.message_id))
                        else:
                            bet_mes = await message.answer("%s недостаточно денег\nНекоторые ставки не прошли\n%s" % (
                                name, PrevBets))
                            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                        (chatid, bet_mes.message_id))
            except Exception:
                await message.reply("Oops. something went wrong. Try again.")
                shakeit.update([(chatid, False)])


# %у УДВОИТЬ ВСЕ СТАВКИ
@dp.message_handler(text='%у')
async def double_bet(message):
    chatid = message.chat.id

    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        if Game is True:
            try:
                if shakeit[chatid] is False:
                    userid = message.from_user.id
                    name = message.from_user.first_name
                    lastname = message.from_user.last_name
                    username = message.from_user.username

                    cur.execute("SELECT Bet, Numbers FROM BETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
                    doub = cur.fetchall()
                    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                    groshi1 = cur.fetchall()[0][0]

                    a1 = []
                    b1 = []
                    double = ''

                    if doub:
                        for i in range(len(doub)):
                            Bet1 = doub[i][0]
                            Num1 = doub[i][1]
                            b1.append(Bet1)
                            if groshi1 >= int(Bet1) * 2:
                                a1.append(Bet1)
                                double += str(makegoodview(int(Bet1) * 2)) + ' ' + 'на' + ' ' + str(Num1) + '\n'
                                cur.execute(
                                    "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                                    "WHERE UserId = '%i'" % (name, lastname, username, Bet1, userid))

                                cur.execute(
                                    "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                    "AND Numbers = '%s'" % (Bet1, userid, chatid, Num1))
                                conn.commit()

                        if b1 == a1:
                            _mes = await bot.send_message(chatid, "%s удвоил все ставки\n%s" % (name, double))
                            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                        (chatid, _mes.message_id))
                        else:
                            _mes = await bot.send_message(chatid, "%s не хватает денег на некоторые ставки" % name)
                            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                        (chatid, _mes.message_id))
            except Exception as e:
                await message.reply("Oops. something went wrong. Try again.")
                shakeit.update([(chatid, False)])


# ПЕРЕДАТЬ ДЕНЬГИ
@dp.message_handler(regexp="(^[+][г])([' ']*)(\d)")
async def transfer_money(message):
    try:
        if 0 < int(''.join(message.text[2:].split(','))) < 10 ** 18 and message.reply_to_message is not None:
            name = message.from_user.first_name
            lastname = message.from_user.last_name
            username = message.from_user.username
            userid = message.from_user.id
            chatid = message.chat.id
            await alldataUSERS(name, lastname, username, userid, chatid)
            try:

                if message.reply_to_message.from_user.is_bot is False:
                    howmuch = int(''.join(message.text[2:].split(',')))
                    whoid = message.reply_to_message.from_user.id
                    whoname = message.reply_to_message.from_user.first_name
                    wholastname = message.reply_to_message.from_user.last_name
                    whousername = message.reply_to_message.from_user.username
                    if userid != whoid:
                        await alldataUSERS(whoname, wholastname, whousername, whoid, chatid)
                        cur.execute("SELECT Money FROM USERS WHERE UserId = %i" % userid)
                        balance = int(cur.fetchall()[0][0])
                        if howmuch <= balance:
                            cur.execute(
                                "UPDATE USERS set Money = Money - %i WHERE UserId = %i" % (howmuch, userid))
                            cur.execute(
                                "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (howmuch, whoid))
                            await bot.send_message(chatid,
                                                   "<a href='tg://user?id=%i'>%s</a> передал "
                                                   "<a href='tg://user?id=%i'>%s</a> "
                                                   "%s грывень" % (userid, name, whoid, whoname, makegoodview(howmuch)))

                        else:
                            await bot.send_message(chatid, "Нету столько", reply_to_message_id=message.message_id)

                    await check_limit_money(whoid)
            except Exception as e:
                await message.reply("Oops. something went wrong. Try again.")
            else:
                conn.commit()

    except Exception:
        pass


# ПРОВЕРКА НА СТАВКУ
@dp.message_handler(regexp="(\d[' ']\d)$")
@dp.message_handler(regexp="(\d[ ]\d[-]\d)$")
@dp.throttled(bet_trottled, rate=1.2)
async def chekbet(message: types.Message):
    global shakeit
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Ставки не принимаются")
    else:
        #   ПРОВЕРКА НА СТАВКУ
        text = message.text
        if len(text.split()) == 2:
            if Game is True:
                try:
                    if shakeit[chatid] is False:
                        name = message.from_user.first_name
                        lastname = message.from_user.last_name
                        username = message.from_user.username
                        userid = message.from_user.id
                        await alldataUSERS(name, lastname, username, userid, chatid)

                        # ЕСЛИ ЗАПИСЬ 100 2
                        try:
                            if (''.join((text.split()[0]).split(','))).isdigit() and (text.split()[1]).isdigit() \
                                    and 0 < int((''.join((text.split()[0]).split(','))).isdigit()) < 10 ** 18 \
                                    and 0 < int(text.split()[1]) <= 6:
                                bet = int(''.join((text.split()[0]).split(',')))
                                num = str(text.split()[-1])

                                #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                                cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                                groshi = cur.fetchall()[0][0]
                                if groshi >= bet:
                                    await confirmbets(name, lastname, username, userid, chatid, num, bet)

                                else:
                                    mes1 = await bot.send_message(chatid,
                                                                  "<a href='tg://user?id=%i'>%s</a>, нету столько" %
                                                                  (userid, name))
                                    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                                (chatid, mes1.message_id))
                                    conn.commit()

                        except Exception as e:
                            pass

                        # ЕСЛИ ЗАПИСЬ 100 2 - 4
                        try:
                            if (''.join((text.split()[0]).split(','))).isdigit() \
                                    and 0 < int((''.join((text.split()[0]).split(','))).isdigit()) < 10 ** 18 \
                                    and (text.split()[1].split("-")[0]).isdigit() \
                                    and (text.split()[1].split("-")[1]).isdigit() \
                                    and 0 < (int(text.split()[1].split("-")[0])) < (
                                    int(text.split()[1].split("-")[1])) <= 6:

                                bet = int(''.join((text.split()[0]).split(',')))
                                num = str(text.split()[-1])

                                #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                                cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                                groshi = cur.fetchall()[0][0]
                                if groshi >= bet:
                                    await confirmbets(name, lastname, username, userid, chatid, num, bet)

                                else:
                                    mes1 = await message.answer(
                                        "<a href='tg://user?id=%i'>%s</a>, нету столько" % (userid, name))
                                    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                                (chatid, mes1.message_id))
                                    conn.commit()

                        except Exception as e:
                            pass

                except Exception as e:
                    await message.reply("Oops. something went wrong. Try again.")
                    shakeit.update([(chatid, False)])


#  ОБРАБОТКА СТАВКИ
async def confirmbets(name, lastname, username, userid, chatid, num, bet):
    #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
    cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
        userid, chatid))
    UsNum = cur.fetchall()
    if (num,) in UsNum:
        #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
        cur.execute("SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" %
                    (userid, num, chatid))
        UsBet = int(cur.fetchall()[0][0])

        bet_mes = await bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на "
                                         "%s" % (userid, name, makegoodview(UsBet + bet), num))

        cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                    (chatid, bet_mes.message_id))

        cur.execute(
            "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
            "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))

        cur.execute(
            "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
            "AND Numbers = '%s'" % (bet, userid, chatid, num))
        conn.commit()
    else:
        bet_mes = await bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на "
                                         "%s" % (userid, name, makegoodview(bet), num))

        cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                    (chatid, bet_mes.message_id))

        cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                    "VALUES ('%i', '%i', '%s', '%i')" % (userid, bet, num, chatid))

        cur.execute(
            "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
            "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))
        conn.commit()


#  НАЧАЛЬНОЕ СООБЩЕНИЕ
async def start_game_message(chatid):
    game_kb = types.InlineKeyboardMarkup(row_width=3)
    n1 = types.InlineKeyboardButton(text='5 на 1', callback_data="1")
    n2 = types.InlineKeyboardButton(text='5 на 2', callback_data="2")
    n3 = types.InlineKeyboardButton(text='5 на 3', callback_data="3")
    game_kb.row(n1, n2, n3)

    n4 = types.InlineKeyboardButton(text='5 на 4', callback_data="4")
    n5 = types.InlineKeyboardButton(text='5 на 5', callback_data="5")
    n6 = types.InlineKeyboardButton(text='5 на 6', callback_data="6")
    game_kb.row(n4, n5, n6)

    t13 = types.InlineKeyboardButton(text='5 на 1-3', callback_data="1-3")
    t46 = types.InlineKeyboardButton(text='5 на 4-6', callback_data="4-6")
    game_kb.add(t13, t46)

    t12 = types.InlineKeyboardButton(text='5 на 1-2', callback_data="1-2")
    t34 = types.InlineKeyboardButton(text='5 на 3-4', callback_data="3-4")
    t56 = types.InlineKeyboardButton(text='5 на 5-6', callback_data="5-6")

    game_kb.row(t12, t34, t56)

    start_mes = await bot.send_message(chatid, "🧖🏽‍♂️Бросаем кубики нэ стесняемся🎲\n"
                                               "Угадай число от 1 до 6\n"
                                               "Делай ставки не скупи💰\n"
                                               "\n"
                                               "<i>%п</i> - повтор, <i>%у</i> - удвоить\n"
                                               "<i>ставки</i> - ваши ставки\n", reply_markup=game_kb)
    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                (chatid, start_mes.message_id))
    conn.commit()


async def autostart(chatid):
    global shakeit
    await asyncio.sleep(300)
    cur.execute("SELECT Game, Time FROM GAME WHERE IDChat = %i" % chatid)
    data = cur.fetchall()
    if data:
        Game = data[0][0]
        Time = int(data[0][1])

        if 300 <= int(time.time()) - Time <= 308 and Game is True:
            shakeit.update([(chatid, True)])
            #   STOP GAME
            cur.execute("DELETE FROM GAME WHERE IDChat = %i" % chatid)
            conn.commit()

            cur.execute("SELECT MessId FROM ToDelMes WHERE IDChat = '%i'" % chatid)
            messid = cur.fetchall()
            for i in range(len(messid)):
                try:
                    await bot.delete_message(chatid, messid[i][0])
                except Exception as e:
                    pass
            cur.execute("DELETE FROM todelmes where idchat = '%i'" % chatid)
            conn.commit()

            await algoritm(chatid)
            await endgame(chatid)

            cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
            conn.commit()
            shakeit.update([(chatid, False)])


#  make good bet/balance view
def makegoodview(how):
    how = str(how)
    how = list(how)
    q = 0
    for i in range(1, len(how) + 1):
        if -i % 3 == 0:
            how.insert(-(i + q), ',')
            q += 1
    if how[0] == ',':
        del how[0]
    how = ''.join(how)
    return how


#  add data of chat to db
async def alldataCHAT(chatid):
    #   ДОБАВЛЕНИЕ ТАБЛИЦЫ ЛОГОВ ЧАТА
    try:
        namedb = 'logchat' + str(abs(chatid))
        cur.execute("CREATE TABLE if not exists %s"
                    "(Id     Serial,"
                    "Log     VARCHAR(20)  NOT NULL,"
                    "PRIMARY KEY(Id));" % namedb)
    except Exception as e:
        pass
        await asyncio.sleep(1)
    else:
        conn.commit()


#  add data of user to db
async def alldataUSERS(name, lastname, username, userid, chatid):
    #   ДОБАВЛЕНИЕ ИГРОКОВ
    try:
        cur.execute("SELECT Count(UserId) FROM USERS WHERE UserId = '%i'" % userid)
        UserdIds = cur.fetchall()[0][0]
        if UserdIds == 1:
            pass
        if UserdIds < 1:
            cur.execute("INSERT INTO USERS (Name, LastName, UserName, UserId, Money, Bonustime, "
                        "Lost, Won, Bonus_mes_id, Giveaway_time) "
                        f"VALUES ('{name}','{lastname}','{username}','{userid}', 5000, 0, 0, 0, Null, 0)")
        if UserdIds > 1:
            cur.execute("DELETE FROM USERS WHERE Id = (SELECT MAX(ID) FROM USERS WHERE USERID = '%i')" % userid)
    except Exception as e:
        pass
    else:
        conn.commit()

    #   ДЛЯ РЕЙТИНГА
    try:
        if userid != chatid:
            cur.execute("SELECT Count(UserId) FROM chatusers WHERE IDChat = %i AND UserID = %i" % (chatid, userid))
            UserdIds = cur.fetchall()[0][0]
            if UserdIds < 1:
                cur.execute("INSERT INTO chatusers (IDChat, UserId) VALUES (%i, %i)" % (chatid, userid))
    except Exception as e:
        pass

    else:
        conn.commit()


async def check_limit_money(userid):
    userid = int(userid)
    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
    money = cur.fetchall()[0][0]
    if money > 2 ** 55:
        cur.execute("UPDATE USERS SET MONEY = %i WHERE USERID = %i" % (10 ** 16, userid))
        conn.commit()


async def achievs_balance(userid):
    cur.execute("SELECT Money From Users WHERE UserId = %i" % userid)
    money = int(cur.fetchall()[0][0])
    mess = []
    if money >= 10 ** 6:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Попрошайка'" % userid)
        onem = cur.fetchall()
        if not onem:
            mess.append(["Попрошайка", "500 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Попрошайка')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 500000 WHERE UserId = %i" % userid)
            conn.commit()
    if money >= 100 * (10 ** 6):
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Кассир'" % userid)
        onem = cur.fetchall()
        if not onem:
            mess.append(["Кассир", "25 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Кассир')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 25000000 WHERE UserId = %i" % userid)
            conn.commit()
    if money >= 500 * (10 ** 6):
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Коллектор'" % userid)
        fvhundrm = cur.fetchall()
        if not fvhundrm:
            mess.append(["Коллектор", "125 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Коллектор')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 125000000 WHERE UserId = %i" % userid)
            conn.commit()
    if money >= 10 ** 9:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Магнат'" % userid)
        oneb = cur.fetchall()
        if not oneb:
            mess.append(["Магнат", "250 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Магнат')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 250000000 WHERE UserId = %i" % userid)
            conn.commit()
    if money >= 10 ** 12:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Буржуй'" % userid)
        onet = cur.fetchall()
        if not onet:
            mess.append(["Буржуй", "1 000 000 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Буржуй')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def achieves_plays(userid):
    cur.execute("SELECT Plays From Users WHERE UserId = %i" % userid)
    plays = int(cur.fetchall()[0][0])
    mess = []
    if plays >= 25:
        "исследователь"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Исследователь'" % userid)
        find = cur.fetchall()
        if not find:
            mess.append(['Исследователь', "50 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Исследователь')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 50000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 50:
        "ПРОВИ́ЗОР"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Провизор'" % userid)
        dresir = cur.fetchall()
        if not dresir:
            mess.append(['Провизор', "250 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Провизор')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 250000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 100:
        "любитель"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Любитель'" % userid)
        lover = cur.fetchall()
        if not lover:
            mess.append(['Любитель', "400 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Любитель')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 400000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 200:
        "Одержимый"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Одержимый'" % userid)
        zadr = cur.fetchall()
        if not zadr:
            mess.append(['Одержимый', "1 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Одержимый')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 500:
        "профи"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Профи'" % userid)
        pro = cur.fetchall()
        if not pro:
            mess.append(['Профи', "5 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Профи')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 5000000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 1000:
        "Иллюминат👁"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Иллюминат👁'" % userid)
        mad = cur.fetchall()
        if not mad:
            mess.append(['Иллюминат👁', "1 000 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Иллюминат👁')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 2000:
        "Хранитель 🔮"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Хранитель 🔮'" % userid)
        chran = cur.fetchall()
        if not chran:
            mess.append(['Хранитель 🔮', "1 000 000 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Хранитель 🔮')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def achieves_bonus(bonnums, userid):
    mess = []
    if len(set(bonnums)) == 1 and bonnums[0] != '6':
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Везунчик'" % userid)
        lucker = cur.fetchall()
        if not lucker:
            mess.append(["Везунчик", "250 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Везунчик')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 250000 WHERE UserId = %i" % userid)
            conn.commit()

    if len(set(bonnums)) == 1 and bonnums[0] == '6':
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Адский покровитель🔥'" % userid)
        hell = cur.fetchall()
        if not hell:
            mess.append(['Адский покровитель🔥', "666 666"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Адский покровитель🔥')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 666666 WHERE UserId = %i" % userid)
            conn.commit()

        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Везунчик'" % userid)
        lucker = cur.fetchall()
        if not lucker:
            mess.append(["Везунчик", "250 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Везунчик')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 250000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def max_win(userid, prize):
    # "Волк с Уолл-стрит"
    mess = []
    if prize >= 10 ** 12:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Волк с Уолл-стрит'" % userid)
        maxwin = cur.fetchall()
        if not maxwin:
            mess = ['Волк с Уолл-стрит', "500 000 000 000", userid]
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Волк с Уолл-стрит')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 500000000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


#  start shaking  --> endgame
async def shake(name, userid, chatid):
    # deleting all messages from bot in game
    cur.execute("SELECT MessId FROM ToDelMes WHERE IDChat = '%i'" % chatid)
    messid = cur.fetchall()

    for i in range(len(messid)):
        try:
            await bot.delete_message(chatid, messid[i][0])
        except Exception as e:
            pass
    cur.execute("DELETE FROM todelmes where idchat = '%i'" % chatid)
    conn.commit()

    mes1 = await bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a> бросает кубик" % (userid, name))

    # -------------------------------
    # animation and processing all bets
    await asyncio.sleep(5)

    #   РАНДОМНОЕ ЧИСЛО
    await algoritm(chatid)

    try:
        await bot.delete_message(chatid, mes1.message_id)
    except Exception as e:
        pass

    #   ВЫГРУЗКА ВСЕХ СТАВОК
    await endgame(chatid)

    # -------------------------------

    #   STOP GAME

    cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
    conn.commit()


async def endgame(chatid):
    list_of_plays = []
    list_of_names = {}
    Wonmaxnum = []

    # ВСЕ СТАВКИ
    Fstat = ''
    WINstat = ''
    ALLwins = 0
    Lose = 0

    # processing previous bets of user
    cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i AND Bet > 0" % chatid)
    Usids = cur.fetchall()
    for ids in Usids:
        cur.execute("DELETE FROM PREVBETS WHERE UserId = %i AND IDChat = %i" % (ids[0], chatid))
        conn.commit()

    #  numbers
    namedb = 'logchat' + str(abs(chatid))
    cur.execute("SELECT Log From %s WHERE Id = (Select max(id) from %s)" % (namedb, namedb))
    Numbers = int(cur.fetchall()[0][0])

    # processing all bets
    cur.execute("SELECT Id FROM BETS WHERE IDChat = %i AND Bet > 0" % chatid)
    IDs = cur.fetchall()
    for uid in IDs:
        cur.execute("SELECT UserId, Bet, Numbers FROM BETS WHERE Id = %i" % uid)
        ALLBets = cur.fetchall()

        UsId = ALLBets[0][0]
        UsBet = str(ALLBets[0][1])
        UsNum = str(ALLBets[0][2])
        try:
            if len(UsNum) == 3:
                UsNum1 = str(UsNum.split('-')[0] + UsNum.split('-')[1])
                cur.execute("INSERT INTO PREVBETS (UserId, Bet, Numbers, IDChat) VALUES (%i, %s, %s, %i)" %
                            (UsId, UsBet, UsNum1, chatid))
            elif len(UsNum) == 1:
                cur.execute("INSERT INTO PREVBETS (UserId, Bet, Numbers, IDChat) VALUES (%i, %s, %s, %i)" %
                            (UsId, UsBet, UsNum, chatid))
        except Exception as e:
            pass
        else:
            conn.commit()

        cur.execute("SELECT Name FROM USERS WHERE UserId = %i" % UsId)
        Names = str(cur.fetchall()[0][0])

        #  Для статистики
        list_of_plays.append(UsId)
        list_of_names.update([(UsId, Names)])

        #   ВСЕ СТАВКИ
        Fstat += Names + ' ' + makegoodview(str(UsBet)) + ' на ' + UsNum + '\n'

        # ВЫИГРАЛИ  1000 2-4
        try:
            if len(UsNum.split('-')) == 2:
                if int(UsNum.split('-')[0]) <= Numbers <= int(UsNum.split('-')[1]):
                    Prize = int(int(UsBet) * 6 / (int(UsNum[2]) - int(UsNum[0]) + 1))
                    ALLwins += 1

                    cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Prize, UsId))
                    cur.execute(
                        "UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (int(int(Prize) - int(UsBet)), UsId))
                    conn.commit()

                    WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                               " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

                    Wonmaxnum.append(await max_win(UsId, Prize))

        except Exception as e:
            pass

        # 100 4
        try:
            if len(UsNum.split('-')) == 1 and int(UsNum) == Numbers:
                Prize = int(int(UsBet) * 6)
                ALLwins += 1

                cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (Prize, UsId))
                await check_limit_money(UsId)
                cur.execute(
                    "UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (int(int(Prize) - int(UsBet)), UsId))
                conn.commit()

                WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                           " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

                Wonmaxnum.append(await max_win(UsId, Prize))
        except Exception as e:
            pass

        # WARNING!!!  BE CAREFUL
        await check_limit_money(UsId)

        #   LOST
        try:
            if int(UsNum) != Numbers:
                Lose += 1
                cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                conn.commit()
        except Exception as e:
            pass
        try:
            if int(UsNum.split('-')[1]) < Numbers or Numbers < int(UsNum.split('-')[0]):
                Lose += 1
                cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                conn.commit()
        except Exception as e:
            pass

    # UPDATE STATSLOG
    cur.execute("UPDATE STATS set WON = WON + %i, LOST = LOST + %i, PLAYS = PLAYS + 1 WHERE Id = 1" % (ALLwins, Lose))
    conn.commit()

    # update plays stats
    list_of_plays = list(set(list_of_plays))
    for i in range(len(list_of_plays)):
        cur.execute("UPDATE USERS set Plays = Plays + 1 WHERE UserId = %i" % list_of_plays[i])
        conn.commit()
        try:
            plays = await achieves_plays(list_of_plays[i])
            for k in range(len(plays)):
                title = plays[k][0]
                moni = plays[k][1]
                await bot.send_message(chatid, f"⭐️ {list_of_names[list_of_plays[i]]} получает достижение "
                f"\n<b>{title}</b>\n"
                f"Держи награду +{moni}")

            end = await achievs_balance(list_of_plays[i])
            for j in range(len(end)):
                gift = end[j][1]
                which = end[j][0]
                await bot.send_message(chatid, f"⭐️ {list_of_names[list_of_plays[i]]} получает достижение "
                f"\n<b>{which}</b>\n"
                f"Держи награду +{gift}")

        except Exception as e:
            pass

    try:
        for h in range(len(Wonmaxnum)):
            titleV = Wonmaxnum[h][0]
            moniV = Wonmaxnum[h][1]
            useridV = Wonmaxnum[h][2]
            await bot.send_message(chatid, f"⭐️ {list_of_names[useridV]} получает достижение "
            f"\n<b>{titleV}</b>\n"
            f"Держи награду +{moniV}")
    except Exception:
        pass

    if WINstat == '':
        WINstat = 'Вах, никто нэ выиграл'

    if str(chatid)[:4] == '-100':
        await bot.send_animation(chatid, new_gifs[str(Numbers)])
        await asyncio.sleep(3)

        await bot.send_message(chatid, "🎲  %s\nСтавки:\n%s \n%s" % (Numbers, Fstat, WINstat))
    else:
        await bot.send_message(chatid, "🎲  %s\nСтавки:\n%s \n%s" % (Numbers, Fstat, WINstat))


#  choosing number of cube
async def algoritm(chatid):
    Number = np.random.randint(1, 7, 1)[0]

    namedb = 'logchat' + str(abs(chatid))
    cur.execute("INSERT INTO %s (Log) VALUES (%i)" % (namedb, Number))
    conn.commit()
    cur.execute("SELECT count(Id) FROM %s" % namedb)
    kaunt = cur.fetchall()
    if kaunt[0][0] > 9:
        cur.execute("DELETE FROM %s WHERE Id <= (SELECT MAX(Id) FROM %s) - 10" % (namedb, namedb))
        conn.commit()


@dp.errors_handler(exception=Unauthorized)
@dp.errors_handler(exception=BadRequest)
@dp.errors_handler(exception=ConflictError)
@dp.errors_handler(exception=RetryAfter)
async def error_handler(update, e):
    print(e)
    return True


# polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
