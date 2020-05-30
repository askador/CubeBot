from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import numpy as np
from aiogram.dispatcher import Dispatcher
import psycopg2
import asyncio
import random
import datetime

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
                             "(сколько) на (число(а) кубика)\n"
                             "Пример:\n"
                             " 100 на 5 | 50 2\n"
                             "20 на 1-3 | 30 5-6")
    else:
        await message.reply("Используйте эту команду в личке с ботом")


@dp.message_handler(commands=['help'])
async def help_for_player(message):
    if message.from_user.id == message.chat.id:
        await message.answer("<b>Игровые команды:</b>\n\n"
                       "<b>Кости</b> - запустить игру\n"
                       "<b>Трясти</b> - бросить кубик\n"
                       "<b>Отмена</b> - отмена ставок\n"
                       "<b>Лавэ</b> - зырнуть наличные\n"
                       "<b>Бонус</b> - забрать бонус (раз в 6 часов)"
                       "<b>Ставки</b> - зырнуть шо поставил\n"
                       "<b>логи</b> - зырнуть на историю выпадения чисел(10 значений)\n"
                       "<b>+г [сколько] (ответ на смс в чатах)</b> - передать денюжку\n"
                       "<b>!рейтинг | !рейтинг 10</b> - рейтинг игроков\n"
                       "<b>!стата</b> - личная статистика\n"
                       "<b>%п</b> - повторить ставку с прошлой игры\n"
                       "<b>%у</b> - удвоить ставки\n"
                       "\n"
                       "<b>Над ботом работали:</b>\n"
                       "<a href='tg://user?id=526497876'><b>Серый</b></a> и "
                       "<a href='tg://user?id=547400918'><b>Миша</b></a>")
    else:
        await message.reply("Используйте эту команду в личке с ботом")


@dp.message_handler(commands=['statslog'])
async def stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918 and message.text == '/statslog':
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT WON FROM STATS")
        won = cur.fetchall()[0][0]
        cur.execute("SELECT LOST FROM STATS")
        lost = cur.fetchall()[0][0]
        cur.execute("SELECT PLAYS FROM STATS")
        plays = cur.fetchall()[0][0]
        conn.close()
        await message.answer("WON: %s\nLOST: %s\nPLAYS: %s" % (won, lost, plays))
    try:
        if message.from_user.id == 526497876 and message.text.split()[1] == "сбросить":
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute("UPDATE STATS set WON = 0, LOST = 0, PLAYS = 0")
            conn.commit()
            conn.close()
            await message.answer("Сброшено")
    except Exception:
        pass


