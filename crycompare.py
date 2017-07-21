import sys
import requests
import warnings
import time


class Price:
	def __init__(self):
		self.coinlisturl = 'https://www.cryptocompare.com/api/data/coinlist/'
		self.priceurl = 'https://min-api.cryptocompare.com/data/price?'
		self.pricemultiurl = 'https://min-api.cryptocompare.com/data/pricemulti?'
		self.pricemultifullurl = 'https://min-api.cryptocompare.com/data/pricemultifull?'
		self.generateavgurl = 'https://min-api.cryptocompare.com/data/generateAvg?'
		self.dayavgurl = 'https://min-api.cryptocompare.com/data/dayAvg?'
		self.historicalurl = 'https://min-api.cryptocompare.com/data/pricehistorical?'
		self.coinsnapshoturl = 'https://www.cryptocompare.com/api/data/coinsnapshot/?'
		self.coinsnapshotfull = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?'

	def coin_list(self):
		return self.get_url(self.coinlisturl)

	def price(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.get_price(self.priceurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def pricemulti(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.get_price(self.pricemultiurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def pricemultifull(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.get_price(self.pricemultifullurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def priceHistorical(self, from_curr, to_curr, markets, ts=None, e=None, extraParams=None,
						sign=False, tryConversion=True):
		return self.get_price(self.historicalurl, from_curr, to_curr, markets, e, extraParams, sign, tryConversion)

	def generateAvg(self, from_curr, to_curr, markets, extraParams=None, sign=False, tryConversion=True):
		return self.get_avg(self.generateavgurl, from_curr, to_curr, markets, extraParams, sign, tryConversion)

	def dayAvg(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True,
			   avgType=None, UTCHourDiff=0, toTs=None):
		return self.get_avg(self.dayavgurl, from_curr, to_curr, e, extraParams, sign,
							tryConversion, avgType, UTCHourDiff, toTs)

	def coinSnapshot(self, from_curr, to_curr):
		return self.get_url(self.coinsnapshoturl + 'fsym=' + from_curr.upper() + '&tsym=' + to_curr.upper())

	def coinSnapshotFullById(self, coin_id):
		return self.get_url(self.coinsnapshotfull + 'id=' + str(coin_id))

	def stream(self, target, args, interval=60, filepath=None):
		def generate(f, a, i):
			while 1:
				yield f(*a)
				time.sleep(i)

		# if isinstance(filepath, str):
		for k in generate(target, args, interval):
			k['timestamp'] = time.time()
			print(k)

	def get_price(self, baseurl, from_curr, to_curr, e=None, extraParams=None, sign=False,
				  tryConversion=True, markets=None, ts=None):
		args = list()
		if isinstance(from_curr, str):
			args.append('fsym=' + from_curr.upper())
		elif isinstance(from_curr, list):
			args.append('fsyms=' + ','.join(from_curr).upper())
		if isinstance(to_curr, list):
			args.append('tsyms=' + ','.join(to_curr).upper())
		elif isinstance(to_curr, str):
			args.append('tsyms=' + to_curr.upper())
		if isinstance(markets, str):
			args.append('markets=' + markets)
		elif isinstance(markets, list):
			args.append('markets=' + ','.join(markets))
		if e:
			args.append('e=' + e)
		if extraParams:
			args.append('extraParams=' + extraParams)
		if sign:
			args.append('sign=true')
		if ts:
			args.append('ts=' + str(ts))
		if not tryConversion:
			args.append('tryConversion=false')
		if len(args) >= 2:
			return self.get_url(baseurl + '&'.join(args))
		else:
			raise ValueError('Must have both fsym and tsym arguments.')

	def get_avg(self, baseurl, from_curr, to_curr, markets=None, e=None, extraParams=None,
				sign=False, tryConversion=True, avgType=None, UTCHourDiff=0, toTs=None):
		args = list()
		if isinstance(from_curr, str):
			args.append('fsym=' + from_curr.upper())
		if isinstance(to_curr, str):
			args.append('tsym=' + to_curr.upper())
		if isinstance(markets, str):
			args.append('markets=' + markets)
		elif isinstance(markets, list):
			args.append('markets=' + ','.join(markets))
		if e:
			args.append('e=' + e)
		if extraParams:
			args.append('extraParams=' + extraParams)
		if sign:
			args.append('sign=true')
		if avgType:
			args.append('avgType=' + avgType)
		if UTCHourDiff:
			args.append('UTCHourDiff=' + UTCHourDiff)
		if toTs:
			args.append('toTs=' + toTs)
		if not tryConversion:
			args.append('tryConversion=false')
		if len(args) >= 2:
			return self.get_url(baseurl + '&'.join(args))
		else:
			raise ValueError('Must have both fsym and tsym arguments.')

	def get_url(self, url):
		raw_data = requests.get(url)
		raw_data.encoding = 'utf-8'
		if raw_data.status_code != 200:
			raw_data.raise_for_status()
			return False
		try:
			if isinstance(raw_data.text, unicode):
				warnings.warn('Object returned is of type unicode. Cannot parse to str in Python 2.')
		except NameError:
			pass
		return raw_data.json()

