# coding=utf-8
from aiogram import types
import asyncio
from datetime import datetime

from data.misc import conn, cur, bot
from utils.add_func import makegoodview


async def create_db(chatid):
    try:
        cur.execute(f"CREATE TABLE GIVEAWAY{abs(chatid)}("
                    "Id Serial,"
                    "UserId              BIGINT,"
                    "How_many            BIGINT,"
                    "FullName              TEXT,"
                    "value                  INT,"
                    "Time                BIGINT,"
                    "mes_id                 INT,"
                    "PRIMARY KEY(Id));")
    except Exception as e:
        try:
            cur.execute(f"SELECT TIME FROM GIVEAWAY{abs(chatid)}")
            time = cur.fetchall()
            if time:
                return 1
            else:
                return 0
        except Exception as e:

            return 0
    else:
        conn.commit()
        return 1


async def start_giveaway(message):
    userid = message.from_user.id
    fullname = message.from_user.full_name
    chatid = message.chat.id
    date = int(message.date.timestamp())
    how_much = int(message.text.split()[1])

    giveaway_bt = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='+ 1🏅', callback_data="раздача")
    giveaway_bt.add(button)

    timer = 2.5 * 60

    cur.execute(f"INSERT INTO GIVEAWAY{abs(chatid)} (UserId, How_many, FullName, Time)"
                f" Values ('{userid}', '{how_much}', '%s', %i)" % (fullname, timer))
    conn.commit()

    cur.execute(f"UPDATE USERS SET Giveaway_time = '{int(date) + 3598}', "
                f"Money = Money - {how_much} "
                f"WHERE UserId = {userid}")
    conn.commit()

    giveaway_mes = await message.answer(f"<a href='tg://user?id={userid}'>{fullname}</a> "
                                        f"устраивает раздачу лавэ {await makegoodview(how_much)}\n"
                                        f"\n"
                                        f"Нажимайте на кнопку, набирайте больше всех очков\n"
                                        f"Награда распределится по количеству набранных очков\n"
                                        f"Раздача лавэ через 02:30",
                                        reply_markup=giveaway_bt)
    mes_id = giveaway_mes.message_id

    cur.execute(f"UPDATE GIVEAWAY{abs(chatid)} SET mes_id = {mes_id} WHERE UserId = {userid}")
    conn.commit()

    Loop = asyncio.get_event_loop()
    Loop.create_task(giveaway_timer(mes_id, userid, chatid))


async def giveaway_timer(give_mes_id, userid, chatid):
    cur.execute(f"SELECT FullName FROM GIVEAWAY%s WHERE UserId = %s" % (abs(chatid), userid))
    starter = str(cur.fetchall()[0][0])

    cur.execute(f"SELECT How_many From GIVEAWAY{abs(chatid)} WHERE UserId = {userid}")
    how_many_proc = int(cur.fetchall()[0][0])

    while True:
        cur.execute("SELECT Time FROM GIVEAWAY%s WHERE UserId = %i" % (abs(chatid), userid))
        start_in = cur.fetchall()[0][0]
        # except Exception:
        #     try:
        #         cur.execute("UPDATE GIVEAWAY%s set Time = Time - 3 WHERE UserId = %s" % (abs(chatid), userid))
        #     except Exception:
        #         pass
        #     else:
        #         conn.commit()
        # else:
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
            f"устраивает раздачу лавэ {await makegoodview(how_many_proc)}\n"
            f"Правила:\n"
            f"Нажимайте на кнопку, набирайте больше всех очков\n"
            f"Награда распределится по количеству набранных очков\n"
            f"Раздача лавэ через {datetime.fromtimestamp(start_in).strftime('%M:%S')}"
            f"\n\n"
            f"{list_for_giveaway}", reply_markup=giveaway_bt_procc)

        except Exception:
            pass
        finally:
            cur.execute("UPDATE GIVEAWAY%s set Time = Time - 3 WHERE UserId = %s" % (abs(chatid), userid))
            conn.commit()
            await asyncio.sleep(3)
        if start_in < 4:
            await final(chatid, give_mes_id, how_many_proc, userid, starter)
            break


async def final(chatid, give_mes_id, how_many_proc, userid, starter):
    try:
        await bot.delete_message(chatid, give_mes_id)
    except Exception as e:
        pass

    await asyncio.sleep(1)

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
                          str(await makegoodview(money)) + '\n'

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
