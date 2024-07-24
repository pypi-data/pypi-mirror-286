from urllib import parse as urlp
from collections import namedtuple
import datetime as dt

# namedtuple to match the internal signature of urlunparse
Components = namedtuple(
    typename='Components', 
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)

token = "8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"
path = "tingo/daily/{0}/prices"

def test(symbol, start, end):
    url = r"https://api.tiingo.com/tiingo/daily/aapl/prices?startDate=2012-1-1&endDate=2016-1-1&token=8e72f6389299e266776d96f55d0d5c3dbb8eb9e4"
    p_url = urlp.urlparse(url)
    print(p_url)


    query_params = {
        'startDate': str(start),
        'endDate': str(end),
        'token': token
    }
    c_url = urlp.urlunparse(
        Components(
            scheme='https',
            netloc='api.tiingo.com',
            url=path.format(symbol),
            path='',
            query=urlp.urlencode(query_params),
            fragment=None
        )
    )
    print(c_url)

    c_url2 = urlp.urlunparse(
        [ 'https', 'api.tiingo.com', path.format(symbol), None, urlp.urlencode(query_params), None ]
    )
    print(c_url2)

test("aapl",dt.datetime(2024,7,1).date(), dt.datetime(2024,7,20).date())