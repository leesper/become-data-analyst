getwd()
setwd('/home/likejun/become-data-analyst/EDA_Course_Materials/lesson3/')
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
  scale_x_continuous(breaks = seq(1, 7, 1), limits = c(0, 7))