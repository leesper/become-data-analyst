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

# split into multiple training and test sets, do SelectKBest on them,
# retain features with average score bigger than 3.0
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import StratifiedShuffleSplit

feature_scores = dict()
for feature_name in features_list[1:]:
    feature_scores[feature_name] = []

sss = StratifiedShuffleSplit(n_splits=1000, test_size=0.3, random_state=42)
for train_index, test_index in sss.split(features, labels):
    features_train = []
    labels_train = []
    for ii in train_index:
        features_train.append(features[ii])
        labels_train.append(labels[ii])

    selector = SelectKBest(f_classif, k='all')
    selector.fit(features_train, labels_train)
    feature_score = zip(features_list[1:], selector.scores_)
    for t in feature_score:
        feature_scores[t[0]].append(t[1])

# calculate average scores
for k in feature_scores.keys():
    feature_scores[k] = sum(feature_scores[k])/len(feature_scores[k])
features_list = ['poi']
for k in feature_scores.keys():
    if feature_scores[k] > 3.0:
        features_list.append(k)

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
    # GridSearchCV(Pipeline([("pca", PCA()), ("classifier", GaussianNB())]), param_grid=dict(pca__n_components=range(1, len(features_list)))),
]

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

# modified from test_classifier, I only need the f1 score :)
def calculate_f1_score(clf, dataset, feature_list, folds = 1000):
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    sss = StratifiedShuffleSplit(folds, random_state=42)
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0
    for train_idx, test_idx in sss.split(features, labels):
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )

        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
            else:
                print "Warning: Found a predicted label not == 0 or 1."
                print "All predictions should take value 0 or 1."
                print "Evaluating performance for processed predictions:"
                break
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
    return f1

clf = None
best_f1_score = -1.0
best_features_list = None
for i in range(2, len(features_list)+1):
    sub_features_list = features_list[:i]
    sub_data = featureFormat(my_dataset, sub_features_list, sort_keys = True)
    sub_labels, sub_features = targetFeatureSplit(sub_data)
    for sub_clf in classifiers:
        sub_clf.fit(sub_features, sub_labels)
        f1_score = calculate_f1_score(sub_clf, my_dataset, sub_features_list)
        if f1_score > best_f1_score:
            clf = sub_clf
            best_features_list = sub_features_list
            best_f1_score = f1_score

print 'aloha', clf, best_features_list, best_f1_score

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, best_features_list)
