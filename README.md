# chart_pattern_detection
Scrapes Yahoo finance data and finds [triangle patterns](https://www.investopedia.com/articles/technical/03/091003.asp) using the idea of local maximums and minimums. (Last updated Feb 2018) This was later used in my internship to train a CNN to detect technical patterns. Not the most accurate, but an initial jump to working with financial time series data. 

# The Approach
**Data Retrieval**
-------------------
To analyze the charts, I first needed to import a stock’s data. To do this, I simply
referenced these two links,
[http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/](http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/)
https://bokeh.pydata.org/en/latest/docs/gallery/candlestick.html
which effectively enabled me to import and use the data. Integrating them together was
simple; the yahoo finance data came within a .csv file, and a conversion into a data frame
was all that was needed to use a bokeh graph. Below is the output received, in an HTML
file. I will use JNJ as an example throughout this documentation.


**Recognition**
-------------------
Upon further research of the triangle pattern, there were three distinct
characteristics of the trend:

1. The prices in between often oscillated between the top and the bottom line.
2. The top line was positive, and the bottom line was negative.
3. The triangle pattern occurs locally (only in a certain part of the graph).

**Initial Thoughts**
-------------------
Although I’ve had some experience in Convoluted Neural Networks using Matlab
in one of my engineering classes, I decided against using it due to a lack of in-depth
knowledge. In addition, the triangle pattern seemed unambiguous enough using the data
given. With that, I attempted to use the properties of the triangle trend to make an
efficient analysis.

**Finding the Swings**
-------------------
An important part of the triangle pattern is the oscillating nature of the graphs.
The data imported from Yahoo Finance included the highs and the lows from each day,
so I decided to find the maximums of the high dataset and the minimums of the low
dataset. This indicates the oscillating nature of the graph and where that can be found.
Below, these maximums and minimums are indicated by the blue circles.

![Finding the Swings](/images/readme_im1.png)

**Finding Potential Lines**
-------------------
Starting with the top part of the triangle, I knew that the line had to connect two
points of data and the slope of the line also had to be negative. With this, it would
connect oscillating sections of the graph together. Obviously, finding all combinations of
a negative line would be ineffective, so I used more parameters. For each maximum
(found above), I set a minimum and maximum amount of days that the line could reach.
With this, I had an abundance of possible lines for the top portion of the triangle. I could
use the same method for the minimums to find a large set of possible bottom lines for
the triangle trend. In the image below, the orange lines indicate the top portions of a
possible triangle and the blue lines indicate the bottom portion.

![Finding Potential Lines](/images/readme_im2.png)

**Finding Corresponding Lines**
-------------------
It is obvious that not all of those lines are a great fit for a triangle trend, so by
corresponding the blue lines to orange lines, it is possible to match up a good fitting
triangle that has oscillating maximums and minimums, which is an integral part of the
triangle. By finding lines that start at a similar date and end at a similar date, it is possible
to find a good match for a triangle trend.

![Finding Corresponding Lines](/images/readme_im3.png)

**Running the Program**
-------------------
First, make sure that get-yahoo-quotes.py is built. To run the program, simply
type in the stock symbol in line 16 of CandlestickGrapher.py and execute it. If everything
runs smoothly, a .csv file should be created, and an .html file should also appear as well
with the graph and triangle trend.

**Examples** 
-------------------
Some examples (JNJ, SBUX, NVDA) from 09/04/2018 to 02/21/2019. 
![JNJ-20180904-20190221](/examples/JNJ-20180904-20190221.png)
![SBUX-20180904-20190221](/examples/SBUX-20180904-20190221.png)
![NVDA-20180904-20190221](/examples/NVDA-20180904-20190221.png)
