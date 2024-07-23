# Calculate performance metrics for a classifier.

import os
import pickle
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, RocCurveDisplay, PrecisionRecallDisplay, precision_recall_curve
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score, recall_score, precision_score


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to input file containing labels for each protein (test.pkl).')
    parser.add_argument('predictions', help='Path to file containing predictions made by model (.csv).')
    parser.add_argument('annotation', help='Name of positive label. Will also be used to save figures in the ouput folder.')
    parser.add_argument('output_folder', help='Path to the output folder. Default folder is ./results.', default="./results/")
    parser.add_argument('--multiclass', help='Whether the model that is being tested is a multiclass model.', action='store_true')
    args = parser.parse_args()


    input_file = args.input
    path_to_preds = args.predictions
    output_folder = args.output_folder
    annotation = args.annotation
    mc = args.multiclass
    
    return input_file, path_to_preds, output_folder, annotation, mc


def load_data(input_file, path_to_preds):
    
    test = pd.read_pickle(input_file)
    preds = pd.read_csv(path_to_preds, index_col=0)
    
    return test, preds


def calc_metrics(labels, preds):
    unique_labels = sorted(labels.unique())
    
    #Calculate metrics
    f1 = f1_score(labels, preds, average=None, labels=unique_labels)
    prec = precision_score(labels, preds, average=None, labels=unique_labels) 
    recall = recall_score(labels, preds, average=None, labels=unique_labels)

    scores = pd.DataFrame(data = {"f1_score": f1, "Precision":prec, "Recall":recall}, index=unique_labels)
    print(scores)
    
    
def calc_avg_metrics(labels, preds):
    unique_labels = sorted(labels.unique())
    f1 = f1_score(labels, preds, average='weighted', labels=unique_labels)
    prec = precision_score(labels, preds, average='weighted', labels=unique_labels) 
    recall = recall_score(labels, preds, average='weighted', labels=unique_labels)

    print(f"F1 score : ", f1)
    print(f"Precision : ", prec)
    print(f"Recall : ", recall)
    

def confusion_matrix(labels, preds, annotation, output_folder):
    unique_labels = sorted(labels.unique())
    
    #Plot confusion matrix
    fig, ax = plt.subplots(figsize=(3,3))
    cm = confusion_matrix(labels, preds)
    cmn = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    sns.heatmap(cmn, xticklabels=unique_labels, yticklabels=unique_labels, annot=True, fmt=".2f", ax=ax, annot_kws={"size":6.5})
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(os.path.join(output_folder, annotation, f"conf_matrix_{annotation}.png"), bbox_inches="tight", transparent=True)
    plt.show()
    

def plot_roc_curve(labels, preds, annotation, output_folder):
    fpr, tpr, _ = roc_curve(labels, preds)
    roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
    plt.savefig(os.path.join(output_folder, annotation, f"roc_curve_{annotation}.png"), bbox_inches="tight", transparent=True)
    plt.show()
    
    
def plot_pr_curve(labels, preds, annotation, output_folder):
    prec, recall, _ = precision_recall_curve(labels, preds)
    pr_display = PrecisionRecallDisplay(precision=prec, recall=recall).plot()
    plt.savefig(os.path.join(output_folder, annotation, f"prec_recall_{annotation}.png"), bbox_inches="tight", transparent=True)
    plt.show()
    

def main():
    
    input_file, path_to_preds, output_folder, annotation, mc = parse_args()
    
    if not os.path.exists(os.path.join(output_folder, annotation)):
        os.makedirs(os.path.join(output_folder, annotation))
        
    test, preds = load_data(input_file, path_to_preds)
    
    if not mc:
        calc_avg_metrics(test.label, preds.Annotation==annotation)
        confusion_matix(test.label, preds.Annotation==annotation, annotation, output_folder)
        plot_roc_curve(test.label, preds.loc[:, annotation], annotation, output_folder)
        plot_pr_curve(test.label, preds.loc[:, annotation], annotation, output_folder)
    else:
        calc_metrics(test.label, preds[f"{annotation}_mc"])
        calc_avg_metrics(test.label, preds[f"{annotation}_mc"])
        confusion_matix(test.label, preds[f"{annotation}_mc"], annotation, output_folder)
    
    
if __name__ == '__main__':
    main()