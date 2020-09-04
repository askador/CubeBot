# coding=utf-8

import asyncio
from data.misc import cur, conn, days, bot, dp
from utils.autostart import *
from utils.giveaway_start import giveaway_timer


async def loop_checking_bets():
    cur.execute("SELECT IDChat FROM GAME WHERE Shaking = False")
    idchats = cur.fetchall()
    for i in range(len(idchats)):
        chatid = idchats[i][0]
        from utils.bets import checking_bets

        checking = asyncio.get_event_loop()
        checking.create_task(checking_bets(chatid))


async def loop_bonus_close():
    cur.execute("SELECT Id FROM Bonus")
    Id = cur.fetchall()
    for i in range(len(Id)):
        try:
            cur.execute("SELECT UserId FROM Bonus WHERE Id = %i" % Id[i][0])
            userid = cur.fetchall()[0][0]

            cur.execute("SELECT IDChat FROM Bonus WHERE UserId = %i" % userid)
            chatid = cur.fetchall()[0][0]

            cur.execute("SELECT FullName FROM USERS WHERE UserId = %i" % userid)
            name = cur.fetchall()[0][0]

            loop_bonus = asyncio.get_event_loop()
            loop_bonus.create_task(bonus_autostart(name, userid, chatid))
        except Exception as e:
            pass


async def loop_game_autostart():
    cur.execute("SELECT Time FROM Game WHERE Shaking = False")
    Time = cur.fetchall()
    a = len(Time)
    for i in range(a):
        try:
            cur.execute("SELECT IDChat FROM GAME WHERE Time = %i" % Time[i][0])
            chatid = cur.fetchall()[0][0]

            cur.execute("SELECT Id FROM GAME WHERE Time = %i AND IDChat = %i" % (Time[i][0], chatid))
            id_game = cur.fetchall()[0][0]

            loop_game = asyncio.get_event_loop()
            loop_game.create_task(game_autostart(chatid, id_game))
        except Exception as e:
            print(e, 51)


async def loop_shaking():
    cur.execute("SELECT IDChat FROM GAME WHERE Shaking = True")
    is_shacking_chatid = cur.fetchall()
    for i in range(len(is_shacking_chatid)):
        from utils.shake import endgame
        import datetime
        # from misc import days
        time = int(datetime.datetime.now().timestamp()) + 10800
        date = str(datetime.datetime.fromtimestamp(time)).split()[0].split('-')
        weekday = str(days[str(datetime.datetime.fromtimestamp(time).weekday())])
        day = date[2]
        month = date[1]
        year = date[0][2:]
        day = weekday + ' ' + day + '/' + month + '/' + year
        shaking = asyncio.get_event_loop()
        shaking.create_task(endgame(is_shacking_chatid[i][0], day))
        cur.execute("DELETE FROM GAME WHERE IDChat = %i" % is_shacking_chatid[i][0])
        cur.execute("DELETE FROM BETS WHERE IDChat = %i" % is_shacking_chatid[i][0])
        conn.commit()


async def loop_giveaway():
    cur.execute("SELECT table_name FROM information_schema.tables")
    tables = cur.fetchall()
    for table in tables:
        if str(table[0])[:8] == "giveaway":
            chatid = -int(table[0][8:])
            cur.execute(f"SELECT userid FROM {table[0]} WHERE Value is NULL")
            userid = cur.fetchall()[0][0]
            cur.execute(f"SELECT mes_id FROM {table[0]} WHERE VALUE is NULL")
            mes_id = cur.fetchall()[0][0]

            if mes_id is not None:
                Loop = asyncio.get_event_loop()
                Loop.create_task(giveaway_timer(mes_id, userid, chatid))
            else:
                cur.execute(f"DROP TABLE {table[0]}")
                conn.commit()


async def all_loops(dp):
    await bot.send_message(-443076596, "Запуск. . .")
    general = asyncio.get_event_loop()

    general.create_task(loop_game_autostart())
    general.create_task(loop_shaking())
    general.create_task(loop_checking_bets())
    general.create_task(loop_bonus_close())
    general.create_task(loop_giveaway())