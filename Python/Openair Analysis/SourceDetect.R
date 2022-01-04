########## HELP SECTION ##########
?openair
?plot
?polarPlot


########## Load Data ##########
library(openair)
file = 'PostFallsTest.csv'
file = '2020-07-22--09.csv'
testdata                = read.csv(file, header = FALSE)
colnames(testdata)[1:4] = c('UnixTime', 'ws', 'wd', 'co2')
testdata$date           = ISOdatetime(1970,1,1,0,0,0) + testdata$UnixTime 
testdata$UnixTime       = NULL
testdata                = testdata[c(4,1,2,3)]
#testdata$ws[testdata$ws == 0.0] = 0.1

pollutant = 'co2'
testdata$ws = testdata$ws/5*2.25

#testdata$ws = testdata$ws/5*1.492/2.237
#testdata$wd = testdata$wd*22.5


########## Edit Data ##########
mean(testdata$co2)
testdata$co2 = testdata$co2 + 500

testdata$wsavg  = filter(testdata$ws, rep(1/10, 10))
testdata$wdavg  = filter(testdata$wd, rep(1/10, 10))
testdata$co2avg = filter(testdata$co2,rep(1/100, 100))




########## Normal Plot ##########
plot(testdata$ws, type = 'l', col = 'red')
par(new=TRUE)
plot(testdata$wsavg, type = 'l', col = 'blue')

plot(testdata$wd, type = 'p', col = 'red')
par(new=TRUE)
plot(testdata$wdavg, type = 'l', col = 'blue')

plot(testdata$co2, type = 'l', col = 'red')
par(new=TRUE)
plot(testdata$co2avg, type = 'l', col = 'blue')

minimum = min(testdata$co2)
testdata$co2 = testdata$co2 - minimum


########## Create Avg Frame ##########
testdata = subset(testdata, select = c ('date', 'wsavg', 'wdavg', 'co2avg'),
                  na.rm = TRUE)
colnames(testdata)[1:4] = c('UnixTime', 'ws', 'wd', 'co2')


########## Other Plots ##########
percentileRose(testdata, pollutant = pollutant,
               method = 'cpf', percentile = 90,
               cols = 'darkorange')

windRose(testdata, wd = 'wd', ws = 'ws')

polarAnnulus(testdata, pollutant = pollutant,
             period = 'hour')

########## Polar Plots ##########

polarPlot(testdata, pollutant = pollutant,
          uncertainty = TRUE,
          statistic = 'mean')

polarPlot(testdata, pollutant = pollutant,
          uncertainty = FALSE,
          statistic = 'cpf',
          percentile = 90)



polarPlot(testdata, pollutant = pollutant,
          uncertainty = TRUE,
          statistic = 'cpf',
          percentile = c(50, 65))


polarPlot(testdata, pollutant = pollutant,
          uncertainty = FALSE,
          statistic = 'cpf',
          percentile = c(15, 35))



polarPlot(testdata, pollutant = 'co2', statistic = 'nwr')

polarPlot(testdata, pollutant = pollutant, statistic = 'cpf',
          percentile = 90)
          #uncertainty = TRUE, )


polarPlot(testdata, pollutant =  'co2', colors =  'jet', k = 100,
          statistic = 'nwr')
          #resolution = 'default',
          #statistic = 'nwr')

