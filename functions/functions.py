import bs4
import requests as r
import re
from tqdm import tqdm
from time import sleep

from classes.ETF import ETF

def get_number_ETFs(link: str) -> int|None:
	res = r.get(link)
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	matches = re.findall(r'\(\d+\)', soup.find_all('span', class_='c-heading__text / o-flag__body')[1].get_text())
	if len(matches) == 0:
		return None
	return int(matches[0].replace('(', '').replace(')', ''))

def get_ETF(link: str) -> ETF:
	res = r.get(link)
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	name = soup.find('a', class_='c-faceplate__company-link').get_text().strip()
	isin, company = soup.find('h2', class_='c-faceplate__isin').get_text().split(' - ')
	price = float(soup.find('span', class_='c-instrument c-instrument--last').get_text().replace(',', '.').replace(' ', ''))
	headers = soup.find_all('p', class_='c-list-info__value u-color-big-stone')
	ref_index = headers[0].get_text().strip()
	category = headers[1].get_text().strip()
	fees = float(soup.find('div', class_='c-list-info c-list-info--nopadding-bottom').find_all('li')[2].find_all('p')[1].get_text().replace('%', '').strip().replace(',', '.').replace(' ', ''))
	return ETF(isin, name, link, category, company, price, fees, ref_index)

def ETF_scrapper(number_ETFs: int, first_page: str, main_url: str) -> list[ETF]:
	output = []
	counter = 0
	page_number = 1
	while counter < number_ETFs:
		if page_number == 1:
			res = r.get(first_page)
		else:
			res = r.get(f'https://www.boursorama.com/bourse/trackers/recherche/autres/page-{page_number}?beginnerEtfSearch%5Bcurrency%5D=EUR&beginnerEtfSearch%5Bcurrent%5D=characteristics&beginnerEtfSearch%5BisEtf%5D=1&beginnerEtfSearch%5Btaxation%5D=1')
		soup = bs4.BeautifulSoup(res.content, 'html.parser')
		tags = soup.find_all('tr', class_='c-table__row')[1:]
		for tag in tqdm(tags, desc=f'Scrapping ETFs on page {page_number}'):
			link = f'{main_url}{tag.find('a').get('href')}'
			etf = get_ETF(link)
			output.append(etf)
			sleep(0.2)
		counter += len(output) - counter
		page_number += 1
	return output

def is_PEA_eligible(link: str) -> bool:
	res = r.get(link)
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	tag = soup.find_all('li', class_='c-list-info__item c-list-info__item--no-padding@md')[2]
	tags = tag.find_all('button')
	if len(tags) == 0:
		return False
	for tag in tags:
		if tag.get('title') == 'PEA':
			return True
	return False

def ETF_lev_scrapper(etf_lev_link: str, main_url: str) -> list[ETF]:
	output = []
	res = r.get(etf_lev_link)
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	tags = soup.find_all('tr', class_='c-table__row')[1:]
	for tag in tqdm(tags, desc='Scrapping leveradged ETFs'):
		link = f'{main_url}{tag.find('a').get('href')}'
		if is_PEA_eligible(link):
			etf = get_ETF(link)
			etf.is_leveradged = True
			output.append(etf)
			sleep(0.2)
	return output
