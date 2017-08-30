var timeParser = d3.timeParse("%Y-%m-%d %H:%M:%S");

function preprocess(d) {
  d.CreditScore = +d.CreditScore;
  d.DebtToIncomeRatio = +d.DebtToIncomeRatio;
  d.EmploymentStatusDuration = +d.EmploymentStatusDuration;
  d.StatedMonthlyIncome = +d.StatedMonthlyIncome;
  d.YieldIndex = +d.YieldIndex;
  d.LoanOriginationDate = timeParser(d.LoanOriginationDate);
  if (d.LoanStatus.indexOf("Past Due") !== -1) {
    d.LoanStatus = "Past Due";
  }
  return d;
}
