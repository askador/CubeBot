# coding=utf-8
import random
import numpy as np
import asyncio
from datetime import datetime
from aiogram import types

from utils.autostart import bonus_autostart
from data.misc import conn, cur, bot
from utils.achievements import achieves_bonus, check_limit_money


class Bonus:
    def __init__(self, fullname, userid, chatid):
        self.fullname = fullname
        self.userid = userid
        self.chatid = chatid

    async def coef(self, num, userid, is_line=False):
        if num == '1':
            if is_line is False:
                mnozitel = 1.5
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                mnozitel2 = 25
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel2
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
        if num == '2':
            if is_line is False:
                mnozitel = 2.3
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                mnozitel2 = 28
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel2
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
        if num == '3':
            if is_line is False:
                mnozitel = 3.1
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                mnozitel2 = 33
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel2
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
        if num == '4':
            if is_line is False:
                mnozitel = 3.9
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                mnozitel2 = 38
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel2
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
        if num == '5':
            if is_line is False:
                mnozitel = 4.7
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                if is_line is False:
                    mnozitel2 = 45
                    cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                    cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                    paluchi5 = cur.fetchall()[0][0]
                    paluchi5 = paluchi5 * mnozitel2
                    cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                    conn.commit()
        if num == '6':
            if is_line is False:
                mnozitel = 5.5
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel, userid))
                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()
            else:
                mnozitel2 = 50
                cur.execute("UPDATE BONUS set BONCOEF = %f WHERE UserId = %i" % (mnozitel2, userid))

                cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % userid)
                paluchi5 = cur.fetchall()[0][0]
                paluchi5 = paluchi5 * mnozitel2
                cur.execute("UPDATE BONUS set LAVE = %i WHERE UserId = %i" % (paluchi5, userid))
                conn.commit()

    async def bonus(self, message):
        try:
            cur.execute("SELECT BONUSTIME FROM USERS WHERE UserId = %s" % self.userid)
            bonustime = int(cur.fetchall()[0][0])
        except Exception as e:
            await message.reply("Oops, something went wrong")
            pass
        else:
            ostalos = bonustime - int(message.date.timestamp())

            if self.userid != 526497876 and self.userid != 547400918 and ostalos > 0:
                value = datetime.fromtimestamp(ostalos).strftime('%H:%M:%S')
                await message.reply("Бонусное лавэ можно получить через %s" % value)

            elif self.userid == 526497876 or self.userid == 547400918 or bonustime == 0 or ostalos <= 0:
                keybonus = types.InlineKeyboardMarkup()
                bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить")
                keybonus.add(bonusik)

                cur.execute("SELECT Money From USERS Where UserId = %i" % self.userid)
                money = cur.fetchall()[0][0]
                if money > 100000000:  # 100 000 000
                    lavebonus = int(random.randrange(15000, 25000))
                else:
                    lavebonus = int(random.randrange(1500, 2500))

                numbonus = ''.join([str(np.random.randint(1, 7, 1)[0]) for i in range(3)])

                cur.execute("DELETE FROM BONUS WHERE USERID = %s" % self.userid)
                conn.commit()

                cur.execute(
                    "INSERT INTO BONUS (UserId, BONCOEF, BONNUMS, LAVE, START_LAVE, IDChat) "
                    "VALUES (%i, 1, %s, %i, %i, %i)"
                    % (self.userid, numbonus, lavebonus, lavebonus, self.chatid))
                conn.commit()

                bonusmes = await message.answer("<a href='tg://user?id=%i'>%s</a> бросай кубики\nУвеличивай бонус\n\n"
                                                "Лавэ %i, коеффициент = 1.0\n\n"
                                                "           🎲 : 🎲 : 🎲 \n" % (self.userid, self.fullname, lavebonus),
                                                reply_markup=keybonus)

                punkt = int(message.date.timestamp()) + 7200
                cur.execute("UPDATE USERS set BONUSTIME = %i, Bonus_mes_id = '%i' WHERE UserId = %i" %
                            (punkt, bonusmes.message_id, self.userid))
                conn.commit()

                loop_bonus = asyncio.get_event_loop()
                await loop_bonus.create_task(bonus_autostart(self.fullname, self.userid, self.chatid))

    async def click_1(self, mes_id, call):
        keybonus = types.InlineKeyboardMarkup()
        bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить1")
        keybonus.add(bonusik)

        try:
            cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % self.userid)
            user_mes = cur.fetchall()[0][0]
        except Exception as e:
            pass
        else:
            if user_mes == mes_id:
                try:
                    cur.execute("SELECT START_LAVE FROM BONUS WHERE UserId = %i" % self.userid)
                    lave = cur.fetchall()[0][0]

                    cur.execute("SELECT bonnums from bonus where userid = %i" % self.userid)
                    bonnums = cur.fetchall()[0][0]
                except Exception:
                    pass
                else:
                    try:
                        await bot.edit_message_text(chat_id=self.chatid, message_id=user_mes,
                                                    text="<a href='tg://user?id=%s'>%s</a> бросай кубики\n"
                                                         "Увеличивай бонус\n\n"
                                                         "Лавэ %s, коеффициент = %.1f\n\n"
                                                         "             <b>%s</b> : 🎲 : 🎲 \n" %
                                                         (self.userid, self.fullname, lave, 1, bonnums[0]),
                                                    reply_markup=keybonus)
                        await bot.answer_callback_query(call.id)
                    except Exception as e:
                        pass
            else:
                await call.answer("Не твоё")

    async def click_2(self, mes_id, call):
        keybonus1 = types.InlineKeyboardMarkup()
        bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="Бросить2")
        keybonus1.add(bonusik)

        try:
            cur.execute("SELECT Bonus_mes_id FROM USERS WHERE USERID = %i" % self.userid)
            bonususermes = cur.fetchall()[0][0]
        except Exception as e:
            pass
        else:
            if bonususermes == mes_id:
                try:
                    cur.execute("SELECT bonnums from bonus where userid = %i" % self.userid)
                    bonnums = cur.fetchall()[0][0]
                except Exception as e:
                    pass
                else:
                    try:
                        if bonnums[0] == bonnums[1]:
                            await self.coef(bonnums[0], self.userid)

                        cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % self.userid)
                        lave = cur.fetchall()[0][0]

                        cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % self.userid)
                        boncoef = cur.fetchall()[0][0]

                        await bot.edit_message_text(chat_id=self.chatid, message_id=bonususermes,
                                                    text="<a href='tg://user?id=%s'>%s</a> бросай кубики\n"
                                                         "Увеличивай бонус\n\n"
                                                         "Лавэ %s, коеффициент = %.1f\n\n"
                                                         "               <b>%s</b> : <b>%s</b> : 🎲 \n" %
                                                         (self.userid, self.fullname, lave, boncoef, bonnums[0],
                                                          bonnums[1]),
                                                    reply_markup=keybonus1)
                        await bot.answer_callback_query(call.id)
                    except Exception as e:
                        pass

            else:
                await call.answer("Не твоё")

    async def click_3(self, mes_id, call):
        keybonus2 = types.InlineKeyboardMarkup()
        bonusik = types.InlineKeyboardButton(text='Бросить', callback_data="финал")
        keybonus2.add(bonusik)

        try:
            cur.execute("SELECT Bonus_mes_id FROM USERS WHERE UserId = %i" % self.userid)
            bonususermes = cur.fetchall()[0][0]
        except Exception:
            pass
        else:
            if bonususermes == mes_id:

                try:
                    cur.execute("SELECT bonnums from bonus where userid = %i" % self.userid)
                    bonnums = cur.fetchall()[0][0]
                except Exception:
                    pass
                else:
                    try:
                        if bonnums[0] == bonnums[2] or bonnums[1] == bonnums[2] and len(list(set(bonnums))) != 1:
                            await self.coef(bonnums[2], self.userid)

                        if len(list(set(bonnums))) == 1:
                            await self.coef(bonnums[2], self.userid, is_line=True)

                        cur.execute("SELECT LAVE FROM BONUS WHERE UserId = %i" % self.userid)
                        lave = cur.fetchall()[0][0]

                        cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (lave, self.userid))
                        conn.commit()

                        await check_limit_money(self.userid)

                        cur.execute("SELECT BONCOEF FROM BONUS WHERE UserId = %i" % self.userid)
                        boncoef5 = cur.fetchall()[0][0]

                        await bot.edit_message_text(chat_id=self.chatid, message_id=bonususermes,
                                                    text="<a href='tg://user?id=%s'>%s</a> бросай кубики\n"
                                                         "Увеличивай бонус\n\n"
                                                         "Лавэ %s, коеффициент = %.1f\n\n"
                                                         "               <b>%s</b> : <b>%s</b> : <b>%s</b> \n" %
                                                         (self.userid, self.fullname, lave,
                                                          boncoef5, bonnums[0], bonnums[1], bonnums[2]),
                                                    reply_markup=keybonus2)

                        await bot.answer_callback_query(call.id)

                        try:
                            bonus_achievement = await achieves_bonus(bonnums, self.userid)
                            for i in range(len(bonus_achievement)):
                                gift = bonus_achievement[i][1]
                                title = bonus_achievement[i][0]
                                await bot.send_message(self.chatid, f"⭐️ {self.fullname} получает достижение "
                                                                    f"\n<b>{title}</b>\n"
                                                                    f"Держи награду +{gift}")
                        except Exception as e:
                            pass

                        await asyncio.sleep(3)
                        await bot.edit_message_text(chat_id=self.chatid, message_id=bonususermes,
                                                    text="<a href='tg://user?id=%i'>%s</a> забирает свой бонус %s " %
                                                         (self.userid, self.fullname, lave))

                        cur.execute("DELETE FROM BONUS WHERE UserId = %i" % self.userid)
                        conn.commit()
                    except Exception:
                        pass

            else:
                await call.answer("Не твоё")
