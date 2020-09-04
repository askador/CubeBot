# coding=utf-8
import asyncio
from aiogram import types

from data.misc import bot, conn, cur
from utils.add_func import to_del_mess
from utils.autostart import game_autostart
from utils.bets import checking_bets


class Game:
    def __init__(self, chatid):
        self.chatid = int(chatid)

    async def start_game_message(self):
        game_kb = types.InlineKeyboardMarkup(row_width=3)
        n1 = types.InlineKeyboardButton(text='5 на 1', callback_data="1")
        n2 = types.InlineKeyboardButton(text='5 на 2', callback_data="2")
        n3 = types.InlineKeyboardButton(text='5 на 3', callback_data="3")
        game_kb.row(n1, n2, n3)

        n4 = types.InlineKeyboardButton(text='5 на 4', callback_data="4")
        n5 = types.InlineKeyboardButton(text='5 на 5', callback_data="5")
        n6 = types.InlineKeyboardButton(text='5 на 6', callback_data="6")
        game_kb.row(n4, n5, n6)

        t13 = types.InlineKeyboardButton(text='5 на 1-3', callback_data="1-3")
        t46 = types.InlineKeyboardButton(text='5 на 4-6', callback_data="4-6")
        game_kb.add(t13, t46)

        t12 = types.InlineKeyboardButton(text='5 на 1-2', callback_data="1-2")
        t34 = types.InlineKeyboardButton(text='5 на 3-4', callback_data="3-4")
        t56 = types.InlineKeyboardButton(text='5 на 5-6', callback_data="5-6")

        game_kb.row(t12, t34, t56)

        start_mes = await bot.send_message(self.chatid, "Угадай число от 1 до 6🎲\n"
                                                        "\n"
                                                        "<i>%п</i> - повтор, <i>%у</i> - удвоить\n"
                                                        "<i>ставки</i> - ваши ставки\n"
                                                        "<i>отмена</i> - отменить ставки", reply_markup=game_kb)
        await to_del_mess(self.chatid, start_mes.message_id)

    async def play(self, message):
        delay_start = 20

        # Запуск игры
        try:
            cur.execute("SELECT Shake FROM Game WHERE IDChat = %i" % self.chatid)
            is_game = cur.fetchall()
        except Exception as e:
            pass
        else:
            if is_game:
                mes3 = await message.reply("Игра уже запущена")
                await to_del_mess(self.chatid, mes3.message_id)

            elif not is_game:
                cur.execute("INSERT INTO Game (IDChat, Shake, Time, Shaking) VALUES (%i, False, %i, False)"
                            % (self.chatid, int(message.date.timestamp()) + delay_start))
                conn.commit()

                await self.start_game_message()

                cur.execute("SELECT Id FROM GAME WHERE Time = %i" % (int(message.date.timestamp()) + delay_start))
                id_game = cur.fetchall()[0][0]
                ioloop = asyncio.get_event_loop()

                ioloop.create_task(game_autostart(self.chatid, id_game)),  # autostart
                ioloop.create_task(checking_bets(message.chat.id))

