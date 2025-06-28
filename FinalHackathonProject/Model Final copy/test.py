
import main

# IMPORT THE LIBRARY
import yfinance as yf
from datetime import datetime
import numpy as np


# CREATE TICKER INSTANCE FOR AMAZON
#Initialize API
GOOG = yf.Ticker("GOOG")
#Make the end date the current day
end_date = datetime.now().strftime('%Y-%m-%d')
#Pull Stock Price History
goog_hist = GOOG.history(start='2017-01-01',end=end_date)



goog_close = goog_hist['Close']
goog_value = goog_close.values
goog_value = goog_value.reshape(-1,1)

print(goog_value[-50:])


last50 = goog_value[-50:]
for i in range(10):
    output = main.main(model="./Goog.keras", array=last50[-50:])
    last50 = list(last50)
    last50.append(output)
    last50 = np.array(last50)



print(last50[-10:])