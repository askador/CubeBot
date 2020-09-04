# coding=utf-8

import psycopg2
from data.config import DB
from data.config import token
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = psycopg2.connect(DB)
cur = conn.cursor()


months = {
    '1': 'Jan',
    '2': 'Feb',
    '3': 'Mar',
    '4': 'Apr',
    '5': 'May',
    '6': 'Jun',
    '7': 'Jul',
    '8': 'Aug',
    '9': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '0': 'Dec',
}

days = {
      '1': 'Mon',
      '2': 'Tue',
      '3': 'Wed',
      '4': 'Thr',
      '5': 'Fri',
      '6': 'Sat',
      '0': 'Sun',
}

days_in_month = {
     '1': 31,
     '2': 28,
     '3': 31,
     '4': 30,
     '5': 31,
     '6': 30,
     '7': 31,
     '8': 31,
     '9': 30,
    '10': 31,
    '11': 30,
    '0': 31
}

parts = {
    '0': '00:00-03:00',
    '1': '03:00-06:00',
    '2': '06:00-09:00',
    '3': '09:00-12:00',
    '4': '12:00-15:00',
    '5': '15:00-18:00',
    '6': '18:00-21:00',
    '7': '21:00-24:00',
}

tags = {
    '00:00-03:00': '1/8',
    '03:00-06:00': '2/8',
    '06:00-09:00': '3/8',
    '09:00-12:00': '4/8',
    '12:00-15:00': '5/8',
    '15:00-18:00': '6/8',
    '18:00-21:00': '7/8',
    '21:00-24:00': '8/8',
}

