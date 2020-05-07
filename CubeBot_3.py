import telebot
from telebot import types
import random
import psycopg2
import time
from datetime import datetime
import numpy as np
import sys

token = '996503468:AAFA1AHH7rlHJ_u0YXBJuKYCbxoXfMPrEdY'
bot = telebot.TeleBot(token)

conn = psycopg2.connect("postgres://widffjyseacqgd:9e0aba3ec9eff3396d1f1c12998e638343e7d1666f17995b2d77e31e6a55c99d"
                        "@ec2-18-232-143-90.compute-1.amazonaws.com:5432/d5v7nd5uqgpo2b")

conn.set_client_encoding("UTF8")
cur = conn.cursor()


Money = 0
cf = 0.16666666666666666666666666666667
Nums = [1, 2, 3, 4, 5, 6]
sys.setrecursionlimit(10 ** 2)

Gifs = ['CgACAgQAAxkBAAIYLV6jKaDrig_qR_Vgw_AvQgGuruadAAItAgAC5N51UOsPf1ouSS4zGQQ',
        'CgACAgQAAxkBAAIYLl6jKaIkGk1Evh4-e8Xy6wQyux-DAAJaAgACb7ntUutpUszjF0COGQQ',
        'CgACAgIAAxkBAAIYL16jKabyMhMqejWNaXKYnD9ejG6JAAJiBAACn94RSMkn7AO4qNgMGQQ',
        'CgACAgQAAxkBAAIYMF6jKahWwvj-S_jMHnNXM3M8CwABtgACFQIAAj3r_FKtfLDEEE_JGhkE',
        'CgACAgQAAxkBAAIYMV6jKarED9koopdgh5T4AQnePVOYAAORAAKHGWQH9PG0ucr3uIkZBA',
        'CgACAgQAAxkBAAIYMl6jKatmTlt7OIkjaNIwfMjH1EelAAL5AQACd2lFU1qxqx5bO0StGQQ',
        'CgACAgQAAxkBAAIYM16jKa4_6XmB4cFcyFVr6DR37ftTAALhAQACp1_0UsLTIm4ovJNYGQQ']


@bot.message_handler(commands=['start'])
def start_message(message):
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    userid = message.from_user.id
    chatid = message.chat.id
    alldataCHAT(chatid)
    alldataUSERS(name, lastname, username, userid, chatid)
    if chatid == userid:
        markup = types.ReplyKeyboardMarkup(True)
        itembtna = types.KeyboardButton('Кости')
        trasti = types.KeyboardButton('Трясти')
        markup.row(itembtna, trasti)

        bot.send_message(message.chat.id, "Добро пожаловать, в Cube Bot!\n"
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
                                          "/bonuslave - бонус", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Добро пожаловать, в Cube Bot!\n"
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
                                          "/bonuslave - бонус")


