# coding=utf-8
import asyncio

from misc import conn, cur, bot
from handlers.shake import endgame


async def game_autostart(chatid, id_game):
    delay = 300
    await asyncio.sleep(delay)
    cur.execute("SELECT Shaking FROM GAME WHERE IDChat = %i"
                " AND Id = %i AND Shaking = False" % (chatid, id_game))
    data = cur.fetchall()
    if data:
        if data[0][0] is False:
            cur.execute("UPDATE Game set Shaking = True")
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

            await endgame(chatid)

            # Clearing bets table
            cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
            conn.commit()

            #   STOP GAME
            cur.execute("DELETE FROM GAME WHERE IDChat = %i" % chatid)
            conn.commit()


async def bonus_autostart(name, userid, chatid):
    delay = 240

    await asyncio.sleep(delay)
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
            except Exception as e:
                print(e)
            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (lave[0][0], userid))
            conn.commit()

    except Exception:
        pass
