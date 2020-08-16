# coding=utf-8
from misc import conn, cur


class Chat:

    def __init__(self, chatid, title, date):
        self.chatid = chatid
        self.title = title
        self.date = date

    async def add_chat_data(self):
        #   ДОБАВЛЕНИЕ ТАБЛИЦЫ ЛОГОВ ЧАТА
        try:
            namedb = 'logchat' + str(abs(self.chatid))
            cur.execute("CREATE TABLE if not exists %s"
                        "(Id     Serial,"
                        "Log     VARCHAR(20)  NOT NULL,"
                        "PRIMARY KEY(Id));" % namedb)
        except Exception as e:
            pass
        else:
            conn.commit()

        try:
            cur.execute("SELECT count(IdChat) From Stats WHERE IdChat = '%i'" % self.chatid)
            title_count = cur.fetchall()[0][0]
            if title_count < 1:
                cur.execute("INSERT INTO Stats (Title, IdChat, Plays, Won, Lost, Bets_num, Last_activity) "
                            "VALUES ('%s', '%i', 0, 0, 0, 0, '%s')" % (self.title, self.chatid, self.date))
            else:
                cur.execute("UPDATE Stats set Title = '%s', Last_activity = '%s' WHERE IdChat = '%i'" %
                            (self.title, self.date, self.chatid))
        except Exception as e:
            pass
        else:
            conn.commit()


    async def logs(self, message):
        LOG = ''
        namedb = 'logchat' + str(abs(self.chatid))
        try:
            cur.execute("SELECT Log FROM %s" % namedb)
            logs = cur.fetchall()
            for i in range(len(logs)):
                if logs[i][0] != 'Бонус':
                    LOG += "🎲  %s\n" % logs[i][0]
                else:
                    LOG += "🏵  %s\n" % logs[i][0]
            if LOG != '':
                await message.answer(LOG)
            else:
                await message.answer("Лог пустой")
        except Exception as e:
            await message.reply("Oops, something went wrong")