# Query dataset for proteins with functions of interest and a subset of negative examples.

import os
import json
import argparse
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

# Parse arguments
def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to dataset file.', default='./data/proteins_wKnown_functions.csv')
    parser.add_argument('annotation_dict', help='Path to file containing dictionary of annotations.', default='./data/annotations.json')
    parser.add_argument('annotation', help='Function of interest (key in annotation_dict). Will also be used to name new dataset files.')
    parser.add_argument('--exclude_from_neg', help='Annotations to exclude from negative set.', default=None)
    parser.add_argument('-o', '--output_folder', help='Path to the output folder.', default='./data/')
    parser.add_argument('--hierarchical', help='Whether the annotation provided is for a sub-hierarchical model.', action='store_true')
    parser.add_argument('--max_prots', type=int, help='Maximum number of proteins to use. Default use all proteins.', default=None)
    
    args = parser.parse_args()


    input_file = args.input
    annotation_dict = args.annotation_dict
    annotation = args.annotation
    exclude_from_neg = args.exclude_from_neg
    output_folder = args.output_folder
    hier = args.hierarchical
    max_prots = args.max_prots
    
    return input_file, annotation_dict, annotation, exclude_from_neg, output_folder, hier, max_prots


# Get labels corresponding to protein type of interest from annotation dictionary.
def get_labels(annotation_dict, protein_of_interest):
    
    with open(annotation_dict, 'r') as fp:
        annotations = json.load(fp)
    
    return annotations[protein_of_interest]