@bot.message_handler(commands=['rules'])
def rules_for_player(message):
    if message.from_user.id == message.chat.id:
        bot.send_message(message.chat.id, "Угадай число от 1 до 6🎲\n\n"
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
        bot.send_message(message.chat.id, "Используйте эту команду в личке с ботом",
                         reply_to_message_id=message.message_id)


@bot.message_handler(commands=['help'])
def help_for_player(message):
    if message.from_user.id == message.chat.id:
        bot.send_message(message.chat.id, "<b>Игровые команды:</b>\n\n"
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
                                          "\n"
                                          "<b>Над ботом работали:</b>\n"
                                          "<a href='tg://user?id=526497876'><b>Серый</b></a> и "
                                          "<a href='tg://user?id=547400918'><b>Миша</b></a>",
                         parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Используйте эту команду в личке с ботом",
                         reply_to_message_id=message.message_id)


#
#   FOR ME
@bot.message_handler(commands=['statslog'])
def stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918 and message.text == '/statslog':
        cur.execute("SELECT WON FROM STATS")
        won = cur.fetchall()[0][0]
        cur.execute("SELECT LOST FROM STATS")
        lost = cur.fetchall()[0][0]
        cur.execute("SELECT PLAYS FROM STATS")
        plays = cur.fetchall()[0][0]
        bot.send_message(message.chat.id, "WON: %s\nLOST: %s\nPLAYS: %s" % (won, lost, plays))
    try:
        if message.from_user.id == 526497876 and message.text.split()[1] == "сбросить":
            cur.execute("UPDATE STATS set WON = 0, LOST = 0, PLAYS = 0")
            conn.commit()
            bot.send_message(message.chat.id, "Сброшено")
    except Exception:
        pass


@bot.message_handler(commands=['setmoney'])
def setmoney(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        papaid = message.from_user.id
        howmch = message.text.split()[1]
        towho = message.text.split()[2]
        try:
            if isinstance(int(howmch), int) is True and isinstance(int(towho), int) is True and howmch[0] != '+' \
                    and howmch[0] != '-':
                cur.execute("UPDATE USERS set Money = %i WHERE UserId = %i" % (int(howmch), int(towho)))
                conn.commit()
                bot.send_message(papaid, "SET completed")

            elif howmch[0] == '+':
                cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                conn.commit()
                bot.send_message(papaid, "ADDed")
                bot.send_message(towho, "Бонус %s💰" % makegoodview(howmch[1:]))
        except Exception:
            pass


#
#

@bot.message_handler(commands=['kosti'])
@bot.message_handler(content_types=['text'], regexp='Кости')
def start_game(message):
    global Game, Shake
    if len(message.text.split()) == 1 and message.text.lower() == "кости" or message.text[:6] == '/kosti':
        name = message.from_user.first_name
        lastname = message.from_user.last_name
        username = message.from_user.username
        userid = message.from_user.id
        chatid = message.chat.id

        alldataCHAT(chatid)
        alldataUSERS(name, lastname, username, userid, chatid)


        #   ВЫГРУЗКА ПАРАМЕТРА Shake
        #   ВЫГРУЗКА ПАРАМЕТРА GAME
        try:
            #   ВЫГРУЗКА ПАРАМЕТРА Shake
            cur.execute("SELECT Shake FROM GAME WHERE IDChat = '%i'" % chatid)
            Shake = cur.fetchall()[0][0]
            #   ВЫГРУЗКА ПАРАМЕТРА GAME
            cur.execute("SELECT Game FROM GAME WHERE IDChat = '%i'" % chatid)
            Game = cur.fetchall()[0][0]
        except Exception:
            time.sleep(3)

        #       ПРОВЕРКА НА СПАМ    |||||    ELSE  ЗАПУСТИТЬ ИГРУ
        if Game is not True:
            try:
                cur.execute("UPDATE GAME set Game = True WHERE IDChat = '%i'" % chatid)
            except Exception:
                conn.rollback()
            else:
                conn.commit()

            game(message)

        #   ПРОВЕРКА МОЖНО БРОСАТЬ КУБИКИ
        try:
            if Game is True:
                chekbet(message)


        except Exception:
            time.sleep(1)


bonnums = []
to_del = []
@bot.callback_query_handler(func=lambda c: True)
def inl(c):
    global bonusmesid, lavebonus, mnozitel, numbonus, bonnums, paluchi, bonuserid, bonusmesid, to_del
    chatid = c.message.chat.id
    userid = c.from_user.id
    name = c.from_user.first_name
    lastname = c.from_user.last_name
    username = c.from_user.username

    if c.data == '5 на 1':
        beta = 5
        numa = '1'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 2':
        beta = 5
        numa = '2'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 3':
        beta = 5
        numa = '3'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 4':
        beta = 5
        numa = '4'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 5':
        beta = 5
        numa = '5'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 6':
        beta = 5
        numa = '6'
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)
                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)
                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 1-3':
        beta = 5
        numa = '1-3'

        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)
                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                        userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 4-6':
        beta = 5
        numa = '4-6'

        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 1-2':
        beta = 5
        numa = '1-2'

        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 3-4':
        beta = 5
        numa = '3-4'

        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)
                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)
    if c.data == '5 на 5-6':
        beta = 5
        numa = '5-6'

        #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
        try:
            cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
            groshi = cur.fetchall()[0][0]
            if groshi >= beta:
                #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                    userid, chatid))
                UsNum = cur.fetchall()
                if (numa,) in UsNum:
                    #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                    cur.execute(
                        "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                            userid, numa, chatid))
                    UsBet = cur.fetchall()[0][0]
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta + UsBet, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (beta, userid, chatid, numa))
                    conn.commit()
                else:
                    bet_mes = bot.send_message(chatid,
                                               "<a href='tg://user?id=%i'>%s</a> поставил %i грывэнь на %s" % (
                                                   userid, name, beta, numa), parse_mode="HTML")
                    to_del.append(bet_mes.message_id)

                    cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                "VALUES ('%i', '%i', '%s', '%i')" % (userid, beta, numa, chatid))

                    cur.execute(
                        "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                        "WHERE UserId = '%i'" % (name, lastname, username, beta, userid))
                    conn.commit()

            else:
                bot.send_message(chatid,
                                 "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                     userid, name), parse_mode="HTML")
        except Exception:
            time.sleep(1)

    try:
        a = bonusmesid.copy()
        if c.data == "Бросить":
            for key, v in a.items():
                if userid == key and a.get(key) == c.message.message_id:
                    keybonus = types.InlineKeyboardMarkup()
                    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить1")
                    keybonus.add(bonusik)

                    numbonus = int(np.random.randint(1, 7, 1)[0])


                    cur.execute("UPDATE BONUS set BONNUM1 = %i WHERE UserId = %i" % (numbonus, key))
                    conn.commit()

                    cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                    paluchi3 = cur.fetchall()[0][0]

                    bot.edit_message_text(chat_id=chatid, message_id=a.get(key),
                                          text="<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                               "Лавэ %i, коеффициент = %.1f\n\n"
                                               "             <b>%i</b> : 🎲 : 🎲 \n" %
                                               (userid, name, paluchi3, 1, numbonus),
                                          parse_mode="HTML", reply_markup=keybonus)

        if c.data == "Бросить1":
            for key, v in a.items():
                if userid == key and a.get(key) == c.message.message_id:

                    keybonus = types.InlineKeyboardMarkup()
                    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить2")
                    keybonus.add(bonusik)

                    numbonus1 = int(np.random.randint(1, 7, 1)[0])

                    cur.execute("UPDATE BONUS set BONNUM2 = %i WHERE UserId = %i" % (numbonus1, key))
                    conn.commit()

                    cur.execute("SELECT BONNUM1, BONNUM2 FROM BONUS WHERE UserId = %i" % key)
                    g = cur.fetchall()

                    bonnums = [g[0][0], g[0][1]]

                    if len(list(set(bonnums))) == 1:
                        if bonnums[0] == 1:
                            mnozitel = 1.5
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))

                            cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                            paluchi = cur.fetchall()[0][0]
                            paluchi = paluchi * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()

                        if bonnums[0] == 2:
                            mnozitel = 2.3
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))

                            cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                            paluchi = cur.fetchall()[0][0]
                            paluchi = paluchi * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()

                        if bonnums[0] == 3:
                            mnozitel = 3.1
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))
                            paluchi = lavebonus * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()
                        if bonnums[0] == 4:
                            mnozitel = 3.9
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))

                            cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                            paluchi = cur.fetchall()[0][0]
                            paluchi = paluchi * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()

                        if bonnums[0] == 5:
                            mnozitel = 4.7
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))

                            cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                            paluchi = cur.fetchall()[0][0]
                            paluchi = paluchi * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()

                        if bonnums[0] == 6:
                            mnozitel = 5.5
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, key))

                            cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                            paluchi = cur.fetchall()[0][0]
                            paluchi = paluchi * mnozitel
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi, key))
                            conn.commit()

                    cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                    paluchi = cur.fetchall()[0][0]

                    cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % key)
                    boncoef = cur.fetchall()[0][0]

                    bot.edit_message_text(chat_id=chatid, message_id=a.get(key),
                                          text="<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                               "Лавэ %i, коеффициент = %.1f\n\n"
                                               "               <b>%i</b> : <b>%i</b> : 🎲 \n" %
                                               (userid, name, paluchi, boncoef, bonnums[0], bonnums[1]),
                                          parse_mode="HTML", reply_markup=keybonus)

        if c.data == "Бросить2":
            for key, v in a.items():
                if userid == key and a.get(key) == c.message.message_id:
                    keybonus = types.InlineKeyboardMarkup()
                    bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить3")
                    keybonus.add(bonusik)

                    numbonus = int(np.random.randint(1, 7, 1)[0])

                    cur.execute("UPDATE BONUS set BONNUM3 = %i WHERE UserId = %i" % (numbonus, key))
                    conn.commit()

                    cur.execute("SELECT BONNUM1, BONNUM2, BONNUM3 FROM BONUS WHERE UserId = %i" % key)
                    t = cur.fetchall()
                    bonnums1 = [t[0][0], t[0][1], t[0][2]]

                    if len(list(set(bonnums1))) != 1 and bonnums1[0] == bonnums1[2] or bonnums1[1] == bonnums1[2]:
                        if bonnums1[2] == 1:
                            mnozitel1 = 1.5
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()

                        if bonnums1[2] == 2:
                            mnozitel1 = 2.3
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()
                        if bonnums1[2] == 3:
                            mnozitel1 = 3.1
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()
                        if bonnums1[2] == 4:
                            mnozitel1 = 3.9
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()
                        if bonnums1[2] == 5:
                            mnozitel1 = 4.7
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()
                        if bonnums1[2] == 6:
                            mnozitel1 = 5.5
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel1, key))
                            paluchi1 = lavebonus * mnozitel1
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi1, key))
                            conn.commit()

                    if len(list(set(bonnums1))) == 1:
                        if bonnums1[0] == 1:
                            mnozitel2 = 25
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()
                        if bonnums1[0] == 2:
                            mnozitel2 = 28
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()
                        if bonnums1[0] == 3:
                            mnozitel2 = 33
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()
                        if bonnums1[0] == 4:
                            mnozitel2 = 38
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()
                        if bonnums1[0] == 5:
                            mnozitel2 = 45
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()
                        if bonnums1[0] == 6:
                            mnozitel2 = 50
                            cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, key))
                            paluchi3 = lavebonus * mnozitel2
                            cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi3, key))
                            conn.commit()

                    cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % key)
                    paluchi5 = cur.fetchall()[0][0]

                    cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (paluchi5, key))
                    conn.commit()

                    cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % key)
                    boncoef5 = cur.fetchall()[0][0]

                    bot.edit_message_text(chat_id=chatid, message_id=a.get(key),
                                          text="<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                               "Лавэ %i, коеффициент = %.1f\n\n"
                                               "               <b>%i</b> : <b>%i</b> : <b>%i</b> \n" %
                                               (
                                                   userid, name, paluchi5, boncoef5, bonnums1[0], bonnums1[1],
                                                   bonnums1[2]),
                                          parse_mode="HTML", reply_markup=keybonus)

                    time.sleep(2)
                    bot.edit_message_text(chat_id=chatid, message_id=a.get(key),
                                          text="<a href='tg://user?id=%i'>%s</a> забирает свой бонус %i" %
                                               (bonuserid, name, paluchi5), parse_mode="HTML")
                    del bonusmesid[key]
                    cur.execute("DELETE FROM BONUS WHERE UserId = %i" % key)
                    conn.commit()

    except Exception:
        time.sleep(1)


