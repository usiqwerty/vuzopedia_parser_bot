#!/usr/bin/env python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import json

with open('config.json') as f:
	config=json.load(f)

balls={}


bot=Bot(token=config['token'])
dp=Dispatcher()

print('bot, dp')

@dp.message(Command(commands=['start']))
async def start_command(message: Message):
	await message.answer('Это первый запуск, необходимо ввести баллы')
	await message.answer('')

@dp.message(Command(commands=['update']))
async def start_command(message: Message):
	await message.answer('Запускаем обновление баз... Это займёт время, мы напишем, когда закончим')
	await message.answer('Обновление завершено')
async def main():
	print('Starting polling...')
	await dp.start_polling(bot)
	print('Ended polling')


if __name__=="__main__":
	asyncio.run(main())
	#main()
