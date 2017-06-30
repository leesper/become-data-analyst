library(ggplot2)

# exer 1
p1 <- ggplot(data=diamonds, aes(x=log(price)))
p1 + geom_histogram(aes(fill=cut)) + 
  facet_wrap(~color) + 
  scale_fill_brewer(type='qual')

# exer 2
p2 <- ggplot(data=diamonds, aes(x=table, y=price))
p2 + geom_point(aes(color=cut)) + 
  scale_fill_brewer(type='qual')

# exer 4
library(dplyr)
diamondsWithVolume <- mutate(diamonds, volume=x*y*z)
p3 <- ggplot(data=subset(diamondsWithVolume, volume <= quantile(diamondsWithVolume$volume, prob=.99)), aes(x=volume, y=price, color=clarity))
p3 + geom_point() + scale_y_log10() + scale_color_brewer(type='div')

# exer 5
pf$prop_initiated <- pf$friendships_initiated/pf$friend_count

# exer 6
pf$year_joined <- floor(2014 - pf$tenure / 365)
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))
p4 <- ggplot(data=subset(pf, !is.na(year_joined.bucket)), aes(x=tenure, y=prop_initiated))
p4 + geom_line(aes(color=year_joined.bucket), stat='summary', fun.y=median)

# exer 7
p4 <- ggplot(data=subset(pf, !is.na(year_joined.bucket)), aes(x=7 * round(tenure / 7), y=prop_initiated))
p4 + geom_line(aes(color=year_joined.bucket), stat='summary', fun.y=median) + 
  geom_smooth(aes(color=year_joined.bucket), se=FALSE)

# exer 9
pfAbove2012 <- pf %>% filter(year_joined > 2012) 
summary(pfAbove2012$prop_initiated)

# exer 10
p5 <- ggplot(data=diamonds, aes(x=cut, y=price/carat)) 
p5 + geom_jitter(aes(color=color)) + 
  facet_wrap(~clarity) + 
  scale_color_brewer(type='div')






  