bul = False


@bot.message_handler(commands=['tryasti'])
@bot.message_handler(content_types=['text'], regexp='Трясти')
@bot.message_handler(content_types=['text'], regexp='Го')
def shake_game(message):
    global Game, Shake, bul, checkgame
    chatid = message.chat.id
    userid = message.from_user.id

    if len(message.text.split()) == 1 and message.text.lower() == "го" \
            or message.text.lower() == "трясти" or message.text[:8] == '/tryasti':

        #   ВЫГРУЗКА ПАРАМЕТРА GAME
        try:
            cur.execute("SELECT Game FROM GAME WHERE IDChat = '%i'" % chatid)
            Game = cur.fetchall()[0][0]
        except Exception:
            time.sleep(1)

        try:
            cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i" % chatid)
            usebets = cur.fetchall()
            if usebets and (userid,) in usebets:
                cur.execute("UPDATE GAME set Shake = True WHERE IDChat = '%i'" % chatid)
                conn.commit()
        except Exception:
            time.sleep(1)
        try:
            cur.execute("SELECT Shake FROM GAME WHERE IDChat = '%i'" % chatid)
            Shake = cur.fetchall()[0][0]
        except Exception:
            time.sleep(1)

        #   БРОСИТЬ КУБИКИ
        if Game is True and Shake is True:
            if bul is False:
                bul = True
                checkgame = False
                shake(message)
                bul = False

        # ЕСЛИ НЕ СДЕЛАЛ СТАВКУ
        if Game is True and Shake is False:
            bot.send_message(chatid, "Сначала сделай ставку", reply_to_message_id=message.message_id)

        #   АНТИСПАМ
        if Game is False and Shake is False:
            pass


