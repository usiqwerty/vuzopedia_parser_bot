import json
from datatypes import Program
import os
from fnmatch import fnmatch
from fuzzywuzzy import process
"""def reformat_db():
	with open('programs.json') as f:
		data=json.load(f)
	#data=[
	#	['/a', '00.00.00', 88, 1000, 0, 180,90,0,150,40],
	#	['/b', '00.00.01', 88, 1000, 0, 180,90,0,150,40],
	#	['/c', '00.00.00', 89, 1000, 0, 180,90,0,150,40]
	#	]
	db=[]
	for x in data:
		#print(x)
		if len(x)==11:
			link, code, vuz, _, price, _, ball_budget, places_budget, _, ball_contract, places_contract = x
		if len(x)==9:
			link, code, vuz, _, price, _, _, ball_contract, places_contract = x
			ball_budget=-1
			places_budget=-1	
		db.append({
			'link': link,
			'code': code,
			'vuz_id': vuz,
			'price': price,
			'pl_b': places_budget,
			'b_b': ball_budget,
			'pl_c': places_contract,
			'b_c': ball_contract,
		})
	with open('db.json', 'w') as f:
		json.dump(db, f)"""
def reformat_program_list_to_object(program: list) -> Program:

	#data=['/a', '00.00.00', 88, 1000, 0, 180,90,0,150,40]
	#print(x)
	if len(program)==11:
		link, code, vuz, _, price, _, ball_budget, places_budget, _, ball_contract, places_contract = program
	elif len(program)==9:
		link, code, vuz, _, price, _, _, ball_contract, places_contract = program
		ball_budget=-1
		places_budget=-1
	else:
		raise ValueError
	prog_dict={
		'link': link,
		'code': code,
		'vuz_id': vuz,
		'price': price,
		'pl_b': places_budget,
		'b_b': ball_budget,
		'pl_c': places_contract,
		'b_c': ball_contract,
	}
	return Program(prog_dict)
def obj_list_to_json(programs: list[Program]):
	res=[]
	for program in programs:
		res.append(program.toJsonDict())
	return res
def load_programs() -> list[Program]:
	data=[]
	with open('programs.json') as f:
		for x in json.load(f):
			data.append( Program(x) )
	return data
def load_program_codes() -> dict[str,str]:
	with open('codes.json') as f:
		return json.load(f)
def load_vuzes_city(city_id: int) -> dict:
	city_vuzes=dict()
	with open(f'vuzes-{city_id}.json') as f:
		for k,v in json.load(f).items():
			city_vuzes[k]=v
	return city_vuzes
def load_all_vuzes() -> dict[int, str]:
	files=os.listdir()

	all_vuzes=dict()

	for file in files:
		if fnmatch(file, 'vuzes-*.json'):
			with open(file) as f:
				city_vuzes = json.load(f)
				for vuz in city_vuzes:
					all_vuzes[int(vuz)]=city_vuzes[vuz]
	return all_vuzes
def search(db: list[Program], ball=311, contract=False, program_code='', vuz=0) -> list[Program]:
	results=[]
	for prog in db:
		match=True
		if not contract:
			if prog.ball_budget>ball:
				match=False
			if program_code and prog.code!=program_code:
				match=False
			if vuz and prog.vuz_id!=vuz:
				match=False
			
		if match:
			results.append(prog)
	return results

def vuz_id_by_name(name: str, vuzes: dict) -> int:
	vuz_name = process.extractOne(name, vuzes.values())[0]
	for k in vuzes:
		if vuzes[k] == vuz_name:
			return k
def program_code_by_name(name: str, program_codes: dict) -> str:
	program_name=process.extractOne(name, program_codes.values())[0]
	for k in program_codes:
		#print(name, program_codes[k])
		if program_codes[k]==program_name:
			return k
#def vuz

if __name__=="__main__":

	database = load_programs()
	vuzes = load_all_vuzes()
	pcodes= load_program_codes()
	#wanted_vuz_id=vuz_id_by_name('уральский федеральный', vuzes)

	#for item in search(database, vuz=wanted_vuz_id, program_code='09.03.01'):
	#	print(item, vuzes[item.vuz_id])
	pc=program_code_by_name('программная', pcodes)
	print(pc, pcodes[pc])