@dp.message_handler(commands=['setmoney'])
async def setmoney(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        papaid = message.from_user.id
        howmch = message.text.split()[1]
        towho = message.text.split()[2]
        try:
            if howmch.isdigit() is True and towho.isdigit() is True and howmch[0] != '+':
                if 0 <= int(howmch) < 10 ** 18:
                    conn = psycopg2.connect(
                        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
                    cur = conn.cursor()
                    cur.execute("UPDATE USERS set Money = %i WHERE UserId = %i" % (int(howmch), int(towho)))
                    conn.commit()
                    conn.close()
                    await bot.send_message(papaid, "SET completed")

                else:
                    await bot.send_message(papaid, "Не-а")

        except Exception as e:
            pass

        try:
            if howmch[0] == '+':
                if 0 < int(howmch) < 10 ** 18:
                    cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                    conn.commit()
                    await bot.send_message(papaid, "ADDed")
                    await bot.send_message(towho, "Бонус %s💰" % makegoodview(howmch[1:]))
                else:
                    await bot.send_message(papaid, "Не-а")
        except Exception as e:
            pass

        await check_limit_money(int(towho))


@dp.message_handler(commands=['advice'])
async def advice(message):
    chatid = -443076596
    await bot.send_message(chatid, "Oт @%s, %s\n%s\n-------------------------" %
                            (message.from_user.username, message.from_user.first_name, message.text))


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

    # ВЫГРУЗКА ПАРАМЕТРОВ Shake, GAME
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        #  ЗАПУСТИТЬ ИГРУ
        if Game is False:
            try:
                cur.execute("UPDATE GAME set Game = True WHERE IDChat = '%i'" % chatid)
            except Exception as e:
                await message.reply("Oops. something went wrong. Try again.")
            else:
                conn.commit()

                await start_game_message(chatid)

                # /tryasti antispam
                shakeit.update([(chatid, False)])

                # delayed start
                delayed_start_dict.update([(message.chat.id, (int(message.date.timestamp()) + 30))])
        else:
            mes3 = await message.answer('Игра уже запущена')
            cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                        (chatid, mes3.message_id))
            conn.commit()
        conn.close()


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
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = '%i'" % chatid)
        Game = cur.fetchall()[0][0]
        conn.close()
    except Exception as exc:
        Game = False

    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i" % chatid)
        user_in_bets = cur.fetchall()
        if user_in_bets and (userid,) in user_in_bets:
            cur.execute("UPDATE GAME set Shake = True WHERE IDChat = '%i'" % chatid)
    except Exception as exc:
        pass
    else:
        conn.commit()
        conn.close()

    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Shake FROM GAME WHERE IDChat = '%i'" % chatid)
        Shake = cur.fetchall()[0][0]
        conn.close()
    except Exception as exc:
        Shake = False

    # |  БРОСИТЬ КУБИКИ  |  Проверка на антиспам "Трясти"  |   Отстрочка в 30 секунд запуска в группах
    try:
        if Game is True and Shake is True and shakeit[chatid] is False:

            try:
                if int(delayed_start_dict[chatid]) - int(message.date.timestamp()) < 0 or chatid == userid:
                    shakeit.update([(chatid, True)])
                    name = message.from_user.first_name
                    await shake(name, userid, chatid)
                    shakeit.update([(chatid, False)])
                else:
                    await message.answer("Бросить можно через %s сек" %
                                         str(delayed_start_dict[chatid] - int(message.date.timestamp())))
            except Exception as e:
                shakeit.update([(chatid, True)])
                name = message.from_user.first_name
                await shake(name, userid, chatid)
                shakeit.update([(chatid, False)])

    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
        shakeit.update([(chatid, False)])

    # ЕСЛИ НЕ СДЕЛАЛ СТАВКУ
    if Game is True and Shake is False:
        await message.reply("Сначала сделай ставку")


#  Ставки игрока
@dp.message_handler(lambda message: message.text.lower() == 'ставки')
async def userbets(message):
    chatid = message.chat.id
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
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
        conn.close()


# canceling all user bets
@dp.message_handler(lambda msg: msg.text.lower() == 'отмена')
async def cancelbets(message):
    chatid = message.chat.id
    userid = message.from_user.id
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
    else:
        if Game is True:
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
                            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Bet[i][0], userid))
                            conn.commit()
                        await message.reply("<a href='tg://user?id=%i'>%s</a> отмэныл ставки" % (
                            userid, name))

                    else:
                        message.reply("Отменять нечего")
                except Exception as e:
                    await message.reply("Oops. something went wrong. Try again.")
        conn.close()


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
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Money From USERS Where UserId = '%i'" % userid)
        mon = cur.fetchall()[0][0]
        conn.close()
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
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Log FROM %s" % namedb)
        logs = cur.fetchall()
        conn.close()
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
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
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

        conn.close()


#  users stats
@dp.message_handler(text='!стата')
async def statuser(message):
    try:
        chatid = message.chat.id
        if message.text.lower() == "!стата":
            if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is False:
                userid = message.reply_to_message.from_user.id
                await user_profile(userid, chatid)

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
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute("UPDATE USERS set WON = 0, LOST = 0 WHERE UserId = %i" % userid)
            await message.answer("Стата сброшена")
            conn.commit()
            conn.close()
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


@dp.message_handler(regexp="!стата сбросить ([0-9]+)")
async def drop_smbdy_stats(message):
    try:
        if message.text.split()[2].isdigit():
            userid = message.text.split()[2]
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute("UPDATE USERS set WON = 0, LOST = 0 WHERE UserId = %i" % int(userid))
            await bot.send_message(message.chat.id, "Стата сброшена %s" % userid)
            conn.commit()
            conn.close()
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")