@bot.message_handler(content_types=['text'], regexp='Отмена')
def cancelbets(message):
    chatid = message.chat.id
    userid = message.from_user.id
    if len(message.text.split()) == 1 and ''.join(list(message.text.lower())[:6]) == "отмена":
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
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
                        bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a> отмэныл ставки" % (
                            userid, name), reply_to_message_id=message.message_id, parse_mode="HTML")

                    else:
                        bot.send_message(chatid, "Отменять то нечего", reply_to_message_id=message.message_id)
                except NameError:
                    pass
            else:
                pass
        else:
            pass


@bot.message_handler(content_types=['text'], regexp='Ставки')
def userbets(message):
    chatid = message.chat.id
    if len(message.text.split()) == 1 and ''.join(list(message.text.lower())[:6]) == "ставки":
        try:
            cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
            Game = cur.fetchall()[0][0]
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
                            Stavki += makegoodview(bets) + ' грыв на ' + nums + '\n'
                        if Stavki == '':
                            bot.send_message(chatid, "%s, нэма ставок" % Name)
                        else:
                            bot.send_message(chatid, "Ставочки %s:\n%s" % (Name, Stavki))
                    else:
                        bot.send_message(chatid, "%s, нэма ставок" % Name)
                except IndexError:
                    userbets(message)
            else:
                pass

        except Exception as e:
            time.sleep(1)


@bot.message_handler(content_types=['text'], regexp='логи')
def logsgame(message):
    chatid = message.chat.id
    alldataCHAT(chatid)

    LOG = ''
    namedb = 'logchat' + str(abs(chatid))
    try:
        cur.execute("SELECT Log FROM %s" % namedb)
        logs = cur.fetchall()

        for i in range(len(logs)):
            LOG += "🎲  %s\n" % logs[i][0]
        if LOG != '':
            bot.send_message(chatid, LOG)
        else:
            bot.send_message(chatid, "Лог пустой")
    except Exception:
        time.sleep(1)


@bot.message_handler(commands=['lave'])
@bot.message_handler(content_types=['text'], regexp='Лавэ')
def usermoney(message):
    if len(message.text.split()) == 1 or message.text.lower()[:5] == '/lave':
        name = message.from_user.first_name
        lastname = message.from_user.last_name
        username = message.from_user.username
        userid = message.from_user.id
        chatid = message.chat.id
        alldataUSERS(name, lastname, username, userid, chatid)
        try:
            cur.execute("SELECT Money From USERS Where UserId = '%i'" % userid)
            mon = cur.fetchall()[0][0]

            bot.send_message(chatid, "%s грывень" % makegoodview(mon), reply_to_message_id=message.message_id)
        except Exception:
            time.sleep(1)


bonusmesid = {}
@bot.message_handler(commands=['bonuslave'])
@bot.message_handler(content_types=['text'], regexp='Бонус')
def bonus(message):
    global bonusmesid, lavebonus, mnozitel, numbonus, bonusdate, bonuserid, bonnums, value
    if len(message.text.split()) == 1 or message.text.lower()[:11] == "/bonuslave"\
                                      or message.text.lower()[:5] == "бонус":
        chatid = message.chat.id
        name = message.from_user.first_name
        bonuserid = message.from_user.id
        username = message.from_user.username
        lastname = message.from_user.last_name
        alldataUSERS(name, lastname, username, bonuserid, chatid)

        cur.execute("SELECT BONUSTIME FROM USERS WHERE UserId = %i" % bonuserid)
        bonustime = int(cur.fetchall()[0][0])

        ostalos = bonustime - message.date

        punkt = int(time.time()) + 21600
        value = datetime.fromtimestamp(punkt).strftime('%H:%M:%S')

        if bonuserid != 526497876 and bonuserid != 547400918 and ostalos > 0:
            value = datetime.fromtimestamp(ostalos).strftime('%H:%M:%S')
            bot.send_message(chatid, "Бонусное лавэ можно получить через %s" % value,
                             reply_to_message_id=message.message_id)

        elif bonuserid == 526497876 or bonuserid == 547400918 or bonustime == 0 or ostalos <= 0:
            keybonus = types.InlineKeyboardMarkup()
            bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить")
            keybonus.add(bonusik)

            lavebonus = int(random.randrange(400, 800))
            mnozitel = 1

            cur.execute(
                "INSERT INTO BONUS (UserId, BONCOEF, BONNUM1, BONNUM2, BONNUM3, LAVE) VALUES (%i, 1, 0, 0, 0, %i)"
                % (bonuserid, lavebonus))
            conn.commit()

            bonusmes = bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                                "Лавэ %i, коеффициент = 1.0\n\n"
                                                "           🎲 : 🎲 : 🎲 \n" % (bonuserid, name, lavebonus),
                                        parse_mode="HTML", reply_markup=keybonus)

            bonusmesid.update([(bonuserid, bonusmes.message_id)])

            cur.execute("UPDATE USERS set BONUSTIME = %i WHERE UserId = %i" % (punkt, bonuserid))
            conn.commit()


