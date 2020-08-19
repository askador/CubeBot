# coding=utf-8

from aiogram import Bot, Dispatcher
import psycopg2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '996503468:AAE8aR09qP8uPdF-322GSr1DTtJUmUBAhmo'
DB = (
      "postgres://ldecbdhgnzovuk:223d4e6aeda20ddca3d72f25d4557040ef6b05616a959788096c193d5f70e61b"
      "@ec2-34-197-188-147.compute-1.amazonaws.com:5432/db5fuj6d41dpo6"
      )

bot = Bot(TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = psycopg2.connect(DB)

cur = conn.cursor()

# cur.execute("DELETE FROM Game WHERE IDChat = 798393467")
# conn.commit()