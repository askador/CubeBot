# coding=utf-8

from aiogram import Bot, Dispatcher
import psycopg2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '11111111:AAAAAAAAAAAAA'
DB = (
      "postgres://"
      )

bot = Bot(TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = psycopg2.connect(DB)

cur = conn.cursor()

