from math import pi

import pandas as pd
import numpy as np
import os

from bokeh.plotting import figure, show, output_file


#Self Identified Triangle Pattern stocks
#AAPL, JNJ, CAT, NVDA
#------------------------------------------------
#-----------USER INPUT---------------------------
#------------------------------------------------
#Symbol to be called
symbol = 'JNJ'

#The minimum that the line must extend
line_len_min = 2
line_dist = 2
#The maximum that a line can extend
day_diff = 17

#When matching up the lines, this is the difference in days that the
#lines are able to extend
match_diff_start = 2
match_diff_end = 2
#------------------------------------------------

#Calls the script to get a csv with stock data from x days ago,
#If you want to change the amount of days, have to edit under
#download_quotes() in get-yahoo-quotes
os.system('python get-yahoo-quotes.py ' + symbol)


#Dataframe used for indices as follows
df = pd.read_csv(symbol+'.csv')
df["Date"] = pd.to_datetime(df["Date"])

#Access the dataframe for reading
#print(df)

inc = df.Close > df.Open
dec = df.Open > df.Close
w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = symbol+" Candlestick")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

#actual candlestick creator
#p.segment(df.date, df.high, df.date, df.low, color="black")
p.segment(df.Date, df.High, df.Date, df.Low, color="black")


#Creates the candlesticks, for each bar there
p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#00ff00", line_color="black")
p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#FF0000", line_color="black")


#Create an numpy array for highs, lows, and dates from DataFrame
highs = np.array(df['High'])
lows = np.array(df['Low'])
dates = np.array(df['Date'])
days = highs.size

#Print the number of days of the data
print("Days in data:", days)

#Connects all of the highs together and lows together
#p.line(dates, highs)
#p.line(dates, lows)


#----------------Find the Swings-----------------------------
#Stores the day(index) at which a max/min is found
#Will create a dataframe of this later
max_prices = []
max_dates = []
max_days = []
min_prices = []
min_dates = []
min_days = []
#This for loop will find the peak of the highs
#This also signifies a swing pattern throughout the days
for x in range(1, days-1):
    if highs[x-1] < highs[x] > highs[x+1] or x == 1:
        #p.circle(dates[x],highs[x])
        max_prices.append(highs[x])
        max_dates.append(dates[x])
        max_days.append(x)

for y in range(1, days-1):
    if lows[y-1] > lows[y] < lows[y+1]:
        #p.circle(dates[y],lows[y])
        min_prices.append(lows[y])
        min_dates.append(dates[y])
        min_days.append(y)
#--------------------------------------------------------
#p.line([min_dates], [min_prices], color = "black")

#------------------Find Possible Lines-------------------
#find all the combinations from a positive to a negative slope and draw that line
#we only care about localized regions, so we can edit that with line_len_min/day_diff
max_days_size = len(max_prices)
start_day_max = []
start_date_max = []
start_price_max = []
end_day_max = []
end_date_max = []
end_price_max = []


#Find possible lines that are negatively sloping and fall within the range
for x in range(max_days_size-line_len_min):
    #graph every slope that creates a negative within our range
    start_day = max_days[x]
    final_day = start_day + line_len_min + day_diff
    for y in range(x+line_len_min, max_days_size):
        if(max_prices[x]<=max_prices[y]):
            break
        #x signifies a starting point, y will signify the 5 points in between
        if(max_days[y] < final_day):
            #Make sure intermediate prices are less than initial day
            change_in_price = max_prices[y] - max_prices[x]
            if(change_in_price <= 0):
                #p.line([max_dates[x],max_dates[y]],[max_prices[x],max_prices[y]], color = "orange");
                #add this data to the arrays
                start_day_max.append(max_days[x])
                start_date_max.append(max_dates[x])
                start_price_max.append(max_prices[x])
                end_day_max.append(max_days[y])
                end_date_max.append(max_dates[y])
                end_price_max.append(max_prices[y])




#Repeat the same process as above
min_days_size = len(min_prices)
start_day_min = []
start_date_min = []
start_price_min = []
end_date_min = []
end_day_min = []
end_price_min = []
for x in range(min_days_size-line_len_min):
    #graph every slope that creates a positive within 5 points
    start_day = min_days[x]
    final_day = start_day + line_len_min+day_diff
    for y in range(x+line_len_min, min_days_size):
        if(min_prices[x]>=min_prices[y]):
            break
        #x signifies a starting point, y will signify the 5 points in between
        if(min_days[y] < final_day):
            #Make sure intermediate prices are less than initial day
            change_in_price = min_prices[y] - min_prices[x]
            if(change_in_price > 0):
                #p.line([min_dates[x],min_dates[y]],[min_prices[x],min_prices[y]], color = "blue");
                start_day_min.append(min_days[x])
                start_date_min.append(min_dates[x])
                start_price_min.append(min_prices[x])
                end_day_min.append(min_days[y])
                end_date_min.append(min_dates[y])
                end_price_min.append(min_prices[y])
#-------------------------------------------------------------------------

#-------------Find Matches----------------------------------------------
#Try to match the starts and the ends of each parameter, with a range of each
num_lines_max = len(start_day_max)
num_lines_min = len(start_day_min)
force_start = 0
for x in range(num_lines_max):
    #go through each of the lines to meet these parameters:
    #1! starting day of min and max must be +-x days apart (use abs())
    #2! ending day of min and max must be +-x days apart
    #match_diff_start
    #match_diff_end
    #Make sure that we don't repeat by setting another parameter: our start day must be
    #larger than force_start, so our lines won't overlap
    for y in range(num_lines_min):
        if(start_day_max[x] < force_start > start_day_min[y]):
            break
        #parameters used to identify a correct line
        if(abs(start_day_max[x]-start_day_min[y]) <= match_diff_start and
        abs(end_day_max[x]-end_day_min[y]) <= match_diff_end and start_day_max[x] > force_start+line_dist < start_day_min[y]):
            p.line([start_date_max[x],end_date_max[x]],[start_price_max[x],end_price_max[x]],line_width = 3, color = 'black')
            p.line([start_date_min[y],end_date_min[y]],[start_price_min[y],end_price_min[y]],line_width = 3, color = 'black')
            force_start = start_day_max[x]


#--------------------------------------------------------------------------

#Output
output_file("candlestick.html", title="candlestick.py example")
show(p)  # open a browser
