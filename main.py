import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from functions.functions import *

MAIN_URL = 'https://www.boursorama.com'
FIRST_PAGE = 'https://www.boursorama.com/bourse/trackers/recherche/autres/?beginnerEtfSearch%5Bcurrency%5D=EUR&beginnerEtfSearch%5Bcurrent%5D=characteristics&beginnerEtfSearch%5BisEtf%5D=1&beginnerEtfSearch%5Bsaving%5D=0&beginnerEtfSearch%5Btaxation%5D=1&refreshableId=js-tabs-fund-refreshable-66262a8c98e2a'
ETF_LEV_LINK = 'https://www.boursorama.com/bourse/trackers/palmares-leverage/_topflop-leverage?etfleverage%5Bcurrent%5D=characteristics&etfleverage%5BisEtf%5D=1&etfleverage%5BisLeverage%5D=1&refreshableId=js-tabs-fund-refreshable-662654b592333'

def main():
	number_ETFs = get_number_ETFs(FIRST_PAGE)

	etf_list = ETF_scrapper(number_ETFs, FIRST_PAGE, MAIN_URL)

	etf_lev_list = ETF_lev_scrapper(ETF_LEV_LINK, MAIN_URL)

	etfs = etf_list + etf_lev_list

	df = pd.DataFrame({
		'ISIN': [etf.ISIN for etf in etfs],
		'name': [etf.name for etf in etfs],
		'price': [etf.price for etf in etfs],
		'fees': [etf.fees for etf in etfs],
		'company': [etf.company for etf in etfs],
		'category': [etf.category for etf in etfs],
		'reference_index': [etf.reference_index for etf in etfs],
		'link': [etf.link for etf in etfs],
		'is_leveradged': [etf.is_leveradged for etf in etfs]
	})

	df.to_excel('./data/output.xlsx', index=False)

if __name__ == '__main__':
	main()
