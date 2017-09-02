var timeParser = d3.timeParse("%Y-%m-%d %H:%M:%S");

// convert strings of number into numeric, combining some kinds of occupations
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

// calculate total count, reshaping data object for easy manipulating
function calculateTotalCategory(data, loanStatus) {
  for (var i = 0; i < data.length; i++) {
    var total = 0;
    for (var j = 0; j < data[i].values.length; j++) {
      var k = data[i].values[j].key;
      var v = data[i].values[j].value;
      data[i][k] = v
      total += v;
    }
    data[i].Category = data[i].key;
    data[i].Total = total;
    delete data[i].key;
    delete data[i].values;

    // add missing loan status
    for (var k = 0; k < loanStatus.length; k++) {
      if (!(loanStatus[k] in data[i])) {
        data[i][loanStatus[k]] = 0;
      }
    }
  }
}

function calculateTotalOccupation(data, status) {
  index = -1
  for (var i = 0; i < data.length; i++) {
    var total = 0;
    for (var j = 0; j < data[i].values.length; j++) {
      var key = data[i].values[j].key;
      var val = data[i].values[j].value;
      total += val;
      data[i][key] = val;
    }
    data[i].Occupation = data[i].key;
    data[i].Total = total;
    delete data[i].key;
    delete data[i].values;
    for (var k = 0; k < status.length; k++) {
      if (!(status[k] in data[i])) {
        data[i][status[k]] = 0;
      }
    }
    if (data[i].Occupation == "NA") {
      index = i;
    }
  }
  if (index != -1) {
    data.splice(index, 1);
  }
}

// group data by key1 and key2
function groupByKeys(key1, key2, data) {
  groupByResult = d3.nest()
    .key(function(d) {
      return d[key1];
    })
    .key(function(d) {
      return d[key2];
    })
    .rollup(function(v) {
      return v.length;
    })
    .entries(data);
  return groupByResult;
}

var loanStatus = ["Completed", "Current", "FinalPaymentInProgress", "Chargedoff", "Defaulted", "Past Due", "Cancelled"];

var stateCodes = {
  "Alabama": "AL",
  "Alaska": "AK",
  "Arizona": "AZ",
  "Arkansas": "AR",
  "California": "CA",
  "Colorado": "CO",
  "Connecticut": "CT",
  "Delaware": "DE",
  "District of Columbia": "DC",
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
