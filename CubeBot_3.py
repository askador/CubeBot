from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import numpy as np
from aiogram.dispatcher import Dispatcher
import psycopg2
import asyncio
import random
import datetime
import time

from aiogram.utils.exceptions import Unauthorized, MessageError

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
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


@dp.message_handler(commands=['rules'])
async def rules_for_player(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


@dp.message_handler(commands=['help'])
async def help_for_player(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


#  |  ЗАПУСК ИГРЫ  |
@dp.message_handler(commands=['kosti'])
@dp.message_handler(lambda message: message.text.lower() == 'кости')
async def start_game(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


#  БРОСИТЬ КУБИКИ
@dp.message_handler(commands=['tryasti'])
@dp.message_handler(lambda message: message.text.lower() == 'трясти')
@dp.message_handler(lambda message: message.text.lower() == 'го')
async def shake_game(message):
    global shakeit, auto_start_dict
    chatid = message.chat.id
    userid = message.from_user.id

    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()

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

    conn.close()


#  Ставки игрока
@dp.message_handler(lambda message: message.text.lower() == 'ставки')
async def userbets(message):
    chatid = message.chat.id
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    try:
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
    global shakeit
    chatid = message.chat.id
    userid = message.from_user.id
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    try:
        cur.execute("SELECT Game FROM GAME WHERE IDChat = %i" % chatid)
        Game = cur.fetchall()[0][0]
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
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
                                await message.reply("<a href='tg://user?id=%i'>%s</a> отмэныл ставки" % (
                                    userid, name))

                            else:
                                message.reply("Отменять нечего")
                        except Exception as e:
                            await message.reply("Oops. something went wrong. Try again.")
            except Exception:
                await message.reply("Oops. something went wrong. Try again.")
                shakeit.update([(chatid, False)])
    conn.close()


#  БАЛАНС ИГРОКА
@dp.message_handler(commands=['lave'])
@dp.message_handler(lambda message: message.text.lower() == 'лавэ')
async def usermoney(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


@dp.message_handler(commands=['bonuslave'])
@dp.message_handler(lambda message: message.text.lower() == 'бонус')
async def bonus(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


async def start_bonus(name, userid, chatid):
    await asyncio.sleep(300)
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()


#  users stats
@dp.message_handler(text='!стата')
async def statuser(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


@dp.message_handler(text='!рейтинг')
async def top(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")



async def giveaway_timer(give_mes_id, userid, chatid):
    start_in = 300
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()

    cur.execute(f"SELECT FullName FROM GIVEAWAY%s WHERE UserId = %s" % (abs(chatid), userid))
    starter = str(cur.fetchall()[0][0])

    cur.execute(f"SELECT How_many From GIVEAWAY{abs(chatid)} WHERE UserId = {userid}")
    how_many_proc = int(cur.fetchall()[0][0])

    conn.close()
    while start_in > 0:
        await asyncio.sleep(3)
        start_in -= 3
        try:

            conn = psycopg2.connect(
                "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
            cur = conn.cursor()
            cur.execute(f"SELECT FullName, Value FROM GIVEAWAY{abs(chatid)}"
                        f" WHERE Value IS NOT NULL ORDER BY VALUE DESC")
            giveaway_data = cur.fetchall()
            conn.close()

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
        conn = psycopg2.connect(
            "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
        cur = conn.cursor()
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
        conn.close()


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'раздача')
@dp.throttled(rate=1.3)
async def scores(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    name = callback_query.from_user.full_name
    name1 = callback_query.from_user.first_name
    lastname = callback_query.from_user.last_name
    username = callback_query.from_user.username

    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()


@dp.message_handler(regexp='!раздача ([0-9]+)')
async def giveaway(message):
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


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


# %п ПОВТОР СТАВОК
@dp.message_handler(text='%п')
async def repeat_bet(message):
    global shakeit
    chatid = message.chat.id
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    try:
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
    conn.close()


# %у УДВОИТЬ ВСЕ СТАВКИ
@dp.message_handler(text='%у')
async def double_bet(message):
    chatid = message.chat.id
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    try:
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
    await bot.send_message(message.chat.id, "Временные технические шоколадки...")


# ПРОВЕРКА НА СТАВКУ
@dp.message_handler(regexp="(\d[' ']\d)$")
@dp.message_handler(regexp="(\d[ ]\d[-]\d)$")
@dp.throttled(bet_trottled, rate=1.2)
async def chekbet(message: types.Message):
    global shakeit
    chatid = message.chat.id
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


async def autostart(chatid):
    global shakeit
    await asyncio.sleep(300)

    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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


#  add data of user to db
async def alldataUSERS(name, lastname, username, userid, chatid):
    conn = psycopg2.connect(
        "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
        "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()


async def check_limit_money(userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
    userid = int(userid)
    cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
    money = cur.fetchall()[0][0]
    if money > 2 ** 55:
        cur.execute("UPDATE USERS SET MONEY = %i WHERE USERID = %i" % (10 ** 16, userid))
        conn.commit()
    conn.close()


async def achievs_balance(userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()
    return mess


async def achieves_plays(userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()
    return mess


async def achieves_bonus(bonnums, userid):
    conn = psycopg2.connect("postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
                            "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6")
    cur = conn.cursor()
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
    conn.close()
    return mess


#  start shaking  --> endgame
async def shake(name, userid, chatid):
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

    cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
    conn.commit()
    conn.close()


async def endgame(chatid):
    list_of_plays = []
    list_of_names = {}

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

    conn.close()

    if WINstat == '':
        WINstat = 'Вах, никто нэ выиграл'



    await asyncio.sleep(3)
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


@dp.errors_handler(exception=Unauthorized)
@dp.errors_handler(exception=MessageError)
async def error_handler(update, e):
    print(e)
    return True


# polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