@bot.message_handler(content_types=['text'], regexp='!рейтинг')
def top(message):
    if len(message.text.split()) == 1 and message.text == '!рейтинг' and message.chat.id != message.from_user.id:
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

            bot.send_message(chatid, topchik)
        except Exception:
            pass

    elif len(message.text.split()) == 2 and message.text == '!рейтинг 10' and message.chat.id != message.from_user.id:
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
                    if top[k][0] != 547400918 and top[k][0] != 526497876:
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

            bot.send_message(chatid, topchik)
        except Exception:
            pass

@bot.message_handler(content_types=['text'], regexp='!стата')
def statuser(message):
    chatid = message.chat.id
    if len(message.text.split()) == 1 and message.text == '!стата':
        try:
            if message.reply_to_message is not None and message.reply_to_message.json['from']['is_bot'] is False:
                userid = message.reply_to_message.from_user.id
                cur.execute("SELECT Name, LastName, Money, Won, Lost FROM Users WHERE UserId = %i" % userid)
                usstat = cur.fetchall()
                profile = ''

                if usstat[0][1] == 'None':
                    Name = str(usstat[0][0])
                else:
                    Name = str(usstat[0][0]) + ' ' + str(usstat[0][1])
                Lave = makegoodview(usstat[0][2])
                Won = usstat[0][3]
                Lost = usstat[0][4]

                profile += "<b>Имя: </b>%s\n" \
                           "<b>Лавэ: </b>%s\n" \
                           "<b>Выиграно: </b>%s\n" \
                           "<b>Проиграно: </b>%s\n" \
                           "\n" \
                           "<b>Id: </b>%i" % (Name, Lave, Won, Lost, userid)
                bot.send_message(chatid, profile, parse_mode='HTML')

            else:
                userid = message.from_user.id
                cur.execute("SELECT Name, LastName, Money, Won, Lost FROM Users WHERE UserId = %i" % userid)
                usstat = cur.fetchall()
                profile = ''
                if usstat[0][1] == 'None':
                    Name = str(usstat[0][0])
                else:
                    Name = str(usstat[0][0]) + ' ' + str(usstat[0][1])
                Lave = makegoodview(usstat[0][2])
                Won = usstat[0][3]
                Lost = usstat[0][4]

                profile += "<b>Имя: </b>%s\n" \
                           "<b>Лавэ: </b>%s\n" \
                           "<b>Выиграно: </b>%s\n" \
                           "<b>Проиграно: </b>%s\n" \
                           "\n" \
                           "<b>Id: </b>%i" % (Name, Lave, Won, Lost, userid)
                bot.send_message(chatid, profile, parse_mode='HTML')
        except Exception:
            pass

    try:
        if message.text.split()[0] == '!стата' and message.text.lower().split()[1] == "сбросить":
            userid = message.from_user.id
            cur.execute("UPDATE USERS set WON = 0, LOST = 0 WHERE UserId = %i" % userid)
            conn.commit()
        bot.send_message(chatid, "Стата сброшена")
    except Exception:
        pass


