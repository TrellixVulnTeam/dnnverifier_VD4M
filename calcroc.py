import glob
import os.path
import argparse
import subprocess
import csv
import math
import platform
import os.path
import extractfts
import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as pp
import sklearn.metrics as metrics
from sklearn.metrics import accuracy_score,precision_score, recall_score

def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)):
        if y_actual[i]==y_hat[i]==1:
           TP += 1
        if y_hat[i]==1 and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]==0:
           TN += 1
        if y_hat[i]==0 and y_actual[i]!=y_hat[i]:
           FN += 1

    return(TP, FP, TN, FN)

def main():
    parser = argparse.ArgumentParser(description='psnr calculation parser.')
    parser.add_argument('--infile', type=str, help='select directory', default='psnrresult_total.csv')
    args = parser.parse_args()

    infile = args.infile

    if infile == None:
        print("select psnr result csv file")
        return

    scores = []
    lables = []
    if infile != None:
        with open(infile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(row['psnr'], row['target'])
                scores.append( float(row['psnr']))
                lables.append(int(row['target']))

    smax = float(max(scores))

    ascores = np.array(scores) / smax
    alable = np.array(lables)


    afpr, atpr, thresholds = metrics.roc_curve(alable, ascores)

    arocauc = metrics.auc(afpr, atpr)

    pp.title("Receiver Operating Characteristic")
    pp.xlabel("False Positive Rate(1 - Specificity)")
    pp.ylabel("True Positive Rate(Sensitivity)")
    pp.plot(afpr, atpr, "b", label="(AUC = %0.2f)" % arocauc)
    pp.plot([0, 1], [1, 1], "y--")
    pp.plot([0, 1], [0, 1], "r--")
    pp.legend(loc="lower right")
    pp.show()

    pp.figure()
    pp.plot(1.0 - atpr, thresholds, marker='*', label='tpr')
    pp.plot(afpr, thresholds, marker='o', label='fpr')
    pp.legend()
    pp.xlim([0, 1])
    pp.ylim([0, 1])
    pp.xlabel('thresh')
    pp.ylabel('far/fpr')
    pp.title(' thresh - far/fpr')
    pp.show()

    for threval in np.arange(0.5, 1.0, 0.05):
        predictval = (ascores > threval)

        TP, FP, TN, FN = perf_measure(alable, predictval)

        FACC = accuracy_score(alable, predictval)
        FFAR = FP / float(FP + TN)
        FFRR = FN / float(TP + FN)

        #ftar =  precision_score(alable, predictval)
        #ffar = recall_score(alable, predictval)

        print("Threshold: %.2f Accuracy : %.2f  FAR: %.2f FRR: %.2f" %(threval * smax ,FACC, FFAR,FFRR))

    print("task complete!")


if __name__== "__main__":
    main()
