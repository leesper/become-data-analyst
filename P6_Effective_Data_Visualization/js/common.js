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
    if (d.Occupation.indexOf("Student") !== -1) {
        d.Occupation = "Student";
    } else if (d.Occupation.indexOf("Pilot") !== -1) {
        d.Occupation = "Pilot";
    } else if (d.Occupation.indexOf("Police") !== -1) {
        d.Occupation = "Police";
    } else if (d.Occupation.indexOf("Engineer") !== -1) {
        d.Occupation = "Engineer";
    } else if (d.Occupation.indexOf("Tradesman") !== -1) {
        d.Occupation = "Tradesman";
    } else if (d.Occupation.indexOf("Sales") !== -1) {
        d.Occupation = "Sales";
    } else if (d.Occupation.indexOf("Driver") !== -1) {
        d.Occupation = "Driver";
    }
    return d;
}

var stateCodes = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
};
