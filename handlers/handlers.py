# coding=utf-8
import asyncio
from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
from datetime import datetime

from misc import dp, bot, conn, cur
from handlers.add_func import to_del_mess, makegoodview
from handlers.User import User
from handlers.Chat import Chat
from handlers.game import Game
from handlers.bets import Bets
from handlers.shake import shake
from handlers.bonus import Bonus
from handlers.achievements import check_limit_money
from handlers.giveaway_start import create_db, start_giveaway


async def bonus_throttled(callback_query, *args, **kwargs):
    await bot.answer_callback_query(callback_query.id, "Не торопись")


async def trottled(callback_query, *args, **kwargs):
    await bot.answer_callback_query(callback_query.id, "Не торопись")


async def bet_trottled(message, *args, **kwargs):
    await message.reply("Не торопись")


async def advice_anti_spam(message, *args, **kwargs):
    await message.reply("Не спамь")


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


@dp.message_handler(commands=['advice'])
@dp.throttled(advice_anti_spam, rate=10)
async def advice(message):
    chatid = -443076596
    if message.chat.type == 'private':
        if len(message.text.split()) != 1:
            await bot.send_message(chatid, "Oт @%s, %s\n\n%s" %
                                   (message.from_user.username, message.from_user.full_name, message.text))

            await message.reply("Спасибо за совет!")
        else:
            await message.answer("Совет не может быть пустым")
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
            conn.rollback()
        else:
            conn.commit()
            await message.answer(f"Achievement {achieve} was added to {userid}")
            cur.execute("SELECT FullName FROM Users WHERE UserID = %i" % userid)
            name = cur.fetchall()[0][0]

            await bot.send_message(userid, "🌟Сириус стал ярче🌟")
            await asyncio.sleep(2)
            await bot.send_message(userid, "🦜Кукушка услышала пение🦜")
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


