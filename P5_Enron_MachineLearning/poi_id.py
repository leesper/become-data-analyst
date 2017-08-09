#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = [
'poi',
'bonus',
'deferral_payments',
'deferred_income',
'director_fees',
'exercised_stock_options',
'expenses',
'from_messages',
'from_poi_to_this_person',
'from_this_person_to_poi',
'loan_advances',
'long_term_incentive',
'other',
'restricted_stock',
'restricted_stock_deferred',
'salary',
'shared_receipt_with_poi',
'to_messages',
] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
### Task 3: Create new feature(s)
# TODO: try to find some advanced features from email data
for k in data_dict.keys():
    from_this_person_to_poi = data_dict[k]['from_this_person_to_poi']
    from_messages = data_dict[k]['from_messages']
    from_poi_to_this_person = data_dict[k]['from_poi_to_this_person']
    to_messages = data_dict[k]['to_messages']
    shared_receipt_with_poi = data_dict[k]['shared_receipt_with_poi']
    data_dict[k]['from_this_person_to_poi_ratio'] =  from_this_person_to_poi * 1.0 / from_messages if from_this_person_to_poi != 'NaN' and from_messages != 'NaN' else 'NaN'
    data_dict[k]['from_poi_to_this_person_ratio'] =  from_poi_to_this_person * 1.0 / to_messages if from_poi_to_this_person != 'NaN' and to_messages != 'NaN' else 'NaN'
    data_dict[k]['shared_receipt_with_poi_ratio'] = shared_receipt_with_poi * 1.0 / to_messages if shared_receipt_with_poi != 'NaN' and to_messages != 'NaN' else 'NaN'

### Store to my_dataset for easy export below.
my_dataset = data_dict
features_list.append('from_this_person_to_poi_ratio')
features_list.append('from_poi_to_this_person_ratio')
features_list.append('shared_receipt_with_poi_ratio')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
#TODO : some feature selection operation

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
