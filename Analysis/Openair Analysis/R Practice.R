list.files()
getwd()
setwd('C:/users/Adriann Liceralde/Desktop/Repo/WirelessSensorNetwork/Analysis/OpenAir Analysis')


mydata = read.csv('example.csv', header = TRUE)
summary(mydata)

mydata$date = as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M", tz ="GMT"))

summary(mydata)
names(mydata)

summary(mydata$nox)
mean(mydata$nox)
mean(mydata$nox, na.rm = TRUE)

hist(mydata$no2, 
     main = 'Histogram of NO2',
     xlab = 'NO2 (ppb)')

newdata = na.omit(mydata)


plot(mydata$date[1:500], mydata$nox[1:500],
     type = 'l',
     xlab = 'date',
     ylab = 'nox (ppb)')

means = aggregate(mydata["nox"], 
                  format(mydata["date"], "%Y-%m"),
                  mean,
                  na.rm = TRUE)

means$date  = seq(min(mydata$date), max(mydata$date), length = nrow(means))

plot(means$date, means[, 'nox'], type = 'l')


means = aggregate(mydata["nox"], 
                  format(mydata["date"], "%Y-%k"),
                  mean,
                  na.rm = TRUE)
plot(means)

#OPENAIR
library(openair)
?openair
?polarPlot


subdata = subset(mydata, as.numeric(rownames(mydata)) < 150,select = c(date, nox, no2, wd,ws))

polarPlot(subdata, fontsize = 20, na.rm = TRUE)

summaryPlot(selectByDate(mydata, year = c(2000, 2001)))

mydata$ws[mydata$ws < 0 ] = NA
summary(mydata)
