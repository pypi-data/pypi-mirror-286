# Predict the function of the phage proteins in a given dataset.

import os
import pickle
import joblib
import argparse
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to input file containing protein embeddings that you wish to annotate (.pkl).')
    parser.add_argument('name', help='Predictions will be saved using this name in the results folder (no extension).')
    parser.add_argument('-f', '--models_folder', help='Path to folder containing pretrained models. Default folder is ./models/', default="./models/")
    parser.add_argument('-o', '--output_folder', help='Path to the output folder. Default folder is ./results/', default="./results/")
    parser.add_argument('-m', '--mode', help='Which types of proteins you want to predict. Accepted arguments are "all" (default), "pvp", "rbp", "lysin", "regulator", ...', default="all")
    parser.add_argument('-c', '--custom', help='Instead of using --mode, you can specify the path to your own custom trained model (.pkl). The name you use will be used as the positive label.', default=False)
    args = parser.parse_args()


    input_file = args.input
    models_folder = args.models_folder
    name = args.name
    output_folder = args.output_folder
    mode = args.mode
    custom = args.custom

    return input_file, models_folder, name, output_folder, mode, custom


# Load dataset we want to make predictions for
def load_dataset(input_file):

    print("Loading dataset...")

    if input_file.endswith(".pkl"):
        test = pd.read_pickle(input_file)

    if input_file.endswith(".csv"):
        test = pd.read_csv(input_file, index_col=0)
        test.columns = test.columns.astype(int)

    X_test = test.loc[:, 0:1023]

    print("Done loading dataset.")

    return X_test


def _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=False):

    # If X_test is empty (ex. no predicted capsid proteins for major_capsid model), skip this model
    if X_test.shape[0] == 0:
        return all_preds

    # If model is hierarchical, set aside proteins that do not belong to parent annotation.
    # We wont waste resources making predictions for these proteins.
    if parent_anno:
        keep = all_preds.index[all_preds.loc[:, parent_anno] > 0.5]
        all_preds_ = all_preds.loc[~all_preds.index.isin(keep), :] # set aside non-anno proteins
        X_test = X_test.loc[X_test.index.isin(keep), :]

        if X_test.shape[0] == 0:
            return all_preds

    # Load model and make predictions
    #with open(os.path.join(models_folder, f"{anno}_svm.pkl"), 'rb') as file:
    #    clf=pickle.load(file)
    clf = joblib.load(os.path.join(models_folder, f"{anno}_svm.pkl"))
    preds = pd.DataFrame(clf.predict_proba(X_test), columns=clf.classes_, index=X_test.index).iloc[:,1]


    # Format annotations
    all_preds = _format_preds(preds, all_preds, mode, anno)

    # If hierarchical re-add proteins that did not belong to parent annotation
    if parent_anno:
        all_preds = pd.concat([all_preds, all_preds_]) # Re-add non-anno proteins

    return all_preds


# Make predictions for binary models and aggregate results
def _format_preds(preds, all_preds, mode, anno):

    cols = list(all_preds.columns) + [anno]
    all_preds = pd.merge(all_preds, preds, left_index=True, right_index=True)
    all_preds.columns = cols

    if mode == anno: # assign "non-poi" (poi=protein of interest) as label if in binary mode (ex. pvp vs non-pvp).
        annotations = pd.Series(np.where(all_preds[anno] > 0.5, anno, f"non-{anno}"), index=all_preds.index)
    else:
        annotations = pd.Series(np.where(all_preds[anno] > 0.5, anno, ""), index=all_preds.index)

    if "Annotation" in all_preds.columns:
        all_preds.Annotation = all_preds.Annotation.str[:] + "|" + annotations.str[:]
        all_preds.Annotation = all_preds.Annotation.str.rstrip("|")
    else:
        all_preds["Annotation"] = annotations.str[:]

    return all_preds