@dp.message_handler(text='!рейтинг')
async def top(message):
    if message.chat.id != message.from_user.id:
        try:
            rate = []
            chatid = message.chat.id
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute("SELECT UserId FROM chatusers WHERE IDChat = %i" % chatid)
            topofchat = cur.fetchall()
            topchik = ""
            q = 0
            for i in topofchat:
                cur.execute("SELECT UserId, Name, LastName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    if top[k][0] != 547400918 and top[k][0] != 526497876:
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

            conn.close()
            await message.answer(topchik)
        except Exception as e:
            message.reply("Oops, something went wrong")


@dp.message_handler(text='!рейтинг 10')
async def top(message):
    if message.chat.id != message.from_user.id:
        try:
            rate = []
            chatid = message.chat.id
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute("SELECT UserId FROM chatusers WHERE IDChat = %i" % chatid)
            topofchat = cur.fetchall()
            topchik = ""
            q = 0
            for i in topofchat:
                cur.execute("SELECT UserId, Name, LastName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    if top[k][0] != 547400918 and top[k][0] != 526497876:
                        if i[0] == top[k][0]:
                            rate.append(top[k][1:])
            ratesort = sorted(rate, key=lambda money: money[2])[::-1]

            conn.close()
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
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    if callback_query.data == '1':
        bet = 5
        num = '1'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '2':
        bet = 5
        num = '2'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '3':
        bet = 5
        num = '3'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '4':
        bet = 5
        num = '4'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '5':
        bet = 5
        num = '5'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '6':
        bet = 5
        num = '6'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '1-3':
        bet = 5
        num = '1-3'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '4-6':
        bet = 5
        num = '4-6'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '1-2':
        bet = 5
        num = '1-2'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '3-4':
        bet = 5
        num = '3-4'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    if callback_query.data == '5-6':
        bet = 5
        num = '5-6'
        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        groshi = cur.fetchall()[0][0]
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
    conn.close()


#  processing bonus callback
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить')
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить1")
    keybonus.add(bonusik)

    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % userid)
    bonususermes = cur.fetchall()[0][0]

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
    conn.close()


#  processing bonus second click step callback  --> def coef()
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить1')
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus1 = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить2")
    keybonus1.add(bonusik)

    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % userid)
    bonususermes = cur.fetchall()[0][0]

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

    conn.close()


async def coef(bonnum, userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить2')
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    keybonus2 = types.InlineKeyboardMarkup()
    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="финал")
    keybonus2.add(bonusik)

    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("SELECT Bonus_mes_id FROM USERS WHERE UserId = %i" % userid)
    bonususermes = cur.fetchall()[0][0]

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
                                             (userid, name, paluchi0, boncoef5, bonnums3[0], bonnums3[1], bonnums3[2]),
                                        reply_markup=keybonus2)

            await bot.answer_callback_query(callback_query.id)

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
    conn.close()


