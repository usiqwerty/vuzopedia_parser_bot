from aiogram.types import CallbackQuery
import re
def search_callback_filter(callback: CallbackQuery):
	data=callback.data
	if data[:7] == "search_":
		page=data[7:]
		try:
			page=int(page)
			return {'page': page}
		except:
			return False
	return False
def more_callback_filter(callback: CallbackQuery):
	r=re.search(r"more_([\d]+)_([\d]+)", callback.data)
	if r and r.groups():
		try:
			f, l = r.groups()
			return {'first':f, "last": l}
		except:
			return False
	return False
def info_callback_filter(callback: CallbackQuery):
	data=callback.data
	print(data)
	if data[:8] == "r_index_":
		index=data[8:]
		try:
			index=int(index)
			return {'index': index}
		except:
			return False
	return False