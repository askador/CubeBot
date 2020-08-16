# coding=utf-8
import asyncio
from aiogram import executor
from misc import dp, bot
import handlers

from on_startup import loop_checking_bets, loop_bonus_close, loop_game_autostart, loop_shaking, loop_giveaway


async def all_loops(dp):
    await bot.send_message(-443076596, "Запуск. . .")
    general = asyncio.get_event_loop()

    general.create_task(loop_game_autostart())
    general.create_task(loop_shaking())
    general.create_task(loop_checking_bets())
    general.create_task(loop_bonus_close())
    general.create_task(loop_giveaway())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=all_loops)
