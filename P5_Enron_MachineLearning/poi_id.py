#!/usr/bin/python

import sys
import pickle
import warnings
warnings.filterwarnings('ignore')
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.metrics import f1_score

def estimate_classifier(clf, dataset, feature_list, folds = 1000):
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    sss = StratifiedShuffleSplit(n_splits=1000, random_state=42)
    cv_f1_scores = []
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
        cv_f1_scores.append(f1_score(predictions, labels_test))
    return np.mean(cv_f1_scores)

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
    if feature_scores[k] >= 2.0:
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
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

gaussianGSCV = GridSearchCV(Pipeline([("pca", PCA(random_state=42)), ("clf", GaussianNB())]),
                            dict(pca__n_components=[1, 2, 3, 4, 6, 8]), 'f1')

svmGSCV = GridSearchCV(Pipeline([("scaler", StandardScaler()), ("pca", PCA(random_state=42)), ("clf", SVC())]),
                       [dict(pca__n_components=[1, 2, 3, 4, 6, 8], clf__C=np.logspace(-2, 3, 6), clf__kernel=['sigmoid'], clf__class_weight=['balanced'], clf__gamma=np.logspace(-4, 1, 6)),
                       dict(pca__n_components=[1, 2, 3, 4, 6, 8], clf__C=np.logspace(-2, 3, 6), clf__kernel=['rbf'], clf__class_weight=['balanced'], clf__gamma=np.logspace(-4, 1, 6))],
                       'f1')

dtGSCV = GridSearchCV(Pipeline([("pca", PCA(random_state=42)), ("clf", DecisionTreeClassifier())]),
                      dict(pca__n_components=[1, 2, 3, 4, 6, 8],
                      clf__criterion=['gini', 'entropy'],
                      clf__splitter=['best', 'random'],
                      clf__min_samples_split=[2, 3, 4, 5],
                      clf__random_state=[0, 42]), 'f1')

adaGSCV = GridSearchCV(Pipeline([("pca", PCA(random_state=42)), ("clf", (AdaBoostClassifier(DecisionTreeClassifier(max_depth=1))))]),
                       dict(pca__n_components=[1, 2, 3, 4, 6, 8],
                       clf__algorithm=['SAMME', 'SAMME.R'],
                       clf__n_estimators=[10, 20, 40, 50, 100, 120, 150, 180, 200, 300]), 'f1')

classifiers = [
    gaussianGSCV,
    svmGSCV,
    dtGSCV,
    adaGSCV,
]

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

best_clf = None
best_f1_score = -1.0
for clf in classifiers:
    clf.fit(features, labels)
    f1 = estimate_classifier(clf.best_estimator_, my_dataset, features_list)
    if f1 > best_f1_score:
        best_clf = clf
        best_f1_score = f1
    print('estimator: {}, f1 score: {}'.format(clf.best_estimator_, f1))
    print

# print('best estimator {} with score {}'.format(best_clf.best_estimator_, best_clf.best_score_))

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(best_clf.best_estimator_, my_dataset, features_list)