# профиль игрока
async def user_profile(userid, chatid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("SELECT Name, LastName, Money, Won, Lost FROM Users WHERE UserId = %i" % userid)
    usstat = cur.fetchall()
    conn.close()
    profile = ''

    if usstat[0][1] == 'None':
        Name = str(usstat[0][0])
    else:
        Name = str(usstat[0][0]) + ' ' + str(usstat[0][1])
    Lave = makegoodview(usstat[0][2])
    Won = makegoodview(str(usstat[0][3]))
    Lost = makegoodview(str(usstat[0][4]))

    profile += "<b>Имя: </b>%s\n" \
               "<b>Лавэ: </b>%s\n" \
               "<b>Выиграно: </b>%s\n" \
               "<b>Проиграно: </b>%s\n" \
               "\n" \
               "<b>Id: </b>%i" % (Name, Lave, Won, Lost, userid)
    await bot.send_message(chatid, profile)


# %п ПОВТОР СТАВОК
@dp.message_handler(text='%п')
async def repeat_bet(message):
    global shakeit
    chatid = message.chat.id
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
    else:
        #   ПРОВЕРКА НА СТАВКУ
        if Game is True:
            try:
                if shakeit[chatid] is False:
                    userid = message.from_user.id
                    name = message.from_user.first_name
                    lastname = message.from_user.last_name
                    username = message.from_user.username
                    cur.execute("SELECT Bet, Numbers FROM PREVBETS WHERE UserId = %i AND IDChat = %i" % (userid, chatid))
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
        conn.close()


# %у УДВОИТЬ ВСЕ СТАВКИ
@dp.message_handler(text='%у')
async def double_bet(message):
    chatid = message.chat.id
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
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
        conn.close()


# ПЕРЕДАТЬ ДЕНЬГИ
@dp.message_handler(regexp="(^[+][г])([' ']*)(\d)")
async def transfer_money(message):
    if 0 < int(''.join(message.text[2:].split())) < 10 ** 18 and message.reply_to_message is not None:
        name = message.from_user.first_name
        lastname = message.from_user.last_name
        username = message.from_user.username
        userid = message.from_user.id
        chatid = message.chat.id
        await alldataUSERS(name, lastname, username, userid, chatid)
        try:
            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            if message.reply_to_message.from_user.is_bot is False:
                howmuch = int(''.join(message.text[2:].split()))
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
            conn.close()


# ПРОВЕРКА НА СТАВКУ
@dp.message_handler(regexp="\d[' ']\d")
@dp.throttled(bet_trottled, rate=1.2)
async def chekbet(message: types.Message):
    global shakeit
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    #    ВЫГРУЗКА GAME
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
    else:
        #   ПРОВЕРКА НА СТАВКУ
        if Game is True:
            try:
                if shakeit[chatid] is False:
                    text = message.text
                    name = message.from_user.first_name
                    lastname = message.from_user.last_name
                    username = message.from_user.username
                    userid = message.from_user.id
                    await alldataUSERS(name, lastname, username, userid, chatid)

                    # ПРОВЕРКА НА СТАВКУ
                    # ЕСЛИ ЗАПИСЬ 100 2
                    try:
                        if len(text.split()) == 2 and (text.split()[0]).isdigit() and (text.split()[1]).isdigit() \
                                and 0 < int(text.split()[0]) < 10 ** 18 and 0 < int(text.split()[1]) <= 6:
                            bet = int(text.split()[0])
                            num = str(text.split()[-1])

                            #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                            groshi = cur.fetchall()[0][0]
                            if groshi >= bet:
                                await confirmbets(name, lastname, username, userid, chatid, num, bet)

                            else:
                                mes1 = await bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a>, нету столько" %
                                                              (userid, name))
                                cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                                            (chatid, mes1.message_id))
                                conn.commit()

                    except Exception as e:
                        pass

                    # ЕСЛИ ЗАПИСЬ 100 2 - 4
                    try:
                        if len(text.split()) == 2 and (text.split()[0]).isdigit() \
                                and 0 < int(text.split()[0]) < 10 ** 18 \
                                and (text.split()[1].split("-")[0]).isdigit() \
                                and (text.split()[1].split("-")[1]).isdigit() \
                                and 0 < (int(text.split()[1].split("-")[0])) < (
                                int(text.split()[1].split("-")[1])) <= 6:

                            bet = int(text.split()[0])
                            num = text.split()[-1]

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
        conn.close()


#  ОБРАБОТКА СТАВКИ
async def confirmbets(name, lastname, username, userid, chatid, num, bet):
    #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()


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
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                (chatid, start_mes.message_id))
    conn.commit()
    conn.close()


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
    #   ДОБАВЛЕНИЕ ЧАТА
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Count(IDChat) FROM GAME WHERE IDChat = %i" % chatid)
        IDChat = cur.fetchall()[0][0]
        if IDChat == 1:
            pass
        if IDChat < 1:
            cur.execute("INSERT INTO GAME (IDChat) VALUES (%i)" % chatid)
    except Exception as e:
        pass

    else:
        conn.commit()
        conn.close()

    #   ДОБАВЛЕНИЕ ТАБЛИЦЫ ЛОГОВ ЧАТА
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
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
        conn.close()


