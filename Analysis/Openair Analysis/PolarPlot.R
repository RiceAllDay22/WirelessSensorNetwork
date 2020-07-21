library(openair)
mydata = read.csv('example.csv', header = TRUE)
mydata$date = as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M", tz ="GMT"))
subdata = subset(mydata, as.numeric(rownames(mydata)) < 10000,select = c(date, ws, wd, nox, no2))


########## Polar Plot ##########

testdata = subset(mydata, as.numeric(rownames(mydata)) < 20,
                  na.drop = TRUE,
                  #mydata$date < as.Date("1998-01-02"),
                  select = c(date, ws, wd, nox, no2))

polarPlot(mydata, statistic = 'cpf', k =10, pollutant = 'nox')
polarPlot(mydata, statistic = 'cpf')

polarPlot(mydata, pollutant = 'no2', min.bin = 1,
          uncertainty = TRUE,
          type = 'daylight')


polarPlot(mydata, statistic = 'nwr', pollutant = 'no2')
polarPlot(mydata, statistic = 'cpf', pollutant = 'no2')
c = polarPlot(mydata, pollutant = 'no2')
print(a, split = c(1, 1, 2, 1))
print(b, split = c(2, 1, 2, 1), newpage = FALSE)


########## Conditional Probability Function ##########



polarPlot(mydata, pollutant = 'nox')
