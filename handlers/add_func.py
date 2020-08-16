# coding=utf-8
from misc import conn, cur


async def to_del_mess(chatid, mess_id):
    cur.execute("INSERT INTO todelmes (IDChat, MessId) VALUES('%i','%i')" %
                (chatid, mess_id))
    conn.commit()


#  make good bet/balance view
async def makegoodview(how):
    how = str(how)
    how = list(how)
    q = 0
    for i in range(1, len(how) + 1):
        if -i % 3 == 0:
            how.insert(-(i + q), ',')
            q += 1
    if how[0] == ',':
        del how[0]
    how = ''.join(how)
    return how
