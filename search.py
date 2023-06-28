import json
from datatypes import Program

def reformat_db():
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
		json.dump(db, f)

def load_db():
	data=[]
	with open('db.json') as f:
		for x in json.load(f):
			data.append( Program(x) )
	return data

def search(db, ball=311, contract=False, program_code='', vuz=0):
	results=[]
	for x in db:
		match=True
		if not contract:
			if x.ball_budget>ball:
				match=False
			if program_code and x.code!=program_code:
				match=False
			if vuz and x.vuz_id!=vuz:
				match=False
			
		if match:
			results.append(x)
	return results
if __name__=="__main__":
	#reformat_db()
	database=load_db()
	for x in search(database, ball=200, program_code='09.03.01'):
		print(x)