#  ПРИНЯТИЕ СТАВОК
@bot.message_handler(content_types=['text'])
def chekbet(message):
    global cur, conn, bet, num, Game, checkgame, to_del
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username
    userid = message.from_user.id
    chatid = message.chat.id

    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception:
        time.sleep(1)
        Game = False

    #   ПРОВЕРКА НА СТАВКУ
    if Game is True:
        text = message.text
        name = message.from_user.first_name
        lastname = message.from_user.last_name
        username = message.from_user.username
        userid = message.from_user.id
        chatid = message.chat.id
        bet = 0
        num = ''

        alldataUSERS(name, lastname, username, userid, chatid)
        # ПРОВЕРКА НА СТАВКУ
        # ЕСЛИ ЗАПИСЬ 100 2

        if len(text.split()) == 2:
            try:
                if (isinstance((int(text.split()[0])), int)) is True \
                        and (isinstance((int(text.split()[1])), int)) is True \
                        and int(text.split()[0]) > 0 and 0 < int(text.split()[1]) <= 6:

                    bet = int(text.split()[0])
                    num = str(text.split()[-1])

                    #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                    groshi = cur.fetchall()[0][0]
                    if groshi >= bet:
                        #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                            userid, chatid))
                        UsNum = cur.fetchall()
                        if (num,) in UsNum:
                            #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                            cur.execute(
                                "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s' AND IDChat = %i" % (
                                    userid, num, chatid))
                            UsBet = cur.fetchall()[0][0]
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet + UsBet), num),
                                                       reply_to_message_id=message.message_id,
                                                       parse_mode="HTML")
                            to_del.append(bet_mes.message_id)

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))

                            cur.execute(
                                "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                "AND Numbers = '%s'" % (bet, userid, chatid, num))
                            conn.commit()
                        else:
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet), num),
                                                       reply_to_message_id=message.message_id, parse_mode="HTML")
                            to_del.append(bet_mes.message_id)

                            cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                        "VALUES ('%i', '%i', '%s', '%i')" % (userid, bet, num, chatid))

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))
                            conn.commit()

                    else:
                        bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                             userid, name), reply_to_message_id=message.message_id,
                                         parse_mode="HTML")


            except Exception:
                conn.rollback()
                pass

        # ЕСЛИ ЗАПИСЬ 100 2-4
        if len(text.split()) == 2:
            try:
                if (isinstance((int(text.split()[0])), int)) is True \
                        and int(text.split()[0]) > 0 \
                        and (isinstance((int(text.split()[1].split("-")[0])), int)) is True \
                        and (isinstance((int(text.split()[1].split("-")[1])), int)) is True \
                        and 0 < (int(text.split()[1].split("-")[0])) < (
                        int(text.split()[1].split("-")[1])) <= 6:

                    bet = int(text.split()[0])
                    num = text.split()[-1]

                    #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                    groshi = cur.fetchall()[0][0]
                    if groshi >= bet:
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i'" % userid)
                        UsNum = cur.fetchall()
                        if (num,) in UsNum:
                            #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                            cur.execute(
                                "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s'" % (
                                    userid, num))
                            UsBet = cur.fetchall()[0][0]
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet + UsBet), num),
                                                       reply_to_message_id=message.message_id,
                                                       parse_mode="HTML")
                            to_del.append(bet_mes.message_id)
                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))

                            cur.execute(
                                "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                "AND Numbers = '%s'" % (bet, userid, chatid, num))

                            conn.commit()
                        else:
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet), num),
                                                       reply_to_message_id=message.message_id, parse_mode="HTML")
                            to_del.append(bet_mes.message_id)
                            cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                        "VALUES ('%i', '%i', '%s', '%i')" % (userid, bet, num, chatid))

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))
                            conn.commit()

                    else:
                        bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a>, нету столько"
                                         % (userid, name), reply_to_message_id=message.message_id,
                                         parse_mode="HTML")

            except Exception:
                conn.rollback()
                pass

        # ЕСЛИ ЗАПИСЬ 100 НА 2-4
        if len(text.split()) == 3 and text.split()[1].lower() == 'на':
            try:
                if (isinstance((int(text.split()[0])), int)) is True \
                        and int(text.split()[0]) > 0 \
                        and (isinstance((int(text.split()[2].split("-")[0])), int)) is True \
                        and (isinstance((int(text.split()[2].split("-")[1])), int)) is True \
                        and 0 < (int(text.split()[2].split("-")[0])) < (
                        int(text.split()[2].split("-")[1])) <= 6:

                    bet = int(text.split()[0])
                    num = text.split()[-1]

                    #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                    groshi = cur.fetchall()[0][0]
                    if groshi >= bet:
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i'" % userid)
                        UsNum = cur.fetchall()
                        if (num,) in UsNum:
                            #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                            cur.execute(
                                "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s'" % (
                                    userid, num))
                            UsBet = cur.fetchall()[0][0]
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet + UsBet), num),
                                                       reply_to_message_id=message.message_id,
                                                       parse_mode="HTML")
                            to_del.append(bet_mes.message_id)

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i' "
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))

                            cur.execute(
                                "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                "AND Numbers = '%s'" % (bet, userid, chatid, num))
                            conn.commit()
                        else:
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet), num),
                                                       reply_to_message_id=message.message_id, parse_mode="HTML")
                            to_del.append(bet_mes.message_id)
                            cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                        "VALUES ('%i', '%i', '%s', '%i')" % (userid, bet, num, chatid))

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))
                            conn.commit()
                    else:
                        bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                             userid, name), reply_to_message_id=message.message_id,
                                         parse_mode="HTML")
            except Exception:
                conn.rollback()
                pass

        # ЕСЛИ ЗАПИСЬ 100 НА 2
        if len(text.split()) == 3 and text.split()[1].lower() == 'на':
            try:
                if (isinstance((int(text.split()[0])), int)) is True \
                        and int(text.split()[0]) > 0 \
                        and (isinstance((int(text.split()[2])), int)) is True \
                        and 0 < int(text.split()[2]) <= 6:

                    bet = int(text.split()[0])
                    num = text.split()[-1]

                    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
                    groshi = cur.fetchall()[0][0]
                    if groshi >= bet:
                        cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i'" % userid)
                        UsNum = cur.fetchall()
                        if (num,) in UsNum:
                            #   ВЫГРУЗКА ДЕНЕЖНОЙ СТАВКИ
                            cur.execute(
                                "SELECT Bet FROM BETS WHERE UserId = '%i' AND Numbers = '%s'" % (
                                    userid, num))
                            UsBet = cur.fetchall()[0][0]
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet + UsBet), num),
                                                       reply_to_message_id=message.message_id,
                                                       parse_mode="HTML")
                            to_del.append(bet_mes.message_id)
                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))

                            cur.execute(
                                "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                                "AND Numbers = '%s'" % (bet, userid, chatid, num))
                            conn.commit()
                        else:
                            bet_mes = bot.send_message(chatid,
                                                       "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s" % (
                                                           userid, name, makegoodview(bet), num),
                                                       reply_to_message_id=message.message_id, parse_mode="HTML")
                            to_del.append(bet_mes.message_id)
                            cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat) "
                                        "VALUES ('%i', '%i', '%s', '%i')" % (userid, bet, num, chatid))

                            cur.execute(
                                "UPDATE USERS SET Name = '%s', LastName = '%s', UserName = '%s' , Money = Money - '%i'"
                                "WHERE UserId = '%i'" % (name, lastname, username, bet, userid))
                            conn.commit()
                    else:
                        bot.send_message(chatid,
                                         "<a href='tg://user?id=%i'>%s</a>, нету столько" % (
                                             userid, name), reply_to_message_id=message.message_id,
                                         parse_mode="HTML")
            except Exception:
                conn.rollback()
                pass

    #    ПЕРЕДАТЬ ДЕНЬГИ КОМУ ТО
    if message.text[:2] == '+г' and message.text[2:].split() != []:
        alldataUSERS(name, lastname, username, userid, chatid)
        try:
            if message.text[2:].split() != [] and (isinstance((int(message.text[2:].split()[0])), int)) is True \
                    and int(''.join(message.text[2:].split())) > 0:
                howmuch = int(''.join(message.text[2:].split()))
                userid = message.from_user.id
                name = message.from_user.first_name
                chatid = message.chat.id
                whoid = message.reply_to_message.from_user.id
                cur.execute("SELECT Money FROM USERS WHERE UserId = %i" % userid)
                denga = int(cur.fetchall()[0][0])
                if userid != whoid:
                    if howmuch <= denga:
                        whoname = message.reply_to_message.from_user.first_name
                        isbot = message.reply_to_message.from_user.is_bot
                        if isbot is False:
                            cur.execute(
                                "UPDATE USERS set Money = Money - %i WHERE UserId = %i" % (howmuch, userid))
                            cur.execute(
                                "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (howmuch, whoid))
                            bot.send_message(chatid,
                                             "<a href='tg://user?id=%i'>%s</a> передал <a href='tg://user?id=%i'>%s</a> %s грывень" %
                                             (userid, name, whoid, whoname, makegoodview(howmuch)),
                                             parse_mode="HTML")
                            conn.commit()
                        else:
                            pass
                    else:
                        bot.send_message(chatid, "Нету столько", reply_to_message_id=message.message_id)
                else:
                    pass
        except Exception:
            conn.rollback()


def game(message):
    global startmes
    chatid = message.chat.id
    #   ИГРА
    key = types.InlineKeyboardMarkup(row_width=3)
    t1 = types.InlineKeyboardButton(text='5 на 1', callback_data="5 на 1")
    t2 = types.InlineKeyboardButton(text='5 на 2', callback_data="5 на 2")
    t3 = types.InlineKeyboardButton(text='5 на 3', callback_data="5 на 3")
    t4 = types.InlineKeyboardButton(text='5 на 4', callback_data="5 на 4")
    t5 = types.InlineKeyboardButton(text='5 на 5', callback_data="5 на 5")
    t6 = types.InlineKeyboardButton(text='5 на 6', callback_data="5 на 6")

    t13 = types.InlineKeyboardButton(text='5 на 1-3', callback_data="5 на 1-3")
    t46 = types.InlineKeyboardButton(text='5 на 4-6', callback_data="5 на 4-6")

    t12 = types.InlineKeyboardButton(text='5 на 1-2', callback_data="5 на 1-2")
    t34 = types.InlineKeyboardButton(text='5 на 3-4', callback_data="5 на 3-4")
    t56 = types.InlineKeyboardButton(text='5 на 5-6', callback_data="5 на 5-6")

    key.add(t1, t2, t3, t4, t5, t6, t13, t46)
    key.row(t12, t34, t56)

    startmes = bot.send_message(chatid, "🧖🏽‍♂️Бросаем кубики нэ стесняемся🎲\n"
                                        "Угадай число от 1 до 6\n"
                                        "Делай ставки не скупи💰\n",
                                reply_markup=key)


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


def alldataCHAT(chatid):
    #   ДОБАВЛЕНИЕ ЧАТА
    try:
        cur.execute("SELECT Count(IDChat) FROM GAME WHERE IDChat = %i" % chatid)
        IDChat = cur.fetchall()[0][0]
        if IDChat == 1:
            pass
        if IDChat < 1:
            cur.execute("INSERT INTO GAME (IDChat) VALUES (%i)" % chatid)
    except Exception:
        time.sleep(1)
    else:
        conn.commit()

    #   ДОБАВЛЕНИЕ ТАБЛИЦЫ ЛОГОВ ЧАТА
    try:
        namedb = 'logchat' + str(abs(chatid))
        cur.execute("CREATE TABLE if not exists %s"
                    "(Id     Serial,"
                    "Log     VARCHAR(20)  NOT NULL,"
                    "PRIMARY KEY(Id));" % namedb)
    except Exception:
        time.sleep(1)
    else:
        conn.commit()


def alldataUSERS(name, lastname, username, userid, chatid):
    #   ДОБАВЛЕНИЕ ИГРОКОВ
    try:
        cur.execute("SELECT Count(UserId) FROM USERS WHERE UserId = '%i'" % userid)
        UserdIds = cur.fetchall()[0][0]
        if UserdIds == 1:
            pass
        if UserdIds < 1:
            cur.execute("INSERT INTO USERS (Name, LastName, UserName, UserId, Money, Bonustime) "
                        "VALUES ('%s','%s','%s','%i','%i', 0)" % (name, lastname, username, userid, 5000))
    except Exception:
        time.sleep(2)
    else:
        conn.commit()

    #   ДЛЯ РЕЙТИНГА
    try:
        if userid != chatid:
            cur.execute("SELECT Count(UserId) FROM chatusers WHERE IDChat = %i AND UserID = %i" % (chatid, userid))
            UserdIds = cur.fetchall()[0][0]
            if UserdIds == 1:
                pass

            elif UserdIds < 1:
                cur.execute("INSERT INTO chatusers (IDChat, UserId) VALUES (%i, %i)" % (chatid, userid))
    except Exception:
        time.sleep(2)
    else:
        conn.commit()


def shake(message):
    global startmes, to_del
    name = message.from_user.first_name
    userid = message.from_user.id
    chatid = message.chat.id

    try:
        bot.delete_message(chatid, startmes.message_id)
    except Exception:
        pass

    for i in range(len(to_del)):
        bot.delete_message(chatid, to_del[i])
    to_del = []

    text = "[%s](tg://user?id=%i) бросает кубик (5 секунд)" % (name, userid)
    mes1 = bot.send_message(chatid, text=text, parse_mode="Markdown")

    time.sleep(5)
    mes2 = bot.send_document(message.chat.id, data=random.choice(Gifs))
    time.sleep(2)
    bot.delete_message(chatid, mes1.message_id)
    bot.delete_message(chatid, mes2.message_id)

    #   РАНДОМНОЕ ЧИСЛО
    algoritm(message)

    #   ВЫГРУЗКА ВСЕХ СТАВОК
    endgame(message)

    namedb = 'logchat' + str(abs(chatid))
    cur.execute("INSERT INTO %s (Log) VALUES (%i)" % (namedb, Number))
    conn.commit()

    #   STOP GAME
    cur.execute("UPDATE GAME set Game = False WHERE IDChat = %i" % chatid)
    conn.commit()

    #   STOP SHAKE
    cur.execute("UPDATE GAME set Shake = False WHERE IDChat = %i" % chatid)
    conn.commit()

    cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
    conn.commit()


def endgame(message):
    chatid = message.chat.id
    # ВСЕ СТАВКИ
    Fstat = ''
    WINstat = ''
    ALLwins = 0
    Lose = 0
    cur.execute("SELECT Id FROM BETS WHERE IDChat = %i AND Bet > 0" % chatid)
    IDs = cur.fetchall()
    for uid in IDs:
        cur.execute("SELECT UserId, Bet, Numbers FROM BETS WHERE Id = %i" % uid)
        ALLBets = cur.fetchall()

        UsId = ALLBets[0][0]
        UsBet = str(ALLBets[0][1])
        UsNum = str(ALLBets[0][2])

        cur.execute("SELECT Name FROM USERS WHERE UserId = %i" % UsId)
        Names = str(cur.fetchall()[0][0])

        #   ВСЕ СТАВКИ
        Fstat += Names + ' ' + UsBet + ' на ' + UsNum + '\n'

        #   ВЫИГРАЛИ
        if len(UsNum.split('-')) == 2 and int(UsNum.split('-')[0]) <= Number <= int(UsNum.split('-')[1]):
            Prize = int(int(UsBet) * 6 / (int(UsNum.split('-')[1]) - int(UsNum.split('-')[0]) + 1))
            ALLwins += 1

            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Prize, UsId))
            cur.execute("UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (Prize, UsId))
            conn.commit()

            WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                       " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

        elif len(UsNum.split('-')) == 1 and int(UsNum) == Number:
            Prize = int(int(UsBet) * 6)
            ALLwins += 1

            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (Prize, UsId))
            cur.execute("UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (Prize, UsId))
            conn.commit()

            WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                       " заработал " + makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

        try:
            if int(UsNum) != Number:
                Lose += 1
                cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                conn.commit()
        except Exception:
            pass

        try:
            if int(UsNum.split('-')[1]) < Number:
                Lose += 1
                cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                conn.commit()
        except Exception:
            pass

        try:
            if Number <= int(UsNum.split('-')[0]):
                Lose += 1
                cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                conn.commit()
        except Exception:
            pass

    cur.execute("UPDATE STATS set WON = WON + %i, LOST = LOST + %i, PLAYS = PLAYS + 1 WHERE Id = 1" % (ALLwins, Lose))

    if WINstat == '':
        WINstat = 'Вах, никто нэ выиграл'

    bot.send_message(chatid, "🎲  %i\nСтавки:\n%s \n%s" % (Number, Fstat, WINstat), parse_mode='HTML')


def algoritm(message):
    global Number
    chatid = message.chat.id
    Number = np.random.randint(1, 7, 1)[0]
    # Number1 = np.random.randint(1, 7, 1)[0]

    namedb = 'logchat' + str(abs(chatid))
    cur.execute("SELECT count(Id) FROM %s" % namedb)
    kaunt = cur.fetchall()
    if kaunt[0][0] > 9:
        cur.execute("DELETE FROM %s WHERE Id <= (SELECT MAX(Id) FROM %s) - 10" % (namedb, namedb))
        conn.commit()


bot.polling(none_stop=False, interval=0, timeout=100)
