#!/usr/bin/env python
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from aiogram.filters import Command, Text
from aiogram import F
import asyncio
import json
import userinput

with open('config.json') as f:
	config=json.load(f)

bot=Bot(token=config['token'])
dp=Dispatcher()
dp.include_router(userinput.router)
print('bot, dp')
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
	await message.answer('Это первый запуск, привет!')


@dp.message(Command(commands=['update']), F.from_user.id==config['admin'])
async def update_command(message: Message):

	await message.answer('Запускаем обновление баз... Это займёт время, мы напишем, когда закончим')
	await message.answer('Обновление завершено')

#@dp.message()
#async def any_message(message: Message):
	#await message.answer("Сообщение не обработано")


async def main():
	print('Starting polling...')
	await dp.start_polling(bot)
	print('Ended polling')


if __name__=="__main__":

	asyncio.run(main())
	#main()
