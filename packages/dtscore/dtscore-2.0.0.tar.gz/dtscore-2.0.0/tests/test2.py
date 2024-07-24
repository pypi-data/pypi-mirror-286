
from dtscore import tiingoadapter as ti
from dtscore import domain
import datetime as dt

closeprice = ti.latesteodclose('aapl')
print(closeprice)

quote = ti.latesteodquote('aapl')
print(quote)

quote = ti.quotefordate('aapl', dt.datetime(2024,1,4).date())
print(quote)

start = dt.datetime(2024,1,4).date();
end = dt.datetime(2024,1,10).date()
quotes = ti.quotesfordaterange('aapl', start, end)
for q in quotes: print(q)