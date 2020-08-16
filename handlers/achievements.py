# coding=utf-8

from misc import conn, cur


async def achievs_balance(userid):
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
    if money > 999_999_999_999_999_999:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Буржуй'" % userid)
        sixnine = cur.fetchall()
        if not sixnine:
            mess.append(["Покоритель вершин 🏔", "1 000 000 000 000 000 001"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Покоритель вершин 🏔')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000000000001 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def achieves_plays(userid):
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
        "ПРОВИ?ЗОР"
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
    if plays >= 2000:
        "Хранитель🔮"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Хранитель🔮'" % userid)
        chran = cur.fetchall()
        if not chran:
            mess.append(['Хранитель🔮', "1 000 000 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Хранитель🔮')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000000 WHERE UserId = %i" % userid)
            conn.commit()
    if plays >= 5000:
        "Вне досегаемости"
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Вне досегаемости'" % userid)
        fivethousand = cur.fetchall()
        if not fivethousand:
            mess.append(['Вне досегаемости', "1 000 000 000 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Вне досегаемости')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000000000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def achieves_bonus(bonnums, userid):
    mess = []
    if len(set(bonnums)) == 1 and bonnums[0] != '6':
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Везунчик'" % userid)
        lucker = cur.fetchall()
        if not lucker:
            mess.append(["Везунчик", "1 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Везунчик')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000 WHERE UserId = %i" % userid)
            conn.commit()

    if len(set(bonnums)) == 1 and bonnums[0] == '6':
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Адский покровитель🔥'" % userid)
        hell = cur.fetchall()
        if not hell:
            mess.append(['Адский покровитель🔥', "6 666 666 666"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Адский покровитель🔥')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 6666666666 WHERE UserId = %i" % userid)
            conn.commit()

        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Везунчик'" % userid)
        lucker = cur.fetchall()
        if not lucker:
            mess.append(["Везунчик", "1 000 000"])
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Везунчик')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 1000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def max_win(userid, prize):
    # "Волк с Уолл-стрит"
    mess = []
    if prize >= 10 ** 12:
        cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Волк с Уолл-стрит'" % userid)
        maxwin = cur.fetchall()
        if not maxwin:
            mess = ['Волк с Уолл-стрит', "500 000 000 000", userid]
            cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES(%i, 'Волк с Уолл-стрит')" % userid)
            conn.commit()
            cur.execute("UPDATE USERS set Money = Money + 500000000000 WHERE UserId = %i" % userid)
            conn.commit()
    return mess


async def check_limit_money(userid):
    userid = int(userid)
    try:
        cur.execute("SELECT Money FROM USERS WHERE UserId = '%i'" % userid)
        money = cur.fetchall()[0][0]
    except Exception as e:
        pass
    else:
        if money > 10**35:
            cur.execute("UPDATE USERS SET MONEY = %i WHERE USERID = %i" % (999999999999999999999999999999999, userid))
            conn.commit()
            cur.execute("SELECT Achieve from Achives WHERE UserId = %i AND Achieve = 'Плутос👑'" % userid)
            god = cur.fetchall()
            if not god:
                achieve = "Плутос👑"
                cur.execute("INSERT INTO Achives (UserId, Achieve) VALUES (%i, '%s')" % (userid, achieve))
                conn.commit()
        if money < 0:
            cur.execute("UPDATE USERS SET MONEY = 0 WHERE USERID = %i" % userid)
            conn.commit()
