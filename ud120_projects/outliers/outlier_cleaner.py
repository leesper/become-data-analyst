#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    diff = [(i, (predictions[i] - net_worths[i])[0]) for i in range(len(predictions))]
    diff = sorted(diff, key=lambda x: x[1])
    for t in diff:
        cleaned_data.append((ages[t[0]], net_worths[t[0]], t[1]))
	if len(cleaned_data) / float(len(ages)) >= 0.9:
            break
    
    return cleaned_data

