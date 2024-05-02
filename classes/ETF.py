class ETF():
	def __init__(self, ISIN: int, name: str, link: str, category: str, company: str, price: float, fees: float, reference_index: str, is_leveradged=False) -> None:
		self.ISIN = ISIN
		self.name = name
		self.link = link
		self.category = category
		self.company = company
		self.price = price
		self.fees = fees
		self.reference_index = reference_index
		self.is_leveradged = is_leveradged
