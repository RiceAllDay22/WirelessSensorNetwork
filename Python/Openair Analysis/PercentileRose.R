library(openair)
mydata = read.csv('example.csv', header = TRUE)
mydata$date = as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M", tz ="GMT"))
subdata = subset(mydata, as.numeric(rownames(mydata)) < 10000,select = c(date, ws, wd, nox, no2))


########## Percentile Rose ##########
percentileRose(subdata, cols = 'jet')


percentileRose(mydata, pollutant = 'so2',
               type = 'daylight',
               percentile = c(25, 50, 75, 90, 95, 99, 99.9),
               col = 'brewer1', key.position ='right',
               smooth = TRUE,
               mean.col = 'black')

percentileRose(mydata, pollutant = 'nox',
               percentile = 95, method = 'cpf',
               col = 'darkorange', smooth = TRUE)


########## Polar Freq ########## 
polarFreq(mydata)





a = percentileRose(mydata, pollutant = 'so2')
b = percentileRose(mydata, pollutant = 'co'
                   print(a, split = c(1, 1, 2, 1))
                   print(b, split = c(2, 1, 2, 1), newpage = FALSE)
                   ########## Polar Plot ##########