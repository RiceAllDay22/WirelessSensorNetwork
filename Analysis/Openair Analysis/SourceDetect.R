########## HELP SECTION ##########
?openair
?plot
?polarPlot

########## Load Data ##########
library(openair)
testdata     = read.csv('2020-07-17--16.csv', header = FALSE)
colnames(testdata)[1:4] = c('UnixTime', 'ws', 'wd', 'co2')
testdata$date           = ISOdatetime(1970,1,1,0,0,0) + testdata$UnixTime 
testdata$UnixTime       = NULL
testdata                = testdata[c(4,1,2,3)]
#testdata$ws[testdata$ws == 0.0] = 0.1

testdata$ws = testdata$ws/5*1.492/2.237
testdata$wd = testdata$wd*22.5

testdata = read.csv('example.csv', header = TRUE)
testdata$date = as.POSIXct(strptime(testdata$date, format = "%d/%m/%Y %H:%M", tz ="GMT"))
testdata = subset(testdata, select = c(date, nox, no2, wd,ws))

########## Edit Data ##########
mean(testdata$co2)
testdata$co2 = testdata$co2 + 500

testdata$wsavg  = filter(testdata$ws, rep(1/10, 10))
testdata$wdavg  = filter(testdata$wd, rep(1/10, 10))
testdata$co2avg = filter(testdata$co2,rep(1/10, 10))

testdata$avg = NULL

pollutant = 'no2'
########## Normal Plot ##########
plot(testdata$ws, type = 'l', col = 'red')
par(new=TRUE)
plot(testdata$wsavg, type = 'l', col = 'blue')

plot(testdata$wd, type = 'l', col = 'red')
par(new=TRUE)
plot(testdata$wdavg, type = 'l', col = 'blue')

plot(testdata$co2, type = 'l', col = 'red')
par(new=TRUE)

########## Create Avg Frame ##########
testdata = subset(testdata, select = c ('date', 'wsavg', 'wdavg', 'co2avg'),
                  na.rm = TRUE)
colnames(testdata)[1:4] = c('UnixTime', 'ws', 'wd', 'co2')

########## Polar Plot ##########
percentileRose(testdata, pollutant = pollutant,
               method = 'cpf', percentile = 80)

polarPlot(testdata, pollutant = 'nox',
          uncertainty = FALSE)
polarPlot(testdata, pollutant = 'co2', statistic = 'nwr')

polarPlot(testdata, pollutant = pollutant, statistic = 'cpf',
          percentile = 90)
          #uncertainty = TRUE, )


polarPlot(testdata, pollutant =  'co2', colors =  'jet', k = 100,
          statistic = 'nwr')
          #resolution = 'default',
          #statistic = 'nwr')

windRose(testdata, wd = 'wd', ws = 'ws')
