import aiogram.enums
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command

from keyboards import markup_search, markup_vuz, markup_ball, markup_prog, keyboard_result_builder, keyboard_more_builder
from filters import info_callback_filter, more_callback_filter, search_callback_filter
import search
router=Router()


vuzes=search.load_all_vuzes()
programs=search.load_programs()
program_codes=search.load_program_codes()


vuz_id=0 #1
program_code='' #2
ball_ege=0 #3

last_input=None
input_mode=0 #


def user_info_formatted():
	return f"Вуз: {vuzes[vuz_id] if vuz_id else 'Нет'}\n" \
		   f"Программа: {program_codes[program_code] if program_code else 'Нет'}\n" \
		   f"Баллы ЕГЭ: {ball_ege if ball_ege else 'Нет'}"

@router.message(Command(commands=['search']))
async def search_data_input_message(message: Message):
	await message.answer(user_info_formatted(), reply_markup=markup_search)
	#await message.answer('')

@router.callback_query(Text(text=["search"]))
async def search_data_input_callback(callback: CallbackQuery):
	#await callback.message.edit_text(user_info_formatted(), reply_markup=markup_search)
	await callback.message.answer(user_info_formatted(), reply_markup=markup_search)
@router.callback_query(Text(text=["vuz_inp", "prog_inp", "balls_inp"]))
async def search_data_input_callback(callback: CallbackQuery):
	global input_mode
	await callback.answer()
	if callback.data=="vuz_inp":
		await callback.message.edit_text('Введите название вуза (не аббревиатурой) и нажмите сохранить', reply_markup=markup_vuz)
		input_mode=1
	elif callback.data == "prog_inp":
		await callback.message.edit_text('Введите название программы (не аббревиатурой) и нажмите сохранить', reply_markup=markup_prog)
		input_mode=2
	elif callback.data == "balls_inp":
		await callback.message.edit_text('Введите баллы ЕГЭ и нажмите сохранить', reply_markup=markup_ball)
		input_mode=3

@router.callback_query(Text(text=["vuz_save", "prog_save", "balls_save"]))
async def search_data_save_callback(callback: CallbackQuery):
	global input_mode, last_input, vuz_id, program_code, ball_ege

	if callback.data=="vuz_save":
		vuz_id=last_input
		last_input=None
		await callback.answer("Вуз сохранён")
	elif callback.data == "prog_save":
		program_code=last_input
		await callback.answer("Программа сохранена")
	elif callback.data == "balls_save":
		ball_ege=last_input
		await callback.answer("Балл сохранён")
	input_mode=0
	#await callback.message.edit_text(user_info_formatted(), reply_markup=markup_search)
	await callback.message.answer(user_info_formatted(), reply_markup=markup_search)

@router.callback_query(Text(text=["vuz_reset", "prog_reset", "balls_reset"]))
async def search_data_reset_callback(callback: CallbackQuery):
	global input_mode, vuz_id, program_code, ball_ege
	await callback.answer()
	if callback.data=="vuz_reset":
		vuz_id=0
	elif callback.data == "prog_reset":
		program_code=''
	elif callback.data == "balls_reset":
		ball_ege=0
	input_mode=0
	#await callback.message.edit_text(user_info_formatted(), reply_markup=markup_search)
	await callback.message.answer(user_info_formatted(), reply_markup=markup_search)

@router.message(lambda x: input_mode==2)
async def input_program_name(message: Message):
	global last_input
	program_code=search.program_code_by_name(message.text, program_codes)
	program_name=program_codes[program_code]
	last_input = program_code

	await message.answer(f"{program_code}: {program_name}", reply_markup=markup_prog)

@router.message(lambda x: input_mode==1)
async def input_vuz_name(message: Message):
	global last_input
	v_id = search.vuz_id_by_name(message.text, vuzes)
	v_name= vuzes[v_id]
	last_input = v_id

	await message.answer(f"{v_id}: {v_name}", reply_markup=markup_vuz)


@router.message(lambda x: input_mode == 3)
async def input_ball(message: Message):
	global last_input
	ball=message.text

	try:
		ball=int(ball)
		if ball<1 or ball>310:
			ball=0
	except:
		ball=0

	last_input = ball
	await message.answer(f"Сумма: {ball}", reply_markup=markup_ball)

@router.callback_query(search_callback_filter)
async def run_db_search(callback: CallbackQuery, page:int):
	b=ball_ege if ball_ege else 311
	p=program_code if program_code else ''
	v=vuz_id if vuz_id else 0
	results=search.search(programs, ball=b, program_code=p, vuz=v)

	response=""
	for i in range(10*(page-1), len(results)):
		if i - 10*(page-1) == 10:
			break
		program=results[i]
		response+=f"<b>{i+1}.</b> {program_codes[program.code]} ({program.code}): на бюджет {program.ball_budget} балла, {program.places_budget} мест\n"
	on_page_count=min(len(results), 10)

	await callback.message.answer(text=response, parse_mode="HTML", reply_markup=keyboard_result_builder(on_page_count, len(results), page))
	await callback.answer()

@router.callback_query(info_callback_filter)
async def program_info_from_search(callback: CallbackQuery, index:int):
	b=ball_ege if ball_ege else 311
	p=program_code if program_code else ''
	v=vuz_id if vuz_id else 0
	results=search.search(programs, ball=b, program_code=p, vuz=v)

	program=results[index]
	code=program.code
	vuz = vuzes [ program.vuz_id ]
	response = f"Программа <a href='https://vuzopedia.ru{program.link}'> {program_codes[code]} ({code})</a> в вузе <b>{vuz}</b>\n" \
			   f"Балл на бюджет <b>{program.ball_budget}</b> ({program.places_budget} мест)\n" \
			   f"Балл на контракт: <b>{program.ball_contract}</b> ({program.places_contract} мест), цена {program.price} руб/год\n"
	await callback.message.answer(text=response, parse_mode=aiogram.enums.ParseMode.HTML)
	await callback.answer()

@router.callback_query(Text(text=['none']))
async def none_callback(callback: CallbackQuery):
	await callback.answer()

@router.callback_query(more_callback_filter)
async def more_callback(callback: CallbackQuery, first, last):
	await callback.message.edit_text(text=callback.message.text, reply_markup=keyboard_more_builder(first, last))