# Predict all protein functions the user desires
def predict_functions(X_test, all_preds, models_folder, mode="all"):

    print("Making predictions...")

    # phage virion proteins
    if (mode == "all") or (mode == "pvp"):
        anno_dict = {"pvp":False, "capsid":"pvp", "major_capsid":"capsid", "minor_capsid":"capsid","tail":"pvp", 
                     "major_tail":"tail", "minor_tail":"tail", "baseplate":"tail", "tail_appendage":"tail", 
                     "tail_sheath":"tail", "portal":"pvp", "collar":"pvp", "head-tail_joining":"pvp"}
        
        for anno in anno_dict:
            print(f"Predicting {anno} proteins...")
            all_preds = _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=anno_dict[anno])



    # DNA-associated
    if (mode == "all") or (mode == "DNA-associated"):
        anno_dict = {"DNA-associated":False, "integration":"DNA-associated", "nuclease":"DNA-associated", 
                     "DNA_polymerase":"DNA-associated", "terminase":"DNA-associated","annealing":"DNA-associated",
                    "helicase":"DNA-associated", "primase":"DNA-associated", "replication_initiation":"DNA-associated"}
        
        for anno in anno_dict:
            print(f"Predicting {anno} proteins...")
            all_preds = _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=anno_dict[anno])

        
    # Transcriptional regulators
    if (mode == "all") or (mode == "regulator"):
        anno_dict = {"transcriptional_regulator":False, "transcriptional_activator":"transcriptional_regulator", 
                     "transcriptional_repressor":"transcriptional_regulator"}
        
        for anno in anno_dict:
            print(f"Predicting {anno} proteins...")
            all_preds = _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=anno_dict[anno])


    # Packaging and assembly proteins
    if (mode == "all") or (mode == "packaging"):
        print("Predicting packaging and assembly proteins...")
        all_preds = _predict(X_test, all_preds, models_folder, "packaging_assembly", mode, parent_anno=False)


    # adsorption-related proteins
    if (mode == "all") or (mode == "adsorption-related"):
        print("Predicting adsorption-related proteins...")
        all_preds = _predict(X_test, all_preds, models_folder, "adsorption-related", mode, parent_anno=False)


    # cell wall depolymerases
    if (mode == "all") or (mode == "cell_wall_depolymerase"):
        print("Predicting cell wall depolymerases...")
        all_preds = _predict(X_test, all_preds, models_folder, "cell_wall_depolymerase", mode, parent_anno=False)

    # RNA-associated
    if (mode == "all") or (mode == "RNA-associated"):
        print("Predicting RNA-associated proteins...")
        all_preds = _predict(X_test, all_preds, models_folder, "RNA-associated", mode, parent_anno=False)

    # nucleotide metabolism
    if (mode == "all") or (mode == "nucleotide_metabolism"):
        print("Predicting proteins associated to nucleotide metabolism...")
        all_preds = _predict(X_test, all_preds, models_folder, "nucleotide_metabolism", mode, parent_anno=False)

    # Internal and ejection proteins
    if (mode == "all") or (mode == "ejection"):
        print("Predicting internal and ejection proteins...")
        all_preds = _predict(X_test, all_preds, models_folder, "ejection", mode, parent_anno=False)


    # phosphorylation
    if (mode == "all") or (mode == "phosphorylation"):
        print("Predicting phosphorylation proteins...")
        all_preds = _predict(X_test, all_preds, models_folder, "phosphorylation", mode, parent_anno=False)


    # transferase
    if (mode == "all") or (mode == "transferase"):
        print("Predicting transferases...")
        all_preds = _predict(X_test, all_preds, models_folder, "transferase", mode, parent_anno=False)


    # reductase
    if (mode == "all") or (mode == "reductase"):
        print("Predicting reductases...")
        all_preds = _predict(X_test, all_preds, models_folder, "reductase", mode, parent_anno=False)


    # defense_systems
    if (mode == "all") or (mode == "defense_systems"):
        anno_dict = ["crispr", "anti-restriction", "sir2", "toxin", "super_infection"]
        
        for anno in anno_dict:
            print(f"Predicting {anno} proteins...")
            all_preds = _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=False)

    # lysis
    if (mode == "all") or (mode == "lysis"):
        anno_dict = {"lysis":False, "endolysin":"lysis", "lysis_inhibitor":"lysis", "holin":"lysis", "spanin":"lysis"}
        
        for anno in anno_dict:
            print(f"Predicting {anno} proteins...")
            all_preds = _predict(X_test, all_preds, models_folder, anno, mode, parent_anno=anno_dict[anno])


    #Create final annotation
    all_preds.loc[all_preds.Annotation == '', "Annotation"] = "unknown"
    all_preds.Annotation = all_preds.Annotation.str.lstrip("|")

    return all_preds


# Save predictions
def save_preds(preds, name, output_folder):

    print("Saving predictions to file...")

    preds.to_csv(os.path.join(output_folder, name, f"predictions_{name}.csv"))

    print("Done saving predictions to file.")


def main():

    #Load user args
    input_file, models_folder, name, output_folder, mode, custom = parse_args()

    #Create output folder
    if not os.path.exists(os.path.join(output_folder, name)):
        os.makedirs(os.path.join(output_folder, name))

    #Load dataset
    X_test = load_dataset(input_file)

    #Remove entries with the duplicate names
    X_test = X_test.loc[~X_test.index.duplicated()]
    if X_test.index.duplicated().sum() > 0:
        print(X_test.index.duplicated().sum(), "sequences with duplicate names were removed. Make sure this is normal as you may have lost some sequences. Here is the list of problematic IDs:", X_test[X_test.index.duplicated()].index)

    #Create empty dataframe to save predictions
    all_preds = pd.DataFrame(index=X_test.index)

    if custom:
        with open(os.path.join(models_folder, custom), 'rb') as file:
            clf=pickle.load(file)
        preds = pd.DataFrame(clf.predict_proba(X_test), columns=clf.classes_, index=X_test.index).iloc[:, 1]
        preds = _format_preds(preds, all_preds, name, name)

    else:
        preds = predict_functions(X_test, all_preds, models_folder, mode)

    save_preds(preds, name, output_folder)


if __name__ == '__main__':
    main()
