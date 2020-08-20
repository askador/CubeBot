# coding=utf-8

import asyncio
from misc import bot, cur, conn
from handlers.add_func import makegoodview
from handlers.achievements import check_limit_money, achieves_plays, achievs_balance, max_win
from numpy import random

bonus_gif = 'CAACAgIAAxkBAAJZsF7ayGQo1aCENzBjuSqMjH-LIrhZAAIHAANUuGEf5o6jSM3m8uIaBA'


#  start shaking  --> endgame
async def shake(name, userid, chatid):
    # deleting all messages from bot in game
    cur.execute("SELECT MessId FROM ToDelMes WHERE IDChat = '%i'" % chatid)
    messid = cur.fetchall()

    for i in range(len(messid)):
        try:
            await bot.delete_message(chatid, messid[i][0])
        except Exception as e:
            pass
    cur.execute("DELETE FROM todelmes where idchat = '%i'" % chatid)
    conn.commit()

    mes1 = await bot.send_message(chatid, "<a href='tg://user?id=%i'>%s</a> бросает кубик" % (userid, name))

    # animation and processing all bets
    await asyncio.sleep(5)

    try:
        await bot.delete_message(chatid, mes1.message_id)
    except Exception as e:
        pass

    #   ВЫГРУЗКА ВСЕХ СТАВОК
    await endgame(chatid)


