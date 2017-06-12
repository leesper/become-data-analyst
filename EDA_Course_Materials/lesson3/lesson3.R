getwd()
setwd('/home/leesper/become-data-analyst/EDA_Course_Materials/lesson3/')
pf = read.csv('pseudo_facebook.tsv', sep='\t')

library(ggplot2)
names(pf)

qplot(data=pf, x=dob_day) +
  scale_x_continuous(breaks=1:31) + 
  facet_wrap(~dob_month, ncol = 3)

qplot(data = pf, x = friend_count, xlim = c(0, 1000))

qplot(data = pf[!is.na(pf$gender),], x = friend_count, binwidth = 10) +
  scale_x_continuous(limits=c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender, ncol = 2)

by(pf$friend_count, pf$gender, summary)

qplot(x = tenure, data = pf, binwidth = 30, color = I('black'), fill = I('#099DD9'))

qplot(x = tenure / 365, data = pf, binwidth = .25, color = I('black'), fill = I('#099DD9')) +
  scale_x_continuous(breaks = seq(1, 7, 1), lim = c(0, 7))

qplot(x = tenure / 365, data = pf, 
      xlab = 'Number of years using Facebook',
      ylab = 'Number of users in sample',
      color = I('black'), fill = I('#F79420')) +
  scale_x_continuous(breaks = seq(1, 7, 1), lim = c(0, 7))

qplot(x = age, data = pf, binwidth = 1,
      xlab = 'Age of Facebook users',
      ylab = 'Number of usersin sample',
      color = I('black'), fill = I('#F79420')) +
  scale_x_continuous(breaks = seq(0, 120, 10), lim = c(0, 120))

 

qplot(x = friend_count, data = pf)

summary(pf$friend_count)

summary(log10(pf$friend_count+1))

library(gridExtra)
p1 <- qplot(x = friend_count, data = pf)
p2 <- qplot(x = log10(friend_count+1), data = pf)
p3 <- qplot(x = sqrt(friend_count), data = pf)
grid.arrange(p1, p2, p3, ncol=1)

p1 <- ggplot(aes(x = friend_count), data = pf) + geom_histogram()
p2 <- p1 + scale_x_log10()
p3 <- p1 + scale_x_sqrt()
grid.arrange(p1, p2, p3, ncol=1)

qplot(x = www_likes, data = subset(pf, !is.na(gender)),
      xlab = 'www likes', ylab = 'proportion of users with that likes',
      geom = 'freqpoly', color = gender) + 
  scale_x_continuous() +
  scale_x_log10()

by(pf$www_likes, pf$gender, sum)





