library(ggplot2)

flighttxt <- '
miles price
337 59.5
2565 509.5
967 124.5
5124 1480.4
2398 696.23
2586 559.5
7412 1481.5
522 474.5
1499 737.5
'
flight <- read.table(header=T, text=flighttxt)

ggplot(data=flight, aes(x=miles, y=price)) + geom_point()

cor.test(flight$miles, flight$price)