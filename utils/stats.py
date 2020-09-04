# coding=utf-8
from matplotlib import pyplot as plt

from data.misc import *
from datetime import datetime
from utils.add_func import get_key


async def general_stats(won, lost):
    """
    Всего сыграно (с 22/04/20): 1533
    Коэффициент выигрыша: 0.416
    """

    cur.execute("UPDATE GENERAL_STATS set Plays = Plays + 1, Won = Won + %i, Lost = Lost + %i" %
                (won, lost))
    conn.commit()


async def new_members():
    """
        id          Month        New_players
        1          Nov 2020        42
        2          Dec 2020        44
        3          Jan 2021        37
    """

    cur.execute(f"SELECT count(Month) FROM new_members WHERE Month = '{month}'")
    lines = cur.fetchall()[0][0]
    if lines < 1:
        cur.execute(f"INSERT INTO new_members (Month, New_players) VALUES ('{month}', 1)")
        conn.commit()
    else:
        cur.execute(f"UPDATE new_members SET new_players = new_players + 1 WHERE Month = '{month}'")
        conn.commit()

    # max lines number check
    cur.execute("SELECT count(id) FROM new_members")
    id_number = cur.fetchall()[0][0]
    if id_number > 11:
        cur.execute("DELETE FROM new_members WHERE Id < (SELECT max(id) FROM new_members) - 11")
        conn.commit()


async def daily_plays():
    """

        id          day        plays
        1       Mo 10/02/20     12
        2       Tu 11/02/20     8
        3       We 12/02/20     3

    """
    cur.execute(f"SELECT count(day) FROM daily_plays WHERE day = '{day}'")
    lines = cur.fetchall()[0][0]
    if lines < 1:
        cur.execute(f"INSERT INTO daily_plays (day, plays) VALUES ('{day}', 1)")
        conn.commit()
    else:
        cur.execute(f"UPDATE daily_plays SET plays = plays + 1 WHERE day = '{day}'")
        conn.commit()

    # max lines number check
    cur.execute("SELECT count(id) FROM daily_plays")
    id_number = cur.fetchall()[0][0]
    if id_number > 7:
        cur.execute("DELETE FROM daily_plays WHERE Id = (SELECT max(id) FROM daily_plays) - 7")
        conn.commit()


async def players_activity_per3h():
    """

        id            time              players
        1       18:00-21:00 10/04        4
        2       21:00-00:00 10/04        5
        3       00:00-03:00 11/04       10

    """
    cur.execute(f"SELECT count(time) FROM players_activity WHERE time = '{time}'")
    lines = cur.fetchall()[0][0]
    if lines < 1:
        cur.execute(f"INSERT INTO players_activity (time, players) VALUES ('{time}', 1)")
        conn.commit()
    else:
        cur.execute(f"UPDATE players_activity SET players = players + 1 WHERE time = '{time}'")
        conn.commit()

    # max lines number check
    cur.execute("SELECT count(id) FROM players_activity")
    id_number = cur.fetchall()[0][0]
    if id_number > 16:
        cur.execute("DELETE FROM players_activity WHERE Id = (SELECT max(id) FROM players_activity) - 40")
        conn.commit()


async def graph(names, values, title, graph_name):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor((0.4, 0.4, 0.4))
    ax.set_facecolor((0.5, 0.5, 0.5))
    ax.set_yticks(values)

    plt.title(u'%s' % title, fontsize='20', color='White')

    #  Устанавливаем подписи тиков
    ax.set_xticklabels(names, color=(0.95, 0.95, 0.95))
    ax.set_yticklabels(values, color=(0.95, 0.95, 0.95))

    plt.fill_between(names, values, color='LawnGreen', alpha=0.25)
    plt.plot(names, values, 'LawnGreen')

    plt.xticks(rotation=15)
    plt.grid(True)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.savefig('%s.png' % graph_name, facecolor=fig.get_facecolor(), transparent=True)


async def show_general_stats():
    stat = ''
    # General stats
    cur.execute("SELECT Plays FROM GENERAL_STATS")
    AllPlays = cur.fetchall()[0][0]
    cur.execute("SELECT Won FROM GENERAL_STATS")
    Won = cur.fetchall()[0][0]
    cur.execute("SELECT Lost FROM GENERAL_STATS")
    Lost = cur.fetchall()[0][0]

    try:
        Winfactor = round((int(Won) / int(Lost)), 3)
    except Exception:
        Winfactor = 0
    stat += f"<b>Всего сыграно:</b> {AllPlays}\n" \
            f"<b>Коэффициент выигрыша:</b> {Winfactor}\n\n"

    return stat


async def show_new_members():
    time = int(datetime.now().timestamp()) + 10800
    date = str(datetime.fromtimestamp(time)).split()[0].split('-')
    # Stats for monthly new players
    current = []

    # func for monthly new players stats
    async def month_check():
        line = []
        year = date[0]
        month = f"{months[str(int(date[1]))]} {year}".rstrip('\n')
        current.insert(0, month)

        last = int(await get_key(months, current[-1][:3]))
        year_of_last = int(current[-1][-4:])

        if last == 0:
            for i in range(12):
                month = str(months[str((last - i) % 12)]) + ' ' + str(year_of_last)
                line.insert(0, month)

        else:
            year = str(year_of_last)
            for i in range(12):
                if last - i <= 0:
                    year = str(year_of_last - 1)

                month = str(months[str((last - i) % 12)]) + ' ' + year
                line.insert(0, month)

        return line

    names = []
    values = []
    month_order = await month_check()
    for k in month_order:
        cur.execute(f"SELECT New_players from new_members where month = '{k}'")
        number = cur.fetchall()
        names.append(k)
        if number:
            values.append(int(number[0][0]))
        else:
            values.append(0)

    await graph(names, values, title='Новых игроков', graph_name='new_members')

    photo = open('new_members.png', 'rb')

    return photo