async def endgame(chatid):
    list_of_plays = []
    list_of_names = {}
    Wonmaxnum = []

    # ВСЕ СТАВКИ
    Fstat = ''
    WINstat = ''
    ALLwins = 0
    Lose = 0

    # processing previous bets of user
    cur.execute("SELECT UserId FROM BETS WHERE IDChat = %i AND Bet > 0" % chatid)
    Usids = cur.fetchall()
    for ids in Usids:
        cur.execute("DELETE FROM PREVBETS WHERE UserId = %i AND IDChat = %i" % (ids[0], chatid))
        # conn.commit()

    # logchat
    namedb = 'logchat' + str(abs(chatid))

    # Выбор кубика (бонусный, обычный)
    key = random.choice([1, 2], p=[0.98, 0.02])

    cur.execute("SELECT UserId FROM bets WHERE IDChat = %i" % chatid)
    not_bonus = cur.fetchall()
    for i in list(set(not_bonus)):
        if not_bonus.count(i) >= 6:
            key = 1

    if key == 1:
        dice_mes = await bot.send_dice(chatid)
        Numbers = dice_mes.dice.value
        cur.execute("INSERT INTO %s (Log) VALUES (%i)" % (namedb, Numbers))

    elif key == 2:
        await bot.send_animation(chatid, bonus_gif)
        cur.execute("INSERT INTO %s (Log) VALUES ('%s')" % (namedb, "Бонус"))

    cur.execute("SELECT count(Id) FROM %s" % namedb)
    log = cur.fetchall()
    if log[0][0] > 9:
        cur.execute("DELETE FROM %s WHERE Id <= (SELECT MAX(Id) FROM %s) - 10" % (namedb, namedb))
        # conn.commit()

    # processing all bets
    cur.execute("SELECT Id FROM BETS WHERE IDChat = %i AND Bet > 0" % chatid)
    IDs = cur.fetchall()
    for uid in IDs:
        cur.execute("SELECT UserId, Bet, Numbers FROM BETS WHERE Id = %i" % uid)
        ALLBets = cur.fetchall()

        UsId = ALLBets[0][0]
        UsBet = str(ALLBets[0][1])
        UsNum = str(ALLBets[0][2])

        # adding to repeat bet
        # try:
        if len(UsNum) == 3:
            UsNum1 = str(UsNum.split('-')[0] + UsNum.split('-')[1])
            cur.execute("INSERT INTO PREVBETS (UserId, Bet, Numbers, IDChat) VALUES (%i, %s, %s, %i)" %
                        (UsId, UsBet, UsNum1, chatid))
            # conn.commit()
        elif len(UsNum) == 1:
            cur.execute("INSERT INTO PREVBETS (UserId, Bet, Numbers, IDChat) VALUES (%i, %s, %s, %i)" %
                        (UsId, UsBet, UsNum, chatid))
            # conn.commit()

        cur.execute("SELECT FullName FROM USERS WHERE UserId = %i" % UsId)
        Names = str(cur.fetchall()[0][0])

        #  Для статистики
        list_of_plays.append(UsId)
        list_of_names.update([(UsId, Names)])

        #   ВСЕ СТАВКИ
        Fstat += Names + ' ' + await makegoodview(str(UsBet)) + ' на ' + UsNum + '\n'

        if key == 1:
            # ВЫИГРАЛИ  1000 2-4
            try:
                if len(UsNum.split('-')) == 2:
                    if int(UsNum.split('-')[0]) <= Numbers <= int(UsNum.split('-')[1]):
                        Prize = int(int(UsBet) * 6 / (int(UsNum[2]) - int(UsNum[0]) + 1))
                        ALLwins += 1

                        cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = '%i'" % (Prize, UsId))
                        cur.execute(
                            "UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (
                                int(int(Prize) - int(UsBet)), UsId))
                        # conn.commit()

                        WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                                   " заработал " + await makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

                        Wonmaxnum.append(await max_win(UsId, Prize))

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
                    # conn.commit()

                    WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                               " заработал " + await makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

                    Wonmaxnum.append(await max_win(UsId, Prize))
            except Exception as e:
                pass

            # LOST
            try:
                if int(UsNum) != Numbers:
                    Lose += 1
                    cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                    # conn.commit()
            except Exception as e:
                pass
            try:
                if int(UsNum.split('-')[1]) < Numbers or Numbers < int(UsNum.split('-')[0]):
                    Lose += 1
                    cur.execute("UPDATE USERS set LOST = LOST + %i WHERE UserId = %i" % (int(UsBet), UsId))
                    # conn.commit()
            except Exception as e:
                pass

        elif key == 2:
            Prize = int(int(UsBet) * 3)
            ALLwins += 1

            cur.execute("UPDATE USERS set Money = Money + %i WHERE UserId = %i" % (Prize, UsId))

            cur.execute(
                "UPDATE USERS set WON = WON + %i WHERE UserId = '%i'" % (int(int(Prize) - int(UsBet)), UsId))

            WINstat += "💰<a href='tg://user?id=%i'>%s</a>" % (UsId, Names) + \
                       " заработал " + await makegoodview(Prize) + ' грывень на ' + UsNum + "\n"

            Wonmaxnum.append(await max_win(UsId, Prize))

        await check_limit_money(UsId)



    # update plays stats
    list_of_plays = list(set(list_of_plays))
    for i in range(len(list_of_plays)):
        cur.execute("UPDATE USERS set Plays = Plays + 1 WHERE UserId = %i" % list_of_plays[i])
        # achievements
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

    try:
        for h in range(len(Wonmaxnum)):
            titleV = Wonmaxnum[h][0]
            moniV = Wonmaxnum[h][1]
            useridV = Wonmaxnum[h][2]
            await bot.send_message(chatid, f"⭐️ {list_of_names[useridV]} получает достижение "
                                           f"\n<b>{titleV}</b>\n"
                                           f"Держи награду +{moniV}")
    except Exception:
        pass

    if WINstat == '':
        WINstat = 'Вах, никто нэ выиграл'

    await asyncio.sleep(3)

    if key == 1:
        await bot.send_message(chatid, "🎲  %s\nСтавки:\n%s \n%s" % (Numbers, Fstat, WINstat))
    elif key == 2:
        await bot.send_message(chatid, "🏵  %s\nСтавки:\n%s \n%s" % ('Бонус', Fstat, WINstat))

    conn.commit()

    #   STOP GAME
    cur.execute("DELETE FROM BETS WHERE IDChat = %i" % chatid)
    conn.commit()