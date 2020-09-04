# coding=utf-8
from aiogram import executor
from data.misc import dp
from on_startup import all_loops

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=all_loops)