@dp.message_handler(commands=['setmoney'])
async def setmoney(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        papaid = message.from_user.id
        howmch = (''.join((message.text.split()[1]).split(',')))
        towho = message.text.split()[2]
        try:
            if howmch.isdigit() is True and towho.isdigit() is True and howmch[0] != '+':
                if 0 <= int(howmch) < 10 ** 33:
                    cur.execute("UPDATE USERS set Money = %i WHERE UserId = %i" % (int(howmch), int(towho)))
                    await bot.send_message(papaid, "SET completed")

                else:
                    await bot.send_message(papaid, "10**33 максимум")

        except Exception as e:
            await message.reply("Input data are not correct\n/setmoney (+)howmuch towho")
            conn.rollback()
        else:
            conn.commit()

        try:
            if howmch[0] == '+':
                if 0 < int(howmch) < 10 ** 25:
                    # Прикрепить сообщение к бонусу
                    if len(message.text.split()) >= 4:
                        note = ' '.join(message.text.split()[3:])
                        cur.execute(
                            "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                        await bot.send_message(papaid, "ADDed")
                        await bot.send_message(towho, "Бонус %s💰\n%s" % (makegoodview(howmch[1:]), note))

                    else:
                        cur.execute(
                            "UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (int(howmch[1:]), int(towho)))
                        conn.commit()
                        await bot.send_message(papaid, "ADDed")
                        await bot.send_message(towho, "Бонус %s💰" % await makegoodview(howmch[1:]))

                    await check_limit_money(towho)
                else:
                    await bot.send_message(papaid, "10**25 максимум")
        except Exception as e:
            await message.reply("Input data are not correct\n/setmoney (+)howmuch towho")
            conn.rollback()
        else:
            conn.commit()


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
                conn.rollback()
            else:
                conn.commit()
                #  Achevement Неуловимый
                await message.reply("Стата %i скрыта" % whoid)

                cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES (%i, 'Неуловимый')" % whoid)

                conn.commit()
                await message.answer(f"Achievement Неуловимый was added to {whoid}")
                cur.execute("SELECT FullName FROM Users WHERE UserID = %i" % whoid)
                name = cur.fetchall()[0][0]

                await bot.send_message(whoid, "🌟Сириус стал ярче🌟")
                await asyncio.sleep(2)
                await bot.send_message(whoid, "🦜Кукушка услышала пение🦜")
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
                conn.rollback()
            else:
                conn.commit()
                await message.reply("Стата %i открыта" % whoid)


@dp.message_handler(lambda msg: msg.reply_to_message is not None and msg.text == "getid")
async def s(message):
    try:
        await message.reply(message.reply_to_message.from_user.id)
    except Exception:
        pass


@dp.message_handler(text='/statslog')
async def stats(message):
    if message.from_user.id == 526497876 or message.from_user.id == 547400918:
        if message.text == '/statslog':
            stat = ''

            try:
                cur.execute("SELECT Plays FROM STATS WHERE Title = 'General'")
                AllPlays = cur.fetchall()[0][0]
                cur.execute("SELECT Won FROM STATS WHERE Title = 'General'")
                Won = cur.fetchall()[0][0]
                cur.execute("SELECT Lost FROM STATS WHERE Title = 'General'")
                Lost = cur.fetchall()[0][0]
            except Exception as e:
                pass
            else:
                try:
                    Winfactor = round((int(Won) / int(Lost)), 3)
                except Exception:
                    Winfactor = 0
                stat += f"<b>Всего сыграно:</b> {AllPlays}\n" \
                        f"<b>Коэффициент выигрыша:</b> {Winfactor}\n\n"

                cur.execute("SELECT IdChat FROM STATS WHERE IdChat is not Null AND Plays > 0")
                chats = cur.fetchall()
                for i in range(len(chats)):
                    cur.execute("SELECT Title FROM STATS WHERE IDChat = %i" % chats[i][0])
                    title = cur.fetchall()[0][0]

                    cur.execute("SELECT Plays FROM STATS WHERE IDChat = %i" % chats[i][0])
                    plays = cur.fetchall()[0][0]

                    cur.execute("SELECT Won FROM STATS WHERE IDChat = %i" % chats[i][0])
                    Won = cur.fetchall()[0][0]

                    cur.execute("SELECT Lost FROM STATS WHERE IDChat = %i" % chats[i][0])
                    Lost = cur.fetchall()[0][0]

                    cur.execute("SELECT bets_num FROM STATS WHERE IDChat = %i" % chats[i][0])
                    bets_num = cur.fetchall()[0][0]

                    cur.execute("SELECT Last_activity FROM STATS WHERE IDChat = %i" % chats[i][0])
                    last_activity = cur.fetchall()[0][0]


                    try:
                        avrg_bets_num = round((int(bets_num) / int(plays)), 3)
                    except Exception:
                        avrg_bets_num = 0
                    try:
                        win_factor = round((int(Won) / int(Lost)), 3)
                    except Exception:
                        win_factor = 0

                    stat += f"Chat Id: <b>{chats[i][0]}</b>\n" \
                            f"Title: <b>{title}</b>\n" \
                            f"Plays: <b>{plays}</b>\n" \
                            f"Win Factor: <b>{win_factor}</b>\n" \
                            f"Average bets number: <b>{avrg_bets_num}</b>\n" \
                            f"Last activity: <b>{last_activity}</b>\n\n"

                await message.answer(stat)


@dp.message_handler(regexp="/statslog сбросить")
async def stats_rollback(message):
    try:
        if message.text.split()[2] == "все":
            cur.execute("UPDATE STATS set Plays = 0, Won = 0, Lost = 0, Bets_Num = 0")
            await message.answer("Все сброшено")
    except Exception as e:
        conn.rollback()
    else:
        conn.commit()

    try:
        if message.text.split()[2].isdigit:
            cur.execute("UPDATE STATS set Plays = 0, Won = 0, Lost = 0, Bets_Num = 0 WHERE IDChat = %s" %
                        message.text.split()[2])
            await message.answer("Сброшено %s" % message.text.split()[2])
    except Exception as e:
        conn.rollback()
    else:
        conn.commit()


#  |  ЗАПУСК ИГРЫ  |
@dp.message_handler(commands=['kosti'])
@dp.message_handler(lambda message: message.text.lower() == 'кости')
async def start_game(message):
    chatid = int(message.chat.id)
    if message.chat.title is not None:
        title = message.chat.title
    else:
        title = message.chat.first_name
    date = str(datetime.fromtimestamp(message.date.timestamp() + 10800))

    await Chat(chatid, title, date).add_chat_data()

    await Game(chatid).play(message)


#  БРОСИТЬ КУБИКИ
@dp.message_handler(commands=['tryasti'])
@dp.message_handler(lambda message: message.text.lower() == 'трясти')
@dp.message_handler(lambda message: message.text.lower() == 'го')
async def shake_game(message):
    chatid = message.chat.id
    userid = message.from_user.id

    # Проверка на возможность бросать кубики
    try:
        cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i" % chatid)
        user_in_bets = cur.fetchall()
        if user_in_bets and (userid,) in user_in_bets:
            cur.execute("UPDATE GAME set Shake = True WHERE IDChat = '%i'" % chatid)
        else:
            cur.execute("UPDATE GAME set Shake = False WHERE IDChat = '%i'" % chatid)
    except Exception as exc:
        pass
    else:
        conn.commit()

    # Выгрузка параметра Shake
    try:
        cur.execute("SELECT Shake FROM GAME WHERE IDChat = '%i'" % chatid)
        Shake = cur.fetchall()[0][0]
    except Exception:
        Shake = False

    # |  БРОСИТЬ КУБИКИ  |  Проверка на антиспам "Трясти"  |   Отстрочка в 30 секунд запуска в группах
    try:
        cur.execute("SELECT shaking FROM GAME WHERE IDChat = %i" % chatid)
        shaking = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        if Shake is True and shaking is False:
            try:
                cur.execute("SELECT Time FROM Game WHERE IDChat = %i" % chatid)
                Time = int(cur.fetchall()[0][0])
                if Time - int(message.date.timestamp()) < 1 or chatid == userid:
                    cur.execute("UPDATE Game set Shaking = True WHERE IDChat = %i" % chatid)
                    conn.commit()
                    name = message.from_user.first_name
                    await shake(name, userid, chatid)

                    cur.execute("DELETE FROM GAME WHERE IDChat = %i" % chatid)
                    conn.commit()
                else:
                    mmes = await message.answer("Бросить можно через %s сек" %
                                                str(Time - int(message.date.timestamp())))
                    await to_del_mess(chatid, mmes.message_id)

            except Exception as e:
                conn.rollback()
                print(e)

        if Shake is False and shaking is False:
            mes = await message.reply("Сначала сделай ставку")
            await to_del_mess(chatid, mes.message_id)


# ПРОВЕРКА НА СТАВКУ
@dp.message_handler(regexp="(\d[' ']\d)$")
@dp.message_handler(regexp="(\d[ ]\d[-]\d)$")
async def chekbet(message: types.Message):
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await message.reply("Oops, something went wrong")
    else:
        if Shaking:
            if len(message.text.split()) == 2 and Shaking[0][0] is False:
                fullname = message.from_user.full_name
                username = message.from_user.username
                userid = message.from_user.id
                await User(fullname, username, userid, chatid).add_user_data()

                await Bets(message.text, fullname, username, userid, chatid).bet_check()


# processing callback
@dp.callback_query_handler(lambda call: call.data == '1' or call.data == '2' or call.data == '3' or call.data == '3'
                                        or call.data == '4' or call.data == '5' or call.data == '6'
                                        or call.data == '1-3' or call.data == '4-6' or call.data == '1-2'
                                        or call.data == '3-4' or call.data == '5-6')
# @dp.throttled(trottled, rate=1.2)
async def process_callback_game_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await bot.send_message(chatid, "Oops, something went wrong")
    else:
        if Shaking:
            if Shaking[0][0] is False:
                userid = callback_query.from_user.id
                fullname = callback_query.from_user.full_name
                username = callback_query.from_user.username
                await User(fullname, username, userid, chatid).add_user_data()

                text = f'5 {callback_query.data}'
                await Bets(text, fullname, username, userid, chatid).bet_check()
                await bot.answer_callback_query(callback_query.id)


# %п ПОВТОР СТАВОК
@dp.message_handler(text='%п')
async def repeat_bet(message):
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await message.reply("Oops, something went wrong")
    else:
        if Shaking:
            if Shaking[0][0] is False:
                userid = message.from_user.id
                fullname = message.from_user.full_name
                username = message.from_user.username
                await User(fullname, username, userid, chatid).add_user_data()
                text = ' '
                await Bets(text, fullname, username, userid, chatid).repeat_bet(message)


# %у УДВОИТЬ ВСЕ СТАВКИ
@dp.message_handler(text='%у')
async def double_bet(message):
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await message.reply("Oops, something went wrong")
    else:
        if Shaking:
            if Shaking[0][0] is False:
                userid = message.from_user.id
                fullname = message.from_user.full_name
                username = message.from_user.username
                await User(fullname, username, userid, chatid).add_user_data()
                text = ' '
                await Bets(text, fullname, username, userid, chatid).double_bet(message)


@dp.message_handler(lambda message: message.text.lower() == 'ставки')
async def user_bets(message):
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await message.reply("Oops, something went wrong")
    else:
        if Shaking:
            if Shaking[0][0] is False:
                fullname = message.from_user.full_name
                username = message.from_user.username
                userid = message.from_user.id
                await User(fullname, username, userid, chatid).add_user_data()
                await User(fullname, username, userid, chatid).user_bets(message)


# canceling all user bets
@dp.message_handler(lambda msg: msg.text.lower() == 'отмена')
async def cancelbets(message):
    chatid = message.chat.id
    #    ВЫГРУЗКА GAME
    try:
        cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i" % chatid)
        Shaking = cur.fetchall()
    except Exception as e:
        print(e)
        await message.reply("Oops, something went wrong")
    else:
        if Shaking:
            if Shaking[0][0] is False:
                fullname = message.from_user.full_name
                username = message.from_user.username
                userid = message.from_user.id
                await User(fullname, username, userid, chatid).add_user_data()
                await User(fullname, username, userid, chatid).cancel_bets(message)


# all chat logs
@dp.message_handler(lambda msg: msg.text.lower() == 'логи')
async def logsgame(message):
    chatid = message.chat.id

    if message.chat.title is not None:
        title = message.chat.title
    else:
        title = message.chat.first_name
    date = str(datetime.fromtimestamp(message.date.timestamp() + 10800))

    await Chat(chatid, title, date).add_chat_data()

    await Chat(chatid, title, date).logs(message)


#  БАЛАНС ИГРОКА
@dp.message_handler(commands=['lave'])
@dp.message_handler(lambda message: message.text.lower() == 'лавэ')
async def usermoney(message):
    name = message.from_user.full_name
    username = message.from_user.username
    userid = message.from_user.id
    chatid = message.chat.id

    await User(name, username, userid, chatid).add_user_data()

    await User(name, username, userid, chatid).lave(message)


#  users stats
@dp.message_handler(text='!стата')
async def statuser(message):
    chatid = message.chat.id
    if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is False:
        userid = message.reply_to_message.from_user.id
        fullname = message.reply_to_message.from_user.full_name
        username = message.reply_to_message.from_user.username

        cur.execute("SELECT Show_stat FROM Users WHERE UserId = %i" % userid)
        Show_stat = cur.fetchall()[0][0]

        if Show_stat is True or message.from_user.id == 526497876 or message.from_user.id == 547400918:
            await User(fullname, username, userid, chatid).profile(message)

        else:
            await message.reply("На такое лучше не смотреть")

    else:
        userid = message.from_user.id
        fullname = message.from_user.full_name
        username = message.from_user.username
        await User(fullname, username, userid, chatid).profile(message)


@dp.message_handler(text='!стата сбросить')
async def drop_stats(message):
    try:
        if message.text.lower().split()[0] == '!стата' and message.text.lower().split()[1] == "сбросить":
            userid = message.from_user.id
            cur.execute("UPDATE USERS set WON = 0, LOST = 0, Plays = 0 WHERE UserId = %i" % userid)
            await message.answer("Стата сброшена")
    except Exception as e:
        await message.reply("Oops. something went wrong. Try again.")
    else:
        conn.commit()


@dp.message_handler(regexp="!стата сбросить ([0-9]+)")
async def drop_smbdys_stat(message):
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
                cur.execute("SELECT UserId, FullName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    # if top[k][0] != 547400918 and top[k][0] != 526497876:
                    if i[0] == top[k][0]:
                        rate.append(top[k][1:])

            ratesort = sorted(rate, key=lambda money: money[1])[::-1]

            if len(ratesort) <= 30:
                for i in range(len(ratesort)):
                    q += 1
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + await makegoodview(ratesort[i][1]) + '\n'
            else:
                for i in range(30):
                    q += 1
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + await makegoodview(ratesort[i][1]) + '\n'

            await message.answer(topchik)
        except Exception as e:
            await message.reply("Oops, something went wrong")
            print(e)


@dp.message_handler(text='!рейтинг 10')
async def top_10(message):
    if message.chat.id != message.from_user.id:

        try:
            rate = []
            chatid = message.chat.id
            cur.execute("SELECT UserId FROM chatusers WHERE IDChat = %i" % chatid)
            topofchat = cur.fetchall()
            topchik = ""
            q = 0
            for i in topofchat:
                cur.execute("SELECT UserId, FullName, Money FROM USERS ORDER BY Money")
                top = cur.fetchall()
                for k in range(len(top)):
                    # if top[k][0] != 547400918 and top[k][0] != 526497876:
                    if i[0] == top[k][0]:
                        rate.append(top[k][1:])
            ratesort = sorted(rate, key=lambda money: money[1])[::-1]

            if len(ratesort) <= 10:
                for i in range(len(ratesort)):
                    q += 1
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + await makegoodview(ratesort[i][1]) + '\n'
            else:
                for i in range(10):
                    q += 1
                    topchik += str(q) + '. ' + str(ratesort[i][0]) + ' ' + await makegoodview(ratesort[i][1]) + '\n'

            await message.answer(topchik)
        except Exception as e:
            print(e)
            await message.reply("Oops, something went wrong")


# ПЕРЕДАТЬ ДЕНЬГИ
@dp.message_handler(regexp="(^[+][г])([' ']*)(\d)")
async def transfer_money(message):
    try:
        if 0 < int(''.join(message.text[2:].split(','))) < 10 ** 18 and message.reply_to_message is not None:
            name = message.from_user.full_name
            username = message.from_user.username
            userid = message.from_user.id
            chatid = message.chat.id
            await User(name, username, userid, chatid).add_user_data()
            try:

                if message.reply_to_message.from_user.is_bot is False:
                    howmuch = int(''.join(message.text[2:].split(',')))
                    whoid = message.reply_to_message.from_user.id
                    whoname = message.reply_to_message.from_user.full_name
                    whousername = message.reply_to_message.from_user.username
                    if userid != whoid:
                        await User(whoname, whousername, whoid, chatid).add_user_data()
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
        elif 10 ** 18 < int(''.join(message.text[2:].split(','))):
            await message.reply("Передать можно не больше 1,000,000,000,000,000,000 за раз")
    except Exception:
        await message.reply("Не удалось передать деньги")


@dp.message_handler(commands=['bonuslave'])
@dp.message_handler(lambda message: message.text.lower() == 'бонус')
async def bonus(message):
    chatid = message.chat.id
    fullname = message.from_user.full_name
    bonuserid = message.from_user.id
    username = message.from_user.username

    await User(fullname, username, bonuserid, chatid).add_user_data()
    await Bonus(fullname, bonuserid, chatid).bonus(message)


#  processing bonus callback
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить')
@dp.throttled(bonus_throttled, rate=0.7)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    fullname = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    await Bonus(fullname, userid, chatid).click_1(mesid, callback_query)


#  processing bonus second click step callback  --> def coef()
@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить1')
@dp.throttled(bonus_throttled, rate=0.7)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    fullname = callback_query.from_user.first_name
    mesid = callback_query.message.message_id

    await Bonus(fullname, userid, chatid).click_2(mesid, callback_query)


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'Бросить2')
@dp.throttled(bonus_throttled, rate=0.7)
async def process_callback_bonus_buttons(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    fullname = callback_query.from_user.first_name
    mes_id = callback_query.message.message_id

    await Bonus(fullname, userid, chatid).click_3(mes_id, callback_query)


@dp.message_handler(regexp='!раздача ([0-9]+)')
async def giveaway(message):
    if message.text[:8] == '!раздача':
        userid = message.from_user.id
        chatid = message.chat.id
        # if userid != chatid:                      #TODO
        try:
            cur.execute(f"SELECT Giveaway_time FROM Users WHERE UserId = {userid}")
            time_for_giveaway = int(cur.fetchall()[0][0])
        except Exception as e:
            print(e)
        else:
            if int(message.date.timestamp()) > time_for_giveaway or time_for_giveaway == 0:
                if 100000 <= int(message.text.split()[1]) <= 500 * 10**9:
                    created = await create_db(chatid)
                    if created == 0:
                        pass
                    else:
                        await start_giveaway(message)

                else:
                    await message.reply("Минимальная сумма для раздачи 100 000\n"
                                        "Максимальная - 500 миллиардов")
            else:
                await message.reply("Устраивать раздачу можно раз в 1 час")


@dp.callback_query_handler(lambda call_bonus: call_bonus.data == 'раздача')
@dp.throttled(rate=1.3)
async def scores(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    userid = callback_query.from_user.id
    fullname = callback_query.from_user.full_name
    username = callback_query.from_user.username

    try:
        cur.execute(f"SELECT UserId FROM GIVEAWAY{abs(chatid)} WHERE How_many IS NOT NULL")
        not_for_him = cur.fetchall()[0][0]
        if userid != not_for_him:
            await User(fullname, username, userid, chatid).add_user_data()
            cur.execute(f"SELECT count(Value) FROM GIVEAWAY{abs(chatid)} WHERE UserId = {userid}")
            to_count = int(cur.fetchall()[0][0])
            if to_count == 1:
                cur.execute(f"UPDATE GIVEAWAY{abs(chatid)} set Value = Value + 1 WHERE UserId = {userid}")
                conn.commit()
            elif to_count < 1:
                cur.execute(f"INSERT INTO GIVEAWAY{abs(chatid)} (FullName, UserId, Value)"
                            f" VALUES ('{fullname}', {userid}, 1)")
                conn.commit()
            await bot.answer_callback_query(callback_query.id)
        else:
            await bot.answer_callback_query(callback_query.id, "Ты организатор")
    except Exception:
        pass


@dp.errors_handler(exception=TelegramAPIError)
async def error_handler(update, e):
    print(e)
    return True