#  add data of user to db
async def alldataUSERS(name, lastname, username, userid, chatid):
    #   ДОБАВЛЕНИЕ ИГРОКОВ
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        cur.execute("SELECT Count(UserId) FROM USERS WHERE UserId = '%i'" % userid)
        UserdIds = cur.fetchall()[0][0]
        if UserdIds == 1:
            pass
        if UserdIds < 1:
            cur.execute("INSERT INTO USERS (Name, LastName, UserName, UserId, Money, Bonustime, "
                        "Lost, Won, Bonus_mes_id) "
                        f"VALUES ('{name}','{lastname}','{username}','{userid}', 5000, 0, 0, 0, Null)")
        if UserdIds > 1:
            cur.execute("DELETE FROM USERS WHERE Id = (SELECT MAX(ID) FROM USERS WHERE USERID = '%i')" % userid)
    except Exception as e:
        pass
    else:
        conn.commit()
        conn.close()

    #   ДЛЯ РЕЙТИНГА
    try:
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
        if userid != chatid:
            cur.execute("SELECT Count(UserId) FROM chatusers WHERE IDChat = %i AND UserID = %i" % (chatid, userid))
            UserdIds = cur.fetchall()[0][0]
            if UserdIds == 1:
                pass

            elif UserdIds < 1:
                cur.execute("INSERT INTO chatusers (IDChat, UserId) VALUES (%i, %i)" % (chatid, userid))
    except Exception as e:
        pass

    else:
        conn.commit()
        conn.close()


async def check_limit_money(userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    userid = int(userid)
    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
    money = cur.fetchall()[0][0]
    if money > 2**55:
        cur.execute("UPDATE USERS SET MONEY = %i WHERE USERID = %i" % (10**16, userid))
        conn.commit()
    conn.close()


#  start shaking  --> endgame
async def shake(name, userid, chatid):
    global startmes, shakeit

    # deleting all messages from bot in game
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("SELECT MessId FROM ToDelMes WHERE IDChat = '%i'" % chatid)
    messid = cur.fetchall()
    for i in range(len(messid)):
        try:
            await bot.delete_message(chatid, messid[i][0])
        except Exception as e:
            pass
    cur.execute("DELETE FROM todelmes where idchat = '%i'" % chatid)
    conn.commit()
    conn.close()

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
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("UPDATE GAME set Game = False WHERE IDChat = %i" % chatid)
    conn.commit()

    #   STOP SHAKE
    cur.execute("UPDATE GAME set Shake = False WHERE IDChat = %i" % chatid)
    conn.commit()

    cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
    conn.commit()
    conn.close()


async def endgame(chatid):
    mes2 = await bot.send_animation(chatid, random.choice(Gifs))

    # ВСЕ СТАВКИ
    Fstat = ''
    WINstat = ''
    ALLwins = 0
    Lose = 0

    # processing previous bets of user
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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

        #   ВСЕ СТАВКИ
        Fstat += Names + ' ' + makegoodview(str(UsBet)) + ' на ' + UsNum + '\n'


        #   ВЫИГРАЛИ
        #   1000 2-4
        try:
            if len(UsNum.split('-')) == 2:
                if int(UsNum.split('-')[0]) <=Numbers <= int(UsNum.split('-')[1]):
                    Prize = int(int(UsBet) * 6 / (int(UsNum[2]) - int(UsNum[0]) + 1))
                    ALLwins += 1

                    cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Prize, UsId))
                    cur.execute("UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (int(int(Prize) - int(UsBet)), UsId))
                    conn.commit()

                    WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                               " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

        except Exception as e:
            pass

        # 100 4
        try:
            if len(UsNum.split('-')) == 1 and int(UsNum) == Numbers:
                Prize = int(int(UsBet) * 6)
                ALLwins += 1

                cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (Prize, UsId))
                await check_limit_money(UsId)
                cur.execute("UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (int(int(Prize) - int(UsBet)), UsId))
                conn.commit()

                WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                           " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"
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
    conn.close()

    if WINstat == '':
        WINstat = 'Вах, никто нэ выиграл'

    try:
        await bot.delete_message(chatid, mes2.message_id)
    except Exception as e:
        pass

    await bot.send_message(chatid, "🎲  %s\nСтавки:\n%s \n%s" % (Numbers, Fstat, WINstat))


#  choosing number of cube
async def algoritm(chatid):
    Number = np.random.randint(1, 7, 1)[0]

    namedb = 'logchat' + str(abs(chatid))
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    cur.execute("INSERT INTO %s (Log) VALUES (%i)" % (namedb, Number))
    conn.commit()
    cur.execute("SELECT count(Id) FROM %s" % namedb)
    kaunt = cur.fetchall()
    if kaunt[0][0] > 9:
        cur.execute("DELETE FROM %s WHERE Id <= (SELECT MAX(Id) FROM %s) - 10" % (namedb, namedb))
        conn.commit()
    conn.close()


# polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
