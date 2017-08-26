library(dplyr)

# Load original data
originalData <- read.csv('data/prosperLoanData.csv', na.strings = c('', 'NA'))

# Calculate credit score based on average
originalData$CreditScore <- (originalData$CreditScoreRangeLower+originalData$CreditScoreRangeUpper) / 2.0

# Calculate yield index
originalData$YieldIndex <- originalData$LP_CustomerPrincipalPayments / originalData$LoanOriginalAmount * originalData$LenderYield

# Convert listing categories
originalData$ListingCategory <- factor(originalData$ListingCategory,
                                       levels = c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                                       labels = c('Not Available',
                                                  'Debt Consolidation',
                                                  'Home Improvement',
                                                  'Business',
                                                  'Personal Loan',
                                                  'Student Use',
                                                  'Auto',
                                                  'Other',
                                                  'Baby&Adoption',
                                                  'Boat',
                                                  'Cosmetic Procedure',
                                                  'Engagement Ring',
                                                  'Green Loans',
                                                  'Household Expenses',
                                                  'Large Purchases',
                                                  'Medical/Dental',
                                                  'Motorcycle',
                                                  'RV',
                                                  'Taxes',
                                                  'Vacation',
                                                  'Wedding Loans'))

subData <- select(originalData,
                  LoanOriginationDate,
                  LoanStatus,
                  BorrowerState,
                  ListingCategory,
                  Occupation,
                  EmploymentStatus,
                  EmploymentStatusDuration,
                  StatedMonthlyIncome,
                  DebtToIncomeRatio,
                  CreditScore,
                  YieldIndex)

write.table(subData, file='prosperSubData.csv', col.names = TRUE, row.names = FALSE)
