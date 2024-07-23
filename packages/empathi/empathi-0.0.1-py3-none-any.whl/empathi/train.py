# Train an svm to predict phage protein functions

import os
import time
import pickle
import joblib
import argparse
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to file containing the training set.')
    parser.add_argument('annotation', help='Protein of interest. Model will be saved using this name in the models folder (.pkl).')
    parser.add_argument('-m', '--model', help='Type of model to train. Default value is "all". Accepted values are "all", "svm", "rf", "lr".', default='all')
    parser.add_argument('-o', '--output_folder', help='Path to the output folder. Default folder is ./models/', default="./models/")
    parser.add_argument('--optimize', help='Whether to perform grid search of hyperparameters while training model.', action="store_true")
    args = parser.parse_args()


    input_file = args.input
    annotation = args.annotation
    model = args.model
    output_folder = args.output_folder
    optimize = args.optimize
    
    return input_file, annotation, model, output_folder, optimize


# Load dataset
def load_dataset(input_file):
    
    print("Loading dataset...")
    
    data = pd.read_pickle(input_file)
    
    print("Done loading dataset.")
    
    return data


# Train-test split using the protein clusters
def split_clusters(data):
    pcs = np.unique(list(data.loc[:, 'pc']))
    stratify = list(data.loc[data.pc.isin(pcs), ["pc", "label"]].drop_duplicates().label)
    train_pcs, test_pcs = train_test_split(pcs, test_size=0.2, stratify=stratify, random_state=41)
    
    train = data.loc[data.pc.isin(train_pcs), :]
    test = data.loc[data.pc.isin(test_pcs), :]
    return train, test


# Train classifier
def train_clf(X_train, y_train, model="svm", optimize=False):
    
    print(f"Training {model} classifier...")
    t1 = time.time()
    
    if model == "rf":
        if optimize:
            grid={'n_estimators': [5,10,20,50,100],
                 'max_features':[0.1,0.3,0.5,0.7,0.9,1],
                 'max_depth':[2,4,6,8,10],
                 'min_samples_leaf':[2,4,6,8,10]}
        else:
            clf = RandomForestClassifier(random_state=42, class_weight="balanced")
            clf.fit(X_train, y_train)
    
    if model == "svm":
        if optimize:
            grid={'kernel' : ['poly', 'RBF', 'sigmoid'],
                  'C' : [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        else:
            clf = SVC(probability=True, random_state=42, class_weight="balanced")
            clf.fit(X_train, y_train)
    
    if model == "lr":
        if optimize:
            clf = LogisticRegression(random_state=42, max_iter=250, class_weight="balanced")
            grid = {"solver":['newton-cg', 'lbfgs', 'liblinear'], "c_values":[0.01, 0.1, 1, 10, 100]}
            cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
            grid_search = GridSearchCV(estimator=clf, param_grid=grid, n_jobs=-1, cv=cv, scoring='balanced_accuracy',error_score=0)
            grid_result = grid_search.fit(X_train, y_train)
        else:
            clf = LogisticRegression(random_state=42, max_iter=250, class_weight="balanced")
            clf.fit(X_train, y_train)
    
    print(f"Done training classifier in {time.time() - t1} seconds.")
    
    return clf


# Save classifier
def save_clf(clf, annotation, model, output_folder):

    print("Saving classifier to file...")

    #with open(os.path.join(output_folder, f"{annotation}_{model}.pkl"), 'wb') as file:
    #    pickle.dump(clf, file)
    joblib.dump(clf, os.path.join(output_folder, f"{annotation}_{model}.pkl"))

    print("Done saving classifier to file.")


def main():
    
    input_file, annotation, model, output_folder, optimize = parse_args()
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    data = load_dataset(input_file)
    train, test = split_clusters(data)
    
    train = train.sample(frac=1, random_state=42) #shuffle data
    X_train = train.loc[:, 0:1023]
    y_train = train.loc[:, 'label']
    
    if (model == 'svm') or (model == 'all'):
        clf = train_clf(X_train, y_train, 'svm', optimize)
        save_clf(clf, annotation, "svm", output_folder)
        
    if (model == 'rf') or (model == 'all'):
        clf = train_clf(X_train, y_train, 'rf', optimize)
        save_clf(clf, annotation, "rf", output_folder)
        
    if (model == 'lr') or (model == 'all'):
        clf = train_clf(X_train, y_train, 'lr', optimize)
        save_clf(clf, annotation, "lr", output_folder)
    


if __name__ == '__main__':
    main()
