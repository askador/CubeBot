# coding=utf-8

import asyncio
from misc import conn, cur, bot
from handlers.add_func import to_del_mess, makegoodview
from handlers.achievements import check_limit_money


class Bets:
    def __init__(self, text, fullname, username, userid, chatid):
        self.fullname = fullname
        self.username = username
        self.userid = userid
        self.chatid = chatid
        self.text = text

    async def bet_check(self):
        # ЕСЛИ ЗАПИСЬ 100 2
        try:
            if (''.join((self.text.split()[0]).split(','))).isdigit() and (self.text.split()[1]).isdigit() \
                    and 0 < int((''.join((self.text.split()[0]).split(','))).isdigit()) < 10 ** 18 \
                    and 0 < int(self.text.split()[1]) <= 6:
                bet = int(''.join((self.text.split()[0]).split(',')))
                num = str(self.text.split()[-1])

                #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % self.userid)
                groshi = cur.fetchall()[0][0]
                if groshi >= bet:
                    await self.confirmbets(num, bet, confirm=True)

                else:
                    await check_limit_money(self.userid)
                    mes1 = await bot.send_message(self.chatid,
                                                  "<a href='tg://user?id=%i'>%s</a>, нету столько" %
                                                  (self.userid, self.fullname))
                    await to_del_mess(self.chatid, mes1.message_id)

        except Exception as e:
            pass

        # ЕСЛИ ЗАПИСЬ 100 2 - 4
        try:
            if (''.join((self.text.split()[0]).split(','))).isdigit() \
                    and 0 < int((''.join((self.text.split()[0]).split(','))).isdigit()) < 10 ** 18 \
                    and (self.text.split()[1].split("-")[0]).isdigit() \
                    and (self.text.split()[1].split("-")[1]).isdigit() \
                    and 0 < (int(self.text.split()[1].split("-")[0])) < (
                    int(self.text.split()[1].split("-")[1])) <= 6:

                bet = int(''.join((self.text.split()[0]).split(',')))
                num = str(self.text.split()[-1])

                #    ПРОВЕРКА НА СОСТОЯТЕЛЬНОСТЬ
                cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % self.userid)
                groshi = cur.fetchall()[0][0]
                if groshi >= bet:
                    await self.confirmbets(num, bet, confirm=True)

                else:
                    await check_limit_money(self.userid)
                    mes1 = await bot.send_message(self.chatid,
                                                  "<a href='tg://user?id=%i'>%s</a>, нету столько" %
                                                  (self.userid, self.fullname))
                    await to_del_mess(self.chatid, mes1.message_id)

        except Exception as e:
            pass

    async def confirmbets(self, num, bet, confirm=False):
        if confirm is True:
            #      ПРОВЕРКА НА ТАКУЮ ЖЕ СТАВКУ
            cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                self.userid, self.chatid))
            UsNum = cur.fetchall()
            if (num,) in UsNum:
                cur.execute(
                    "UPDATE USERS SET FullName = '%s', UserName = '%s' , Money = Money - '%i' "
                    "WHERE UserId = '%i'" % (self.fullname, self.username, bet, self.userid))

                cur.execute(
                    "UPDATE BETS set Bet = Bet + '%i', Showed = False WHERE UserId = '%i' AND IDChat = '%i' "
                    "AND Numbers = '%s'" % (bet, self.userid, self.chatid, num))
                conn.commit()
            else:
                cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat, Showed) "
                            "VALUES ('%i', '%i', '%s', '%i', False)" % (self.userid, bet, num, self.chatid))

                cur.execute(
                    "UPDATE USERS SET FullName = '%s', UserName = '%s' , Money = Money - '%i'"
                    "WHERE UserId = '%i'" % (self.fullname, self.username, bet, self.userid))
                conn.commit()

    async def repeat_bet(self, msg):
        cur.execute(
            "SELECT Bet, Numbers FROM PREVBETS WHERE UserId = %i AND IDChat = %i" % (self.userid, self.chatid))
        prev = cur.fetchall()
        if prev:
            PrevBets = ''
            a = []
            b = []
            cur.execute("SELECT Numbers FROM BETS WHERE UserId = '%i' AND IDChat = %i" % (
                self.userid, self.chatid))
            UsNum = cur.fetchall()
            for i in range(len(prev)):
                Bet = prev[i][0]
                if len(str(prev[i][1])) == 2:
                    Num = str(list(prev[i][1])[0]) + '-' + str(list(prev[i][1])[1])
                else:
                    Num = str(prev[i][1])
                a.append(Num)
                cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % self.userid)
                money = cur.fetchall()[0][0]
                if money >= int(Bet):
                    if (Num,) in UsNum:
                        PrevBets += str(await makegoodview(Bet)) + ' ' + 'на' + ' ' + str(Num) + '\n'
                        b.append(Num)

                        cur.execute(
                            "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                            "AND Numbers = '%s'" % (Bet, self.userid, self.chatid, Num))
                        conn.commit()

                        cur.execute(
                            "UPDATE USERS SET FullName = '%s', UserName = '%s' , Money = Money - '%i'"
                            "WHERE UserId = '%i'" % (self.fullname, self.username, Bet, self.userid))
                        conn.commit()

                    else:
                        PrevBets += str(await makegoodview(Bet)) + ' ' + 'на' + ' ' + str(Num) + '\n'
                        b.append(Num)
                        cur.execute("INSERT INTO BETS (UserId, Bet, Numbers, IDChat, Showed) "
                                    "VALUES ('%i', '%i', '%s', '%i', False)" % (self.userid, Bet, Num, self.chatid))

                        cur.execute(
                            "UPDATE USERS SET FullName = '%s', UserName = '%s' , Money = Money - '%i'"
                            "WHERE UserId = '%i'" % (self.fullname, self.username, Bet, self.userid))
                        conn.commit()

            if a == b:
                bet_mes = await msg.answer("%s повтор с прошлой игры:\n%s" % (self.fullname, PrevBets))
                await to_del_mess(self.chatid, bet_mes.message_id)
            else:
                await check_limit_money(self.userid)
                bet_mes = await msg.answer("%s недостаточно денег на некоторые ставки\n%s" % (
                    self.fullname, PrevBets))
                await to_del_mess(self.chatid, bet_mes.message_id)

    async def double_bet(self, msg):
        cur.execute("SELECT Bet, Numbers FROM BETS WHERE UserId = %i AND IDChat = %i" % (self.userid, self.chatid))
        doub = cur.fetchall()
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % self.userid)
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
                    double += str(await makegoodview(int(Bet1) * 2)) + ' ' + 'на' + ' ' + str(Num1) + '\n'
                    cur.execute(
                        "UPDATE USERS SET FullName = '%s', UserName = '%s' , Money = Money - '%i' "
                        "WHERE UserId = '%i'" % (self.fullname, self.username, Bet1, self.userid))

                    cur.execute(
                        "UPDATE BETS set Bet = Bet + '%i' WHERE UserId = '%i' AND IDChat = '%i' "
                        "AND Numbers = '%s'" % (Bet1, self.userid, self.chatid, Num1))
                    conn.commit()

            if b1 == a1:
                _mes = await bot.send_message(self.chatid, "%s удвоил все ставки\n%s" % (self.fullname, double))
                await to_del_mess(self.chatid, _mes.message_id)
            else:
                await check_limit_money(self.userid)
                _mes = await bot.send_message(self.chatid, "%s не хватает денег на некоторые ставки" % self.fullname)
                await to_del_mess(self.chatid, _mes.message_id)


