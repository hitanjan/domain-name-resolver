__author__ = 'hitanjan'

from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report
import input
from operator import itemgetter
from time import time
import numpy as np
from scipy.stats import randint as sp_randint
from sklearn.externals import joblib
import pickle


class classifier():
    __cache_dir__ = "bin"

    def __init__(self, pipeline=None, file=None, load_from_disk=False):
        if(not os.path.exists(self.__cache_dir__)):
            os.makedirs(self.__cache_dir__)

        if(not pipeline is None):
            self.pipeline = pipeline
        if(not file is None):
            self.file = file
            if load_from_disk:
                self.load()

        self.train_complete = False
        self.categories = input.get_categories()

    def __str__(self):
        return str(self.pipeline)

    def __repr__(self):
        return repr(self.pipeline)

    def can_load(self):
        return os.path.exists(os.path.join(self.__cache_dir__, self.file))

    def save(self):
        print("Saving classifier..")
        if(self.train_complete):
            joblib.dump(self.trained_pipeline, os.path.join(self.__cache_dir__,self.file))
        else:
            joblib.dump(self.pipeline, os.path.join(self.__cache_dir__,self.file))

    def load(self):
        if(self.can_load()):
            print("Loading classifier..")
            self.pipeline = joblib.load(os.path.join(classifier.__cache_dir__,self.file))


    def predict(self, model):
        model.load_raw_data()
        text = model.text
        pred = int(self.pipeline.predict([text]))
        return self.categories[pred] == self.categories[1]

    def train(self, x_train, y_train, categories):

        print("Training:  %s" % self.pipeline)
        t0 = time()
        self.pipeline.fit(x_train, y_train)
        train_time = time() - t0
        print("Train Time %s" % train_time)

        self.categories = categories
        self.train_complete = True
        self.trained_pipeline = self.pipeline

    def test(self, x_test, y_test):
        print("Testing:  %s" % self.pipeline)

        t0 = time()
        pred = self.pipeline.predict(x_test)
        test_time = time() - t0
        print("Test Time %s" % test_time)
        score = metrics.accuracy_score(y_test, pred)
        print("Score %s" % score)

        if hasattr(self.pipeline, 'coef_'):
            print("Dimentionality - %s "% self.pipeline.coef_.shape[1])
            print("Density - %s" % density(self.pipeline.coef_))


        print("Classification Report - %s" % classification_report(y_test, pred,
                                            target_names=self.categories))

        print("Confusion Matrix - %s "% metrics.confusion_matrix(y_test, pred))



    def train_and_fit_params(self, x_train, y_train, x_test, y_test, categories, param_grid, n_iter, cv, randomized=False, run_parallel=False):

        def print_param_search_report(grid_scores, n_top=3):
            top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
            for i, score in enumerate(top_scores):
                print("Model with rank: {0}".format(i + 1))
                print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                      score.mean_validation_score,
                      np.std(score.cv_validation_scores)))
                print("Parameters: {0}".format(score.parameters))
                print("")

        if(run_parallel):
            n_jobs=-1
        else:
            n_jobs=1

        print("Training Classifier with Cross Validation..")

        if(randomized or not n_iter is None):
            search = RandomizedSearchCV(self.pipeline, param_distributions=param_grid, cv=cv, n_jobs=n_jobs,
                                   n_iter=n_iter)
        else:
            search = GridSearchCV(self.pipeline, param_grid=param_grid, cv=cv, n_jobs=n_jobs)

        start = time()
        search.fit(x_train, y_train)
        print("%s took %.2f seconds for %d candidate parameter settings." % (search, time() - start, len(search.grid_scores_)))
        print("Best parameters set found on development set:")
        print()
        print(search.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        print_param_search_report(search.grid_scores_)



        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, search.predict(x_test)
        print("Detailed classification report:")
        print(classification_report(y_true, y_pred,target_names=categories))
        print()

        self.categories = categories
        self.train_complete = True
        self.trained_pipeline = search.best_estimator_


def create_classifier_template2():
    data = input.load_data(0.5)
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(sublinear_tf=True, strip_accents='unicode', decode_error='replace')),
        #('hash', HashingVectorizer()),
        #('svd', TruncatedSVD()),
        #('lsa', Normalizer()),
        ('sgd', SGDClassifier(verbose=1, alpha=.0001, n_iter=50,
                                           penalty='l2', loss='modified_huber'))
    ])

    c = classifier(pipeline=pipe, file="p1", load_from_disk=False)
    c.train(data[0], data[1], data[4])
    c.test(data[2], data[3])
    c.save()

def load_classifier_template2():
    c = classifier(file="p1", load_from_disk=True)
    return c

def load_classifier_template1():
    c = classifier(file="p3", load_from_disk=True)
    return c

def create_classifier_template1():
    data = input.load_data(0.6)
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer()),
        #('hash', HashingVectorizer()),
        #('svd', TruncatedSVD()),
        #('lsa', Normalizer()),
        ('sgd', SGDClassifier(verbose=1))
    ])

    c = classifier(pipeline=pipe, file="p3", load_from_disk=False)

    param_dict_random = {
              #"tfidf__max_df" : np.arange( 0, 1, 0.001 ).tolist(),
              #"tfidf__min_df" : np.arange( 0, 1, 0.001 ).tolist(),
              "tfidf__norm" : ['l1', 'l2'],
              "tfidf__use_idf" : [True, False],
              "tfidf__smooth_idf" : [True, False],
              "tfidf__sublinear_tf": [True, False],
              "tfidf__ngram_range": [(1, 1), (1, 2)],
              "tfidf__binary" :[ True, False],
              "sgd__loss" : ["hinge", "log", "modified_huber", "squared_hinge", "perceptron", "squared_loss", "huber", "epsilon_insensitive", "squared_epsilon_insensitive"],
              "sgd__penalty": ["l2", "l1", "elasticnet"],
              "sgd__average": [True, False],
              "sgd__warm_start": [True, False],
              "sgd__fit_intercept": [True, False],
              "sgd__shuffle":[True, False],
              #"sgd__learning_rate": ["constant", "invscaling"], #, "optimal"],
              #"sgd__eta0":
              "sgd__n_iter": sp_randint(1, 150),
              "sgd__alpha": np.arange(0.000001, 0.1, 0.01 ).tolist(),

              }

    c.train_and_fit_params(data[0], data[1], data[2], data[3], data[4], param_dict_random, 30, 10, run_parallel=True)
    c.save()



if __name__ == '__main__':
    #create_classifier_template2() #- 82%
    #create_classifier_template1()
    pass