# Load whole dataset and add label corresponding to function of interest.
def load_dataset(filepath, annotations, exclude_neg, hier, max_prots):
    
    data = pd.read_pickle(filepath)
    
    if hier:
        data = data.loc[data.label == 1, :]
        
    data.loc[data.Annotation.isin(annotations), "label"] = 1
    data.loc[((~data.Annotation.isin(annotations)) & (~data.Annotation.str.contains("unknown"))), "label"] = 0
    data = data.loc[~data.Annotation.isin(exclude_neg), :] # Remove annotations from negative set.
    
    data = data.drop_duplicates(subset=data.loc[:, 0:1023].columns)
    
    if (max_prots != None):
        pos = data.loc[data.label==1,:]
        neg = data.loc[data.label==0,:]
        if (len(pos) > max_prots):
            pos = pos.sample(n=max_prots//2, random_state=41)
        if (len(neg) > max_prots):
            neg = neg.sample(n=max_prots//2, random_state=41)
        data = pd.concat([pos, neg])
    
    return data
    
    

"""
# For multiclass prediction. Load whole dataset and add label corresponding to function of interest.
def load_dataset_mc(filepath, annotations):
    
    data = pd.read_pickle(filepath)
    all_prots = pd.DataFrame()
    
    for anno in annotations.keys():
        keep = data.loc[data.Annotation.isin(annotations[anno]), :]
        keep.loc[:, "label"] = anno
        all_prots = pd.concat([all_prots, keep])
    
    all_prots = all_prots.drop_duplicates(subset=all_prots.loc[:, 0:1023].columns)
    
    return all_prots
"""

# Return the list of clusters that are associated to more than 1 label (pcs that possess annotations for positive and negative dataset)
def find_multiAnno_pcs(data):
    multiAnno = data.loc[:, ["pc", "label"]].groupby("pc").nunique()
    return list(multiAnno.loc[multiAnno.label > 1, :].index)


# Train-test split using the protein clusters
def split_clusters(data):
    pcs = np.unique(list(data.loc[:, 'pc']))
    stratify = list(data.loc[data.pc.isin(pcs), ["pc", "label"]].drop_duplicates().label)
    train_pcs, test_pcs = train_test_split(pcs, test_size=0.2, stratify=stratify, random_state=41)
    
    train = data.loc[data.pc.isin(train_pcs), :]
    test = data.loc[data.pc.isin(test_pcs), :]
    return train, test

"""
def sample_dataset(data):
    
    # For negative proteins, we want to have a dataset that is representative of the diversity observed in nature.
    #  1 protein is kept per negative cluster (no homologous proteins in the negative dataset).
    neg = data.loc[data.label == 0, :].drop_duplicates(subset=["pc"])
    

    # Split train-test (80%-20%) using protein clusters from mmseqs
    data = pd.concat([data.loc[data.label == 1, :], neg])
    train, test = split_clusters(data)
    
    
    # Print pos/neg counts in the train and test sets.
    print(f"There are {len(data.loc[data.label == 1, :].pc.unique())} unique rbp clusters containing a total of {len(data.loc[data.label == 1, :])} proteins.")
    print(f"There are {len(test.loc[test.label == 1, :].pc.unique())} unique rbp clusters in the test set containing a total of {len(test.loc[test.label == 1, :])} proteins.")
    print(f"There are {len(train.loc[train.label == 1, :].pc.unique())} unique rbp clusters in the train set containing a total of {len(train.loc[train.label == 1, :])} proteins.")

    print(f"\nThere are {len(data.loc[data.label == 0, :].pc.unique())} unique non-rbp clusters containing a total of {len(data.loc[data.label == 0, :])} proteins.")
    print(f"There are {len(test.loc[test.label == 0, :].pc.unique())} unique non-rbp clusters in the test set containing a total of {len(test.loc[test.label == 0, :])} proteins.")
    print(f"There are {len(train.loc[train.label == 0, :].pc.unique())} unique non-rbp clusters in the train set containing a total of {len(train.loc[train.label == 0, :])} proteins.")
    
    
    # Remove columns that are useless for training to reduce size of file
    train = train.drop(columns=["pc", "Accession", "VC", "Host", "host_type", "Annotation", "Category"])
    
    return train, test


#For multiclass prediction.
def sample_dataset_mc(data):
    
    train, test = split_clusters(data)
    
    for anno in data.label.unique():
        print(f"There are {len(data.loc[data.label == anno, :].pc.unique())} unique {anno} clusters containing a total of {len(data.loc[data.label == anno, :])} proteins.")
        print(f"There are {len(test.loc[test.label == anno, :].pc.unique())} unique {anno} clusters in the test set containing a total of {len(test.loc[test.label == anno, :])} proteins.")
        print(f"There are {len(train.loc[train.label == anno, :].pc.unique())} unique {anno} clusters in the train set containing a total of {len(train.loc[train.label == anno, :])} proteins.\n")
    
    
    # Remove columns that are useless for training to reduce size of file
    train = train.drop(columns=["pc", "Accession", "VC", "Host", "host_type", "Annotation", "Category"])
    
    return train, test
"""

def main():
    
    # Parse args
    input_file, annotation_dict, annotation, exclude_from_neg, output_folder, hier, max_prots = parse_args()
    
    
    # Get annotations corresponding to protein type of interest
    annotations = get_labels(annotation_dict, annotation)
    
    if exclude_from_neg is not None:
        exclude_neg = get_labels(annotation_dict, exclude_from_neg)
    else:
        exclude_neg= []
    
    # Load dataset containing positive and negative examples
    data = load_dataset(input_file, annotations, exclude_neg, hier, max_prots)
    
    
    # Remove pcs associated to many annotations (to the positive and negative dataset at the same time).
    multi_anno_pcs = find_multiAnno_pcs(data)

    multi_anno_proteins = data.loc[data.pc.isin(multi_anno_pcs), :]
    data = data.loc[~data.pc.isin(multi_anno_pcs), :]

    
    # For negative proteins, we want enough proteins to be representative of the diversity observed, but not too many.
    #  If the negative set is too big, 1 protein is kept per negative cluster (no homologous proteins in the negative dataset).
    #  If not, all negative proteins are kept.
    if not hier:
        neg = data.loc[data.label == 0, :].drop_duplicates(subset=["pc"])
    else:
        neg = data.loc[data.label == 0, :]

    # Split train-test (80%-20%) using protein clusters from mmseqs
    data = pd.concat([data.loc[data.label == 1, :], neg])
    
    print(f"There are {len(data.loc[data.label == 1, :].pc.unique())} unique {annotation} clusters containing a total of {len(data.loc[data.label == 1, :])} proteins.")
    print(f"There are {len(data.loc[data.label == 0, :].pc.unique())} unique non-{annotation} clusters containing a total of {len(data.loc[data.label == 0, :])} proteins.")
    
    
    # Save files
    if max_prots != None:
        data.to_pickle(os.path.join(output_folder, f"{annotation}_{max_prots}.pkl"))
    
    else:
        data.to_pickle(os.path.join(output_folder, f"{annotation}.pkl"))
    multi_anno_proteins.to_pickle(os.path.join(output_folder, f"{annotation}_multiAnnotationPcs.pkl"))
    

if __name__ == '__main__':
    main()