class Program:
	def __init__(self, json_dict):
		self.vuz_id = json_dict['vuz_id']
		self.code = json_dict['code']
		self.link = json_dict['link']
		self.price = json_dict['price']
		self.ball_budget = json_dict['b_b']
		self.ball_contract = json_dict['b_c']
		self.places_budget = json_dict['pl_b']
		self.places_contract = json_dict['pl_c']
	def toJsonDict(self):
		json_dict=dict()

		json_dict['vuz_id'] = self.vuz_id
		json_dict['code'] = self.code
		json_dict['link'] = self.link
		json_dict['price'] = self.price
		json_dict['b_b'] = self.ball_budget
		json_dict['b_c'] = self.ball_contract
		json_dict['pl_b'] = self.places_budget
		json_dict['pl_c'] = self.places_contract

		return json_dict
	def __repr__(self):
		return f"{self.code}: {self.ball_budget} ({self.places_budget}) ~ {self.price}"
