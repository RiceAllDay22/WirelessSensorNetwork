library(openair)
mydata = read.csv('example.csv', header = TRUE)
mydata$date = as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M", tz ="GMT"))

subdata = subset(mydata, as.numeric(rownames(mydata)) < 50,select = c(date, nox, no2, wd,ws))

subtestdata = subset(mydata, mydata$ws < 0)

#Summary Plot
summaryPlot(selectByDate(mydata))
summaryPlot(selectByDate(mydata, year = c(2000,2001), month = c(seq(1,10))),
            period = 'months',
            col.trend = 'BLACK',
            col.data  = 'GREEN')


#Scatter Plot
scatterPlot(mydata, x = 'nox', y = 'no2', z = 'wd',
            type = 'year')


#Time Variation
timeVariation(subdata, pollutant = 'nox', 
              local.tz = 'Europe/London')
#wiki list tz database
?timeVariation


#Trend Level
trendLevel(mydata,
           rotate.axis = c(45,0))


#Smooth Trend
smoothTrend(mydata, pollutant = 'no2')



#Calendar Plot
calendarPlot(mydata, pollutant = 'no2', year = 2003, 
             annotate = 'wd',
             main = 'Polluant')

#Wind Rose
windRose(mydata, wd = 'wd', ws = 'ws')
?windRose


#Polar Annulus
polarAnnulus(subdata, pollutant = 'nox')

#Polar Plot
subdata = subset(mydata, as.numeric(rownames(mydata)) < 150,select = c(date, nox, no2, wd,ws))
polarPlot(subdata, pollutant = 'nox', type = 'year')
?polarPlot

rm(subtestdata)

testdata = timeAverage(mydata, avg.time = 'month')

polarPlot(subdata, pollutant = 'nox', type = 'year',
          cols = 'jet', statistic = 'cpf')

?polarPlot



#Import Function
import('example.csv', date = 'date')


testdata = read.csv('example.csv', header = TRUE)
# Multiple Plots
mydata = read.csv('example.csv', header = TRUE)
subdata = subset(mydata, as.numeric(rownames(mydata)) < 10000,select = c(date, nox, no2, wd,ws))
a = polarPlot(subdata, pollutant =  'no2', colos = 'jet', resolution = 'fine')
b = polarPlot(subdata, pollutant =  'no2', colos = 'jet', statistic = 'cpf', percentile = c(95, 100))
print(a, split = c(1, 1, 2, 1))
print(b, split = c(2, 1, 2, 1), newpage = FALSE)

?polarPlot
