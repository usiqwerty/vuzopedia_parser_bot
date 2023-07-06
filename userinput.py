import aiogram.enums
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command

from keyboards import markup_search, markup_vuz, markup_ball, markup_prog, keyboard_result_builder, keyboard_more_builder
from filters import info_callback_filter, more_callback_filter, search_callback_filter
import search
router=Router()

VUZ=1
PROGRAM=2
BALL=3

vuzes = search.load_all_vuzes()
programs = search.load_programs()
program_codes = search.load_program_codes()

class UserSession:
	def __init__(self):
		self.vuz_id: int = 0
		self.program_code: str = ''
		self.ball_ege: int = 0
		self.input_mode: int = 0

		self.vuz_input: int = 0
		self.program_input: str = ''
		self.ball_input: int = 0

user_session=UserSession()

def user_info_formatted():
	ball_ege = user_session.ball_ege
	program_code = user_session.program_code
	vuz_id = user_session.vuz_id

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
	global user_session

	await callback.answer()
	if callback.data=="vuz_inp":
		await callback.message.edit_text('Введите название вуза (не аббревиатурой) и нажмите сохранить', reply_markup=markup_vuz)
		user_session.input_mode=1
	elif callback.data == "prog_inp":
		await callback.message.edit_text('Введите название программы (не аббревиатурой) и нажмите сохранить', reply_markup=markup_prog)
		user_session.input_mode=2
	elif callback.data == "balls_inp":
		await callback.message.edit_text('Введите баллы ЕГЭ и нажмите сохранить', reply_markup=markup_ball)
		user_session.input_mode=3

@router.callback_query(Text(text=["save"]))
async def search_data_save_callback(callback: CallbackQuery):
	global user_session
	user_session.vuz_id =user_session.vuz_input
	user_session.program_code = user_session.program_input
	user_session.ball_ege= user_session.ball_input

	user_session.input_mode = 0
	await callback.answer("Данные сохранены")
	#await callback.message.edit_text(user_info_formatted(), reply_markup=markup_search)
	await callback.message.answer(user_info_formatted(), reply_markup=markup_search)

@router.callback_query(Text(text=["vuz_reset", "prog_reset", "balls_reset"]))
async def search_data_reset_callback(callback: CallbackQuery):
	global user_session #, vuz_id, program_code, ball_ege
	await callback.answer()
	if callback.data=="vuz_reset":
		user_session.vuz_id=''
		user_session.vuz_input=0
	elif callback.data == "prog_reset":
		user_session.program_code=''
		user_session.program_input=''
	elif callback.data == "balls_reset":
		user_session.ball_ege=0
		user_session.ball_input=0

	user_session.input_mode=0
	#await callback.message.edit_text(user_info_formatted(), reply_markup=markup_search)
	await callback.message.answer(user_info_formatted(), reply_markup=markup_search)

@router.message(lambda x: user_session.input_mode>0)
async def input_data(message: Message):
	global user_session

	input_mode=user_session.input_mode
	print('input', input_mode)

	if input_mode==PROGRAM:
		value = search.program_code_by_name(message.text, program_codes)
		program_name=program_codes[value]
		user_session.program_input = value
		await message.answer(f"{value}: {program_name}", reply_markup=markup_prog)

	elif input_mode==VUZ:
		v_id = search.vuz_id_by_name(message.text, vuzes)
		v_name = vuzes[v_id]

		user_session.vuz_input = v_id
		await message.answer(f"{v_id}: {v_name}", reply_markup=markup_vuz)

	elif input_mode==BALL:
		ball = message.text

		try:
			ball = int(ball)
			if ball < 1 or ball > 310:
				ball = 0
		except:
			ball = 0

		user_session.ball_input = ball
		await message.answer(f"Сумма: {ball}", reply_markup=markup_ball)

@router.callback_query(search_callback_filter)
async def run_db_search(callback: CallbackQuery, page:int):
	#global user_session

	ball_ege=user_session.ball_ege
	program_code=user_session.program_code
	vuz_id = user_session.vuz_id

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
async def program_details(callback: CallbackQuery, index:int):
	ball_ege=user_session.ball_ege
	program_code=user_session.program_code
	vuz_id = user_session.vuz_id

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