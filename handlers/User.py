# coding=utf-8

from misc import conn, cur
from handlers.add_func import makegoodview, to_del_mess


class User:

    def __init__(self, fullname, username, userid, chatid):
        self.fullname = fullname
        self.username = username
        self.userid = userid
        self.chatid = chatid

    async def add_user_data(self):
        #   ДОБАВЛЕНИЕ ИГРОКОВ
        try:
            cur.execute("SELECT Count(UserId) FROM USERS WHERE UserId = '%i'" % self.userid)
            UserdIds = cur.fetchall()[0][0]

            if UserdIds < 1:
                cur.execute("INSERT INTO USERS (FullName, UserName, UserId, Money, Bonustime, "
                            "Lost, Won, Bonus_mes_id, Giveaway_time, Plays, Show_stat) "
                            f"VALUES ('{self.fullname}','{self.username}','{self.userid}', "
                            f"5000, 0, 0, 0, Null, 0, 0, true)")
            if UserdIds > 1:
                cur.execute(
                    "DELETE FROM USERS WHERE Id = (SELECT MAX(ID) FROM USERS WHERE USERID = '%i')" % self.userid)
        except Exception as e:
            pass
        else:
            conn.commit()

        #   ДЛЯ РЕЙТИНГА
        try:
            if self.userid != self.chatid:
                cur.execute("SELECT Count(UserId) FROM chatusers WHERE IDChat = %i AND UserID = %i"
                            % (self.chatid, self.userid))
                UserdIds = cur.fetchall()[0][0]
                if UserdIds < 1:
                    cur.execute("INSERT INTO chatusers (IDChat, UserId) VALUES (%i, %i)" % (self.chatid, self.userid))
        except Exception as e:
            pass
        else:
            conn.commit()

    async def lave(self, message):
        try:
            cur.execute("SELECT Money From USERS Where UserId = '%i'" % self.userid)
            mon = cur.fetchall()[0][0]
            await message.reply("%s грывень" % await makegoodview(mon))
        except Exception as e:
            await message.reply("Oops. something went wrong. Try again.")

    async def profile(self, msg):
        cur.execute("SELECT FullName, Money, Won, Lost, plays FROM Users WHERE UserId = %i" % self.userid)
        usstat = cur.fetchall()
        cur.execute("SELECT Achieve FROM Achives WHERE UserId = %i" % self.userid)
        achives = cur.fetchall()

        ach = ''
        profile = ''

        try:
            for i in range(len(achives)):
                ach += '\n' + str(achives[i][0])
        except Exception as e:
            pass

        Name = str(usstat[0][0])
        Lave = await makegoodview(usstat[0][1])
        Won = await makegoodview(str(usstat[0][2]))
        Lost = await makegoodview(str(usstat[0][3]))
        Plays = usstat[0][4]

        profile += "<b>Имя: </b>%s\n" \
                   "<b>Лавэ: </b>%s\n" \
                   "<b>Выиграно: </b>%s\n" \
                   "<b>Проиграно: </b>%s\n" \
                   "<b>Игр сыграно: </b>%s\n" \
                   "<b>Достижения: </b>%s\n" \
                   "\n" \
                   "<b>Id: </b>%i" % (Name, Lave, Won, Lost, Plays, ach, self.userid)
        await msg.answer(profile)

    async def user_bets(self, msg):
        cur.execute("SELECT Bet FROM BETS WHERE UserId = %i AND IDChat = %i AND Bet != 0" % (self.userid, self.chatid))
        allbets = cur.fetchall()

        cur.execute("SELECT FullName FROM USERS WHERE UserId = %i" % self.userid)
        Name = str(cur.fetchall()[0][0])
        Stavki = ''

        try:
            if allbets:
                cur.execute("SELECT Numbers FROM BETS WHERE UserId = %i AND IDChat = %i AND Bet != 0" %
                            (self.userid, self.chatid))
                allnums = cur.fetchall()
                for i in range(len(allbets)):
                    bets = str(allbets[i][0])
                    nums = str(allnums[i][0])
                    if nums[0] == "с":
                        Stavki += await makegoodview(bets) + ' грыв на сумму ' + nums[1:] + '\n'
                    else:
                        Stavki += await makegoodview(bets) + ' грыв на ' + nums + '\n'
                us_bets = await msg.answer("Ставочки %s:\n%s" % (Name, Stavki))
                await to_del_mess(self.chatid, us_bets.message_id)
            else:
                us_bets = await msg.answer("%s, ставок нет" % Name)
                await to_del_mess(self.chatid, us_bets.message_id)
        except Exception as e:
            await msg.reply("Oops. something went wrong. Try again.")

    async def cancel_bets(self, msg):
        cur.execute("SELECT count(Bet) FROM BETS WHERE UserId = %i AND IDChat = %i" % (self.userid, self.chatid))
        useringame = cur.fetchall()[0][0]
        if useringame > 0:
            name = msg.from_user.first_name
            chatid = msg.chat.id
            cur.execute("SELECT Bet FROM BETS WHERE UserId = %i AND IDChat = %i" % (self.userid, chatid))
            Bet = cur.fetchall()
            cur.execute("SELECT Numbers FROM BETS WHERE UserId = %i AND IDChat = %i" % (self.userid, chatid))
            Num = cur.fetchall()
            try:
                if Bet != [] and Num != []:
                    cur.execute("DELETE FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (self.userid, chatid))
                    for i in range(len(Bet)):
                        cur.execute(
                            "UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Bet[i][0], self.userid))
                        conn.commit()
                    cancel = await msg.reply("<a href='tg://user?id=%i'>%s</a> отменил ставки" % (
                        self.userid, name))
                    await to_del_mess(self.chatid, cancel.message_id)
                else:
                    cancel = await msg.reply("Отменять нечего")
                    await to_del_mess(self.chatid, cancel.message_id)
            except Exception as e:
                await msg.reply("Oops. something went wrong. Try again.")

