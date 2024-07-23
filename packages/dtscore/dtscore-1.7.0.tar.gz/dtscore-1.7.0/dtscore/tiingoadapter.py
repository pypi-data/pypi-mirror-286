"""
    IEX adapter

    Latest EOD
    https://api.tiingo.com/tiingo/daily/<ticker>/prices

    Historical EOD
    https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1
"""
import datetime as dt
import json
from collections import namedtuple
from typing import Optional
from dtscore import logging as _log
from urllib import parse as urlp

import requests
from domain import Quote

"""
 * URL examples
 *      # Meta Data
 *      https://api.tiingo.com/tiingo/daily/<ticker>
 *      
 *      # Latest Price
 *      https://api.tiingo.com/tiingo/daily/<ticker>/prices
 *      
 *      # Historical Prices
 *      https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1 
 *
 *  EOD
 *      # docs: https://www.tiingo.com/documentation/endDate-of-day
 *      
 *      # Latest Price Information
 *      https://api.tiingo.com/tiingo/daily/<ticker>/prices
 *      
 *      # Historical Price Information
 *      https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-01-01&endDate=2016-01-01&format=csv&resampleFreq=monthly
 *      
 *  SPLITS
 *      # docs: https://www.tiingo.com/documentation/corporate-actions/splits
 *      
 *      # Splits for all equities that occured or will occur on the exDate.
 *      https://api.tiingo.com/tiingo/corporate-actions/splits
 *
 *      # For specific ticker, all splits following the startExDate (future date or historical date)
 *      https://api.tiingo.com/tiingo/corporate-actions/<TICKER>/splits?startExDate=2023-08-25
 *
 *  TICKERS
 *      a zipped CSV file
 *      https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip

"""

"""
 *  [
 *      {
 *          "date":"2019-01-02T00:00:00.000Z",
 *          "close":157.92,
 *          "high":158.85,
 *          "low":154.23,
 *          "open":154.89,
 *          "volume":37039737,
 *          "adjClose":157.92,
 *          "adjHigh":158.85,
 *          "adjLow":154.23,
 *          "adjOpen":154.89,
 *          "adjVolume":37039737,
 *          "divCash":0.0,
 *          "splitFactor":1.0
 *      },
 *      ...
 *  ]
"""
# namedtuple to match the internal signature of urlunparse
Components = namedtuple(
    typename='Components', 
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)

_scheme = "https"
_netloc = "api.tiingo.com"
_path = "tingo/daily/{0}/prices"
_token = "8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"


URL_PREFIX = r"https://api.tiingo.com/tiingo/daily/"
URL_SUFFIX = r"/prices?token=8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"

def latesteodquote(symbol:str) -> Optional[Quote]:
    """ Get the latest eod quote for <symbol> from Tiingo """
    query_params = {
        'token': _token
    }
    jsondoc = query_equityprices(symbol, query_params)
    # json document is returned with one quote element
    quote = to_quotes(jsondoc)[0]
    return quote

# ----------------------------------------------------------------------------------------------------
def latesteodclose(symbol:str) -> float:
    """ Get the latest closing price for <symbol> from Tiingo."""
    quote = latesteodquote(symbol)
    return quote['close']

def quotefordate(symbol:str, adate:dt.date) -> Optional[Quote]:
    quotes = quotesfordaterange(symbol, adate, adate)
    return quotes[0]

def quotesfordaterange(symbol:str, startdate:dt.date, enddate:dt.date) -> Optional[list[Quote]]:
    query_params = {
        'startDate': str(startdate),
        'endDate': str(enddate),
        'token': _token
    }
    jsondoc = query_equityprices(symbol, query_params)
    quotes = to_quotes(jsondoc)
    return quotes

def to_quotes(jsondoc:list[dict]) -> list[Quote]:
    def makequote(d:dict) -> Quote:
        quotedate = dt.datetime.fromisoformat(d['date']).date()
        quote = Quote(quotedate, d['close'], d['high'], d['low'], d['open'], d['volume'],
            d['adjClose'], d['adjHigh'], d['adjLow'], d['adjOpen'], d['adjVolume'],
            d['divCash'], d['splitFactor']
        )
        return quote

    quotes = [ makequote(d) for d in jsondoc ]
    return quotes

# ----------------------------------------------------------------------------------------------------
def normalize(symbol:str) -> str:
    """ Normalize to database convention - symbol components separated by space. """
    return symbol.replace('-', ' ')

# ----------------------------------------------------------------------------------------------------
def denormalize(symbol:str) -> str:
    """ Denormalize to Tiingo convention - symbol components separated by dash. """
    return symbol.replace(' ','-')

def query_equityprices(symbol, query_params) -> list[dict[str,object]]:
    denorm_symbol = denormalize(symbol)
    components = Components(
        scheme=_scheme,
        netloc=_netloc,
        url=_path.format(denorm_symbol),
        path=None,
        query=query_params,
        fragment=None)
    try:
        full_url = urlp.urlunparse(components=components)
        response = requests.get(full_url)
        jsondocument = json.loads(response.text)
        return jsondocument
    except Exception as e:
        #log.error(f'Exception: url: {full_url}, respons: {response}, error: {type(e)}, {e}')
        raise

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('This file cannot be run as a script')
else:
    log = _log.get_log(__name__, _log.DEBUG)
