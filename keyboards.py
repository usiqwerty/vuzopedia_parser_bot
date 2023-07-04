from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup
from math import ceil
buttons_search={"vuz_inp":"Выбрать вуз",
		 "prog_inp":"Выбрать программу",
		 "balls_inp":"Ввести баллы",
		"search_1":"Искать"}
buttons_vuz= {'vuz_save':'Сохранить', 'search':'Назад', "vuz_reset":'Очистить'}
buttons_prog={'prog_save':'Сохранить', 'search':'Назад', "prog_reset":'Очистить'}
buttons_ball={'balls_save':'Сохранить', 'search':'Назад', 'balls_reset':"Очистить"}

def keyboard_more_builder(first:int, last:int) -> InlineKeyboardMarkup:
	kb_more = []
	first, last=int(first), int(last)
	row=[]
	button_count=0
	for n in range(first, last + 1):
		button_count+=1
		r=button_count%4
		if r==1:
			kb_more.append([])
		kb_more[-1].append( InlineKeyboardButton(text=str(n), callback_data=f"r_index_{n - 1}") )

	kb_more.append([InlineKeyboardButton(text='Назад', callback_data=f"search_{ceil(first/10)}")])
	return  InlineKeyboardMarkup(inline_keyboard=kb_more)
def keyboard_result_builder(on_page_count: int, total_count: int, page: int) -> InlineKeyboardMarkup:
	nav=[]
	first=10*(page-1)+1
	last=first+on_page_count-1
	if total_count>10:
		if page>1:
			nav.append(InlineKeyboardButton(text="<-", callback_data=f"search_{page-1}"))
		else:
			nav.append(InlineKeyboardButton(text=" ", callback_data="none"))

		if 10*(page-1) + on_page_count < total_count:
			nav.append(InlineKeyboardButton(text="->", callback_data=f"search_{page+1}"))
		else:
			nav.append(InlineKeyboardButton(text=" ", callback_data="none"))

	kb_result = [[InlineKeyboardButton(text="Подробнее...", callback_data=f"more_{first}_{last}")]]
	if nav:
		kb_result.append(nav)
	return InlineKeyboardMarkup(inline_keyboard=kb_result)

kb_search= [[ InlineKeyboardButton(text=text, callback_data=data)] for data, text in buttons_search.items() ]
kb_vuz = [[InlineKeyboardButton(text=text, callback_data=data) for data, text in buttons_vuz.items()]]
kb_prog = [[InlineKeyboardButton(text=text, callback_data=data) for data, text in buttons_prog.items()]]
kb_ball = [[InlineKeyboardButton(text=text, callback_data=data) for data, text in buttons_ball.items()]]


markup_search=InlineKeyboardMarkup(inline_keyboard=kb_search)
markup_vuz=InlineKeyboardMarkup(inline_keyboard=kb_vuz)
markup_prog=InlineKeyboardMarkup(inline_keyboard=kb_prog)
markup_ball=InlineKeyboardMarkup(inline_keyboard=kb_ball)
