import re

def extract_number(string):
	res=re.search(r"[\s\D]*([\d]+)[\s\D]*", string)
	if res:
		return int(res.groups()[0])
def extract_vuz_id(link):
	res=re.search(r"/vuz/([\d]+)", link)
	if res:
		return int(res.groups()[0])