async def show_daily_plays():
    current = []

    async def days_check():
        line = []
        time = int(datetime.now().timestamp()) + 10800
        date = str(datetime.fromtimestamp(time)).split()[0].split('-')
        weekday = str(days[str(int(datetime.fromtimestamp(time).weekday()) + 1)])
        month = date[1]
        year = int(date[0][2:])
        day = f"{weekday} {date[2]}/{month}/{year}".rstrip('\n')
        current.insert(0, day)

        last = int(await get_key(days, current[-1][:3]))
        day_of_last = int(current[-1][4:6])
        month_of_last = int(current[-1][7:9])
        year_of_last = int(current[-1][10:12])

        if day_of_last > 6:
            for i in range(7):
                day_name = str(days[str((last - i) % 7)])
                full_day = day_name + ' ' + str(day_of_last - i).zfill(2) + \
                           '/' + str(month_of_last).zfill(2) + \
                           '/' + str(year_of_last).zfill(2)
                line.insert(0, full_day)

        else:
            if year % 4 == 0:
                days_in_month.update([('2', 29)])
            else:
                days_in_month.update([('2', 28)])

            month = month_of_last
            for j in range(7):
                day_number = (day_of_last - j) % days_in_month[str((int(month_of_last) - 1) % 12)]

                if day_number == 0:
                    day_number = days_in_month[str((int(month_of_last) - 1) % 12)]

                if day_number >= 25:
                    if month_of_last == 1:
                        month = 12
                    else:
                        month = month_of_last - 1

                day_name = str(days[str((last - j) % 7)])
                full_day = day_name + ' ' + \
                           str(day_number).zfill(2) + '/' + \
                           str(month).zfill(2) + '/' + \
                           str(year_of_last).zfill(2)
                line.insert(0, full_day)
        return line

    names = []
    values = []
    plays = await days_check()
    for y in plays:
        cur.execute(f"SELECT plays from daily_plays where day = '{y}'")
        number = cur.fetchall()
        y = y[:-3]
        names.append(y)
        if number:
            values.append(int(number[0][0]))
        else:
            values.append(0)

    await graph(names, values, title='Ежедневные игры', graph_name='days_check')

    photo = open('days_check.png', 'rb')

    return photo


async def show_players_activity():
    async def players_activity():
        time = int(datetime.now().timestamp()) + 10800
        current_time = str(datetime.fromtimestamp(time)).split()
        day_of_last = int(current_time[0].split('-')[2])
        month_of_last = int(current_time[0].split('-')[1])
        year = int(current_time[0].split('-')[0])
        time = current_time[1][:5]
        current_part = 0
        for i in range(16):
            if int(parts[str(i)].split('-')[0][:2]) <= int(time[:2]) < int(parts[str(i)].split('-')[1][:2]):
                current_part = i
                break
        line = []

        if current_part != 0:
            if day_of_last > 1:
                day_number = day_of_last
                for i in range(16):
                    if parts[str((current_part - i) % 8)][-5:-3] == '24':
                        day_number = (int(day_of_last) - 1) % days_in_month[str((int(month_of_last)) % 12)]
                        day_of_last = day_of_last - 1

                    time = parts[str((current_part - i) % 8)] + ' ' + str(day_number).zfill(2) + '/' + str(
                        month_of_last).zfill(2)
                    line.insert(0, time)

            else:
                month = month_of_last
                day_number = day_of_last
                if year % 4 == 0:
                    days_in_month.update([('2', 29)])
                else:
                    days_in_month.update([('2', 28)])

                for j in range(16):
                    if parts[str((current_part - j) % 8)][-5:-3] == '24':
                        day_number = (int(day_of_last) - 1) % days_in_month[str((int(month_of_last) - 1) % 12)]
                        day_of_last = day_of_last - 1

                    if day_number == 0:
                        day_number = days_in_month[str((int(month_of_last) - 1) % 12)]

                    if day_number >= 25:
                        if month_of_last == 1:
                            month = 12
                        else:
                            month = month_of_last - 1

                    time = parts[str((current_part - j) % 8)] + ' ' + str(day_number).zfill(2) + '/' + str(month).zfill(
                        2)
                    line.insert(0, time)

        return line

    names = []
    values = []
    activity = await players_activity()
    for y in activity:
        cur.execute(f"SELECT players from players_activity where time = '{y}'")
        number = cur.fetchall()
        y = tags[y[:11]] + ' ' + y[12:]
        names.append(y)
        if number:
            values.append(int(number[0][0]))
        else:
            values.append(0)

    await graph(names, values, title='Активность игроков', graph_name='players_activity')

    photo = open('players_activity.png', 'rb')

    return photo
