library(dplyr)

# Load original data
originalData <- read.csv('prosperLoanData.csv', na.strings = c('', 'NA'))

subData <- select(originalData,
                  LoanOriginationDate,
                  LoanStatus,
                  BorrowerState,
                  Occupation)

write.table(subData, sep=',', file='prosperSubData.csv', col.names = TRUE, row.names = FALSE)
