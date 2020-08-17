# coding=utf-8

from misc import conn, cur


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
    Кол-во новых пользователей в месяц
    Создаем поле для нового месяца
    {
    после каждой игры проверяем начало месяца
    если время игры позже 00:00:00 первого числа -> создаем запись
    INSERT INTO New_Players (Month, New_players) VALUES({month + year}, {0})
    }
    //лимит в 12 полей

    Отмечаем новое создание записи для юзера -> апдейтаем запись соответствуещего месяца

    EXAMPLE:
        id          Month        New_players
        1          Nov 2020        42
        2          Dec 2020        44
        3          Jan 2021        37


    """

    pass


async def players_activity_per3h():
    """

    После каждой игры проверяем время
    {
    SELECT Time FROM Players_Activity WHERE Id = (SELECT max(id) FROM Players_activity)
    }
    каждые 3 часа делаем новую запись в бд
    00:00
    03:00
    06:00
    09:00
    12:00
    15:00
    18:00
    21:00

    если не было игр в каком то промежутке, то создаем поле с значением 0
    собирать информацию о кол-ве игроков и апдейтаем для опредленного промежутка времени

    предел в 7 дней
    всегда проверять на кол-во записей, их должно быть не больше 7*8

    EXAMPLE:
        id            time              players
        1       18:00-21:00 10/04        4
        2       21:00-00:00 10/04        5
        3       00:00-03:00 11/04       10

    """
    pass


async def daily_plays():
    """

    проверять время после игры
    если после 00:00, создаем поле для нового дня
    иначе, апдейтаем кол-во игр в строку с определенным днем

    EXAMPLE:
        id          day        plays
        1       Mo 10/02/20     12
        2       Tu 11/02/20     8
        3       We 12/02/20     3

    """
    pass


async def show_players_activity():
    pass


