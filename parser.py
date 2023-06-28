from bs4 import BeautifulSoup as bs
import requests
from datacleaner import extract_number, extract_vuz_id
import time
import json
import random
from datatypes import Program
#page=1
#url=f"https://vuzopedia.ru/region/city/83?page=2"


#r=requests.get(url)
#if r:
#	with open('data.html', 'w') as f:
#		f.write(r.text)

#exit()
#print(url)
with open('data.html') as f:
	data=f.read()

headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
}
def parse_vuzes(data):
	soup=bs(data, 'html.parser')
	results=[]
	for div in soup.find_all('div', class_=['newItemVuz', 'newItemVuzPremium']): #
		info=div.find('div', class_='vuzesfullnorm')
		link_tag=info.find('div', class_='blockAfter').find('a')
		name=link_tag.text.strip()	
		link=link_tag['href']
		#print(name, link)
		vuz_id=extract_vuz_id(link)
		if vuz_id:
			vuz_id=int(vuz_id)
			results.append({'vuz_id':vuz_id, 'name':name,})
	return results

def parse_programs(data, spec_codes, vuz_id):
	soup=bs(data, 'html.parser')
	results=[]
	for div in soup.find_all('div', class_='newBlockSpecProg'):
		link_tag=div.find('div', class_='osnBlockInfoSm').find('a')
		if '|' in link_tag.text:
			code, name=link_tag.text.strip().split('|')
		else:
			code=link_tag.text.strip()
			name=''
		code, name=code.strip(), name.strip()
		link=link_tag['href']
		#print(code, name, link)
		if code not in spec_codes:
			spec_codes[code]=name		

		options_div=div.find('div', class_='col-md-2')
		options=[]
		for option_div in options_div.find_all('div', class_='col-md-12'):

			center_tag=option_div.find_all('center')
			for center in center_tag:
				a_tag=center.find('a')
				if a_tag:
					value=a_tag.getText(';').split(';')[0]
					str_value=extract_number(value)
					if str_value:
						options.append(int(str_value))
					else:
						options.append(0)
				else:
					options.append(0)

		if options:
			#options.pop(0) #там всегда ноль почему-то
			#print(options)
			results.append([link, code, vuz_id] + options)
		
	return results, spec_codes
def fetch_vuz_programs(vuz_id):
	print(f'fetch_programs({vuz_id})')
	spec_codes=dict()

	result=[]
	page=0
	
	noneflag=False
	while True:
		page+=1
		time.sleep(random.randint(15,30))
		if page%5==4:
			print('Extra delay')
			time.sleep(random.randint(30, 60))
		print(f"{page=}")
		url = f"https://vuzopedia.ru/vuz/{vuz_id}/programs/bakispec?page={page}"
		r=requests.get(url, headers=headers)
		if r:
			progs, spec_codes = parse_programs(r.text, spec_codes, vuz_id)
			if not progs:
				if noneflag:
					break
				else:

					print("CAPTCHA WARNING")
					print("noneflag set up, 60 seconds extra delay")
					page-=1
					time.sleep(60)
					noneflag=True
			else:
				if noneflag:
					print('noneflag set down')
					noneflag=False
			result+=progs

	return result, spec_codes

def fetch_city_vuzes(city_id):
	print(f'fetch_city_vuzes({city_id})')
	result=[]
	page=0
	
	noneflag=False
	while True:
		page+=1
		time.sleep(random.randint(15,30))
		if page%5==4:
			print('Extra delay')
			time.sleep(random.randint(30, 60))
		print(f"{page=}")
		url = f"https://vuzopedia.ru/region/city/{city_id}?page={page}"
		r=requests.get(url, headers=headers)
		if r:
			vuzes=parse_vuzes(r.text)
			#print(vuzes)
			if not vuzes:
				if noneflag:
					break
				else:

					print("CAPTCHA WARNING")
					print("noneflag set up, 3 minutes extra delay")
					page-=1
					time.sleep(180)
					noneflag=True
			else:
				if noneflag:
					print('noneflag set down')
					noneflag=False
			result+=vuzes

	return result

def update_programs():
	print('update_programs()')
	progs, codes= fetch_programs()
	print(f"Got {len(progs)} programs")
	with open('programs.json', 'w') as f:
		print('Writing programs.json')
		json.dump(progs, f)
	with open('codes.json', 'w') as f:
		print('Writing codes.json')
		json.dump(codes, f)
def download_city_vuzes(city):
	print(f'download_vuzes({city})')
	vuzes= fetch_city_vuzes(city)
	print(f"Got {len(vuzes)} vuzes")

	with open(f'vuzes-{city}.json', 'w') as f:
		print(f'Writing vuzes-{city}.json')
		json.dump(vuzes, f)

def update_city_vuzes_and_programs(city, spec_codes):
	print(f"update_city_vuzes({city})")
	#download_city_vuzes(city)
	programs=[]
	with open(f'vuzes-{city}.json') as f:
		new_vuzes=json.load(f)
	for x in new_vuzes:
		v_id=x['vuz_id']
		progs, s_codes=fetch_vuz_programs(v_id)
		programs+=progs
		for code in s_codes:
			if code not in spec_codes:
				spec_codes[code]=s_codes[code]

	with open('programs.json') as f:
		print('Reading programs.json')
		data=json.load(f)
	with open('programs.json', 'w') as f:
		print('appending')
		data+=programs
		print('Writing programs.json')
		json.dump(data, f)
	with open('codes.json', 'w') as f:
		
		print('Writing codes.json')
		json.dump(spec_codes, f)
	print('Reformatting database...')
	search.reformat_db()
	print('Update done!')
#print(parse_programs(data, {})[0])
#update_programs()
update_city_vuzes_and_programs(83, {})