async def checking_bets(chatid):
    while True:
        cur.execute("SELECT Shake FROM Game WHERE IDChat = %i" % chatid)
        game = cur.fetchall()
        if game:
            await print_bets(chatid)
        else:
            break


async def print_bets(chatid):
    await asyncio.sleep(3)
    cur.execute("SELECT Bet FROM Bets WHERE showed = False")
    not_showed = cur.fetchall()
    if not_showed:
        cur.execute("SELECT UserId FROM BETS WHERE Showed = False AND IDChat = %i" % chatid)
        users = cur.fetchall()
        answ = ''
        for i in range(len(users)):
            userid = users[i][0]
            cur.execute("SELECT Bet, Numbers FROM Bets WHERE UserId = %s AND showed = False"
                        " AND IDChat = %i" % (userid, chatid))
            bets = cur.fetchall()
            bet = bets[0][0]
            num = bets[0][1]

            cur.execute("SELECT FullName FROM Users WHERE UserId = %s" % userid)
            name = cur.fetchall()[0][0]

            answ += "<a href='tg://user?id=%i'>%s</a> поставил %s грывэнь на %s\n" % \
                    (userid, name, await makegoodview(bet), num)

            cur.execute("UPDATE BETS set Showed = True WHERE Bet = %s AND Numbers = '%s' "
                        "AND UserId = %s AND IDChat = %s" % (bet, num, userid, chatid))

        try:
            bet_mes = await bot.send_message(chatid, answ)
            await to_del_mess(chatid, bet_mes.message_id)
        except Exception as e:
            pass






