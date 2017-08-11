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
] # total_stock_value and total_payments are strongly related with others, so remove them

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
### Task 3: Create new feature(s)
for k in data_dict.keys():
    from_this_person_to_poi = data_dict[k]['from_this_person_to_poi']
    from_messages = data_dict[k]['from_messages']
    from_poi_to_this_person = data_dict[k]['from_poi_to_this_person']
    to_messages = data_dict[k]['to_messages']
    shared_receipt_with_poi = data_dict[k]['shared_receipt_with_poi']
    data_dict[k]['from_this_person_to_poi_ratio'] =  from_this_person_to_poi * 1.0 / from_messages if from_this_person_to_poi != 'NaN' and from_messages != 'NaN' else 'NaN'
    data_dict[k]['from_poi_to_this_person_ratio'] =  from_poi_to_this_person * 1.0 / to_messages if from_poi_to_this_person != 'NaN' and to_messages != 'NaN' else 'NaN'

### Store to my_dataset for easy export below.
my_dataset = data_dict
features_list.append('from_this_person_to_poi_ratio')
features_list.append('from_poi_to_this_person_ratio')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# get rid of features scored lower than 2.0 by SelectKBest:
# (to_messages, deferral_payments, from_messages, restricted_stock_deferred)
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
selector = SelectKBest(f_classif, k='all')
selector.fit(features, labels)
score_feature = zip(selector.scores_, features_list[1:])
features_list = ['poi']
for t in sorted(score_feature, key=lambda x: x[0], reverse=True):
    if t[0] >= 2.0:
        features_list.append(t[1])

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split
from tester import test_classifier

classifiers = [
    GridSearchCV(GaussianNB(), param_grid=dict()),
]

for i in range(2, len(features_list)+1):
    sub_features_list = features_list[:i]
    sub_data = featureFormat(my_dataset, sub_features_list, sort_keys = True)
    sub_labels, sub_features = targetFeatureSplit(sub_data)
    sub_features_train, sub_features_test, sub_labels_train, sub_labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)
    for sub_clf in classifiers:
        sub_clf.fit(sub_features_train, sub_labels_train)
        test_classifier(sub_clf, my_dataset, sub_features_list)


# for a in algorithms:
#     pipeline = Pipeline([("pca", PCA()), a["clf"]])
#     param_grid = dict(pca__n_components=[1, 3, 5, 7, 9])
#     if a["params"] is not None:
#         param_grid.update(a["params"])
#     clf = GridSearchCV(pipeline, param_grid=param_grid)
#     clf.fit(features, labels)
#     print 'best', clf.best_params_

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
