# cryCompare
Python wrapper for Crypto Compare public API

Following requests are supported:
- CoinList
- Price
- PriceHistorical
- CoinSnapshot
- CoinSnapshotFullById
- HistoMinute
- HistoHour
- HistoDay

Wrapper requires following python modules:
- requests

Requests are devided into two classes:
- Price
- History

Price class methods: price, priceMulti, priceMultiFull, generateAvg, dayAvg, priceHistorical, coinSnapshot, coinSnahpshotFullById.
For detailed documentation visit CryptoCompare API website.

History class methods: histoMinute, histoHour, histoDay
For detailed documentation visit CryptoCompare API website.

CryptoCompare API Documentation can be found at https://www.cryptocompare.com/api/#introduction

