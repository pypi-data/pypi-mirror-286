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
from typing import Optional, Any
from dtscore import logging as _log
from urllib import parse as urlp

import requests
from dtscore.domain import Quote

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
_path = "tiingo/daily/{0}/prices"
_token = "8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"


URL_PREFIX = r"https://api.tiingo.com/tiingo/daily/"
URL_SUFFIX = r"/prices?token=8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"

#
#   Public API
#

# ----------------------------------------------------------------------------------------------------
def latesteodquote(symbol:str) -> Optional[Quote]:
    """ Get the latest EOD quote for <symbol> from Tiingo """
    query_params = {
        'token': _token
    }
    jsondoc = _query_tiingo_bysymbol(symbol, query_params)
    # json document containing a list of tiingo json quotes  is returned,
    # possibly with one quote element
    if len(jsondoc) > 0:
        quote = _to_quotes(jsondoc)[0]
        return quote
    else:
        print(f"warning - unable to get latest quote for {symbol}. Is the symbol correct?")
        return None

# ----------------------------------------------------------------------------------------------------
def latesteodclose(symbol:str) -> Optional[float]:
    """ Get the latest closing price for <symbol> from Tiingo. """
    quote = latesteodquote(symbol)
    return quote.close if quote is not None else None 

# ----------------------------------------------------------------------------------------------------
def quotefordate(symbol:str, adate:dt.date) -> Optional[Quote]:
    """ Get the EOD quote for the given <symbol> and <adate> from Tiingo. """
    quotes = quotesfordaterange(symbol, adate, adate)
    return quotes[0] if len(quotes) > 0 else None

# ----------------------------------------------------------------------------------------------------
def quotesfordaterange(symbol:str, startdate:dt.date, enddate:dt.date) -> Optional[list[Quote]]:
    """ Get all EOD quotes for the given symbol and dates range from Tiingo. """
    query_params = {
        'startDate': str(startdate),
        'endDate': str(enddate),
        'token': _token
    }
    jsondoc = _query_tiingo_bysymbol(symbol, query_params)
    quotes = _to_quotes(jsondoc)
    return quotes

# ----------------------------------------------------------------------------------------------------
def normalize(symbol:str) -> str:
    """ Normalize to database convention - symbol components separated by space. """
    return symbol.replace('-', ' ')

# ----------------------------------------------------------------------------------------------------
def denormalize(symbol:str) -> str:
    """ Denormalize to Tiingo convention - symbol components separated by dash. """
    return symbol.replace(' ','-')


#
#   Private api
#

# ----------------------------------------------------------------------------------------------------
def _to_quotes(jsondoc:list[dict]) -> list[Quote]:
    """ Convert a list of Tiingo json quotes to a list of domain Quote objects. """
    def buildquote(d:dict) -> Quote:
        quotedate = dt.datetime.fromisoformat(d['date'].replace('Z','+00:00')).date()
        quote = Quote(date=quotedate, close=d['close'], high=d['high'], low=d['low'], open=d['open'], volume=d['volume'],
            adjClose=d['adjClose'], adjHigh=d['adjHigh'], adjLow=d['adjLow'], adjOpen=d['adjOpen'], adjVolume=d['adjVolume'],
            divCash=d['divCash'], splitFactor=d['splitFactor']
        )
        return quote

    quotes = [ buildquote(d) for d in jsondoc ]
    return quotes

# ----------------------------------------------------------------------------------------------------
def _query_tiingo_bysymbol(symbol:str, query_params:dict[str,Any]) -> list[dict[str,Any]]:
    """ Query Tiingo api by symbol and query parameters. """
    denorm_symbol = denormalize(symbol)
    components = Components(
        scheme=_scheme,
        netloc=_netloc,
        url=_path.format(denorm_symbol),
        path=None,
        query=urlp.urlencode(query_params),
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
