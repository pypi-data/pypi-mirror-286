
# Copyright (c) 2024 Deniz Dahman's, Ph.D. <denizdahman@gmail.com>
 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# denizdahman@gmail.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# Support the author of this package on:.#
# https://patreon.com/user?u=118924481
# https://www.youtube.com/@dahmansphi 
# https://dahmansphi.com/subscriptions/


from urllib.request import Request, urlopen
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


class Disguisedata:
  def __init__(self) -> None:
    pass

  def feedDs(self, ds):
    '''This function prepare the DS for Synthetic Generation process'''
    isDsTrue = type(ds).__module__ == np.__name__
    if isDsTrue:
      dimDsFeatureIstrue = ds.shape[1] >= 6
      dimDsRowIstrue = ds.shape[0] >= 30

      if dimDsFeatureIstrue and dimDsRowIstrue:

        dsNorm = np.linalg.norm(ds)
        ds_normed = ds/dsNorm

        pack = [dsNorm, ds_normed]
        print("Your dataset is ready for process; Now you may call on the disguise_data() Function")
        return pack
      else:
        print("Dataset Must be atleast two features and >=30 cases")
    else:
      print("Dataset Must be of Numpy Type input")

  def discover_effect(self, data, effect):
    '''This function explore the possible disguise based on the effect provided'''
    norm = data[0]
    Xcomplete = data[1]
    X = Xcomplete

    arrLeft = []
    arrRight = []

    for inx in range((X.shape[1])):
      inx += 1
      start = inx-1
      end = inx
      featurerX = X[:,start:inx]

      meanFeature = np.mean(featurerX)
      leftSide_mean = meanFeature - (meanFeature * effect)
      rightSide_mean = meanFeature + (meanFeature * effect)

      coeffList = featurerX/meanFeature

      leftSide_Disguise = coeffList * leftSide_mean
      rightSide_Disguise = coeffList * rightSide_mean

      arrLeft.append(leftSide_Disguise)
      arrRight.append(rightSide_Disguise)

    arrLeft = np.array(arrLeft)
    arrLeft = arrLeft.T
    arrLeft = arrLeft[0]
    leftDataset = arrLeft

    arrRight = np.array(arrRight)
    arrRight = arrRight.T
    arrRight = arrRight[0]
    rightDataset = arrRight

    # dealing with samples of the first 6 columns
    # Graph Axis display
    XsixFeature = Xcomplete[:,:6]
    arrLeftSixFeature = arrLeft[:,:6]
    arrRightSixFeature = arrRight[:,:6]

    groupGraph = [[(0,1), (2,3), (4,5)], [(1,2), (3,4), (0,5)]]
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8), tight_layout=True)

    for i in range(2):
      G = groupGraph[i]
      for j in range(3):
        axs[i, j].scatter(XsixFeature[:,G[j][0]], XsixFeature[:,G[j][1]], label="original")
        axs[i, j].scatter(arrLeftSixFeature[:,G[j][0]], arrLeftSixFeature[:,G[j][1]], label="disguised")
        axs[i, j].set_title(f"Axis: ({G[j][0]}) and ({G[j][1]})")
        axs[i, j].axis("off")

    fig.suptitle("Display of Axis distances- Left from Mean")
    plt.legend()
    plt.show()

    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8), tight_layout=True)
    for i in range(2):
      G = groupGraph[i]
      for j in range(3):
        axs[i, j].scatter(XsixFeature[:,G[j][0]], XsixFeature[:,G[j][1]], label="original")
        axs[i, j].scatter(arrRightSixFeature[:,G[j][0]], arrRightSixFeature[:,G[j][1]], label="disguised")
        axs[i, j].set_title(f"Axis: ({G[j][0]}) and ({G[j][1]})")
        axs[i, j].axis("off")

    fig.suptitle("Display of Axis distances- Right from Mean")
    plt.legend()
    plt.show()

    # Display Mat figure
    YLeftSide = arrLeftSixFeature * norm
    YRightSide = arrRightSixFeature * norm
    Xorg = XsixFeature * norm

    lin_dash = "_" * 35
    bar_dash = "|"

    covOriginal = np.cov(X)
    corrOriginal = np.corrcoef(X)
    covarrLeft = np.cov(arrLeft)
    corrLeft = np.corrcoef(arrLeft)
    covarrRight = np.cov(arrRight)
    corrRight = np.corrcoef(arrRight)

    original_lef_cov_diff = np.sum((covOriginal - covarrLeft)**2)
    original_right_cov_diff = np.sum((covOriginal - covarrRight)**2)

    original_lef_corr_diff = np.sum((corrOriginal - corrLeft)**2)
    original_right_corr_diff = np.sum((corrOriginal - corrRight)**2)

    print(lin_dash)
    print("The covariance and correlation Difference of the original set and Left set")
    print(f"Covariance diff {original_lef_cov_diff}, correlation diff {original_lef_corr_diff}")
    print(lin_dash)
    print("The covariance and correlation Difference of the original set and Right set")
    print(f"Covariance diff {original_right_cov_diff}, correlation diff {original_right_corr_diff}")
    print(lin_dash)

    for inx in range((Xorg.shape[1])):
      ysyntheticLeft = YLeftSide[:,inx]
      ysyntheticRight = YRightSide[:,inx]
      xorginal = Xorg[:,inx]
      meanCurrentFeature = (np.mean(X[:,inx])) * norm
      meanCurrentFeatureLeft = (np.mean(arrLeft[:,inx])) * norm
      meanCurrentFeatureRight = (np.mean(arrRight[:,inx])) * norm

      print(f"First three cases from Column {inx+1}")
      print(f"Original mean of this feature {meanCurrentFeature} {bar_dash} Left mean disguised is {meanCurrentFeatureLeft} {bar_dash} Right mean disguised is {meanCurrentFeatureRight}")
      print(lin_dash)
      for jinx in range(3):
        print(f"Original Entry {xorginal[jinx]} {bar_dash} Disguised Entry- Left {ysyntheticLeft[jinx]} {bar_dash} Disguised Entry- Right {ysyntheticRight[jinx]}")
      print(lin_dash)

    leftDataset = leftDataset * norm
    rightDataset = rightDataset * norm
    return [leftDataset, rightDataset]

  def _explor_effect(self, data, mu, div):
    '''This function offer a view on the divation effect provided as argument'''
    norm = data[0]
    Xcomplete = data[1]
    X = Xcomplete[:,:6]

    meanVal = mu/norm
    covMat2 = np.array([[div]])
    Lcholesky2 = np.linalg.cholesky(covMat2)

    arr = []
    arrComplete = []

    for inx in range((X.shape[1])):
      inx += 1
      start = inx-1
      end = inx
      temX = X[:,start:inx]

      featurMean = np.mean(temX)
      featureMeanScaled = int(featurMean * 10000)

      meanValtem = meanVal

      if featureMeanScaled < 1:
        meanValtem = meanVal * 0.1

      Y = meanValtem + temX @ Lcholesky2.T
      arr.append(Y)

    arr = np.array(arr)
    arr = arr.T
    arr = arr[0]

    for inx in range((Xcomplete.shape[1])):
      inx += 1
      start = inx-1
      end = inx
      temXcomplete = Xcomplete[:,start:inx]

      featurMean = np.mean(temXcomplete)
      featureMeanScaled = int(featurMean * 10000)

      if featureMeanScaled < 1:
        meanVal = meanVal * 0.1

      Ycomplete = meanVal + temXcomplete @ Lcholesky2.T
      arrComplete.append(Ycomplete)

    arrComplete = np.array(arrComplete)
    arrComplete = arrComplete.T
    arrComplete = arrComplete[0]

    # dealing with samples of the first 6 columns
    # Graph Axis display
    groupGraph = [[(0,1), (2,3), (4,5)], [(1,2), (3,4), (0,5)]]
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8), tight_layout=True)

    for i in range(2):
      G = groupGraph[i]
      for j in range(3):
        axs[i, j].scatter(X[:,G[j][0]], X[:,G[j][1]])
        axs[i, j].scatter(arr[:,G[j][0]], arr[:,G[j][1]])
        axs[i, j].set_title(f"Axis: ({G[j][0]}) and ({G[j][1]})")
        axs[i, j].axis("off")

    fig.suptitle("Display of Axis distances")
    plt.show()

    # Display Mat figure
    Y = arr * norm
    Xorg = X * norm

    lin_dash = "_" * 35
    bar_dash = "|"

    for inx in range((Xorg.shape[1])):
      ysynthetic = Y[:,inx]
      xorginal = Xorg[:,inx]
      print(f"First three cases from Column {inx+1}")
      print(lin_dash)
      for jinx in range(3):

        print(f"Original Entry {xorginal[jinx]} {bar_dash} Disguised Entry {ysynthetic[jinx]}")
      print(lin_dash)

    # Display stat figure with all features
    Ycomplete = arrComplete * norm
    XcompleteOrignal = Xcomplete * norm

    meanOrignal = np.mean(XcompleteOrignal, axis=0)
    meanSynthet = np.mean(Ycomplete, axis=0)

    varOriginal = np.var(XcompleteOrignal, axis=0)
    varSynthet = np.var(Ycomplete, axis=0)

    print(lin_dash)
    for inx in range(len(meanOrignal)):
      print(f"Mean & Variance of original and Disguised for feature ({inx+1}), and their difference")
      print(lin_dash)

      meanDif = ((np.abs(meanOrignal[inx] - meanSynthet[inx]))/ (meanOrignal[inx] + meanSynthet[inx])) * 100
      meanDif = format(meanDif, ".2f")

      varDivDiff = np.abs(varOriginal[inx] - varSynthet[inx])
      varDiff = (varDivDiff/(varOriginal[inx] + varSynthet[inx]))*100
      varDiff = format(varDiff, ".3f")

      print(f"mean org {meanOrignal[inx]} {bar_dash} mean disguised {meanSynthet[inx]} {bar_dash} difference: {meanDif}%")
      print(f"variance org {varOriginal[inx]} {bar_dash} variance disguised {varSynthet[inx]} difference: {varDiff}%")
      print(lin_dash)


    # Graph Cov mat
    corrMatYsyth = np.cov(Ycomplete)
    corrMatXorig = np.cov(XcompleteOrignal)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 8), tight_layout=True)
    # print(corrMatYsyth)
    # print(corrMatXorig)
    ax1.imshow(corrMatXorig)
    ax1.set_title("Original Covariance Image")
    ax1.axis("off")

    ax2.imshow(corrMatYsyth)
    ax2.set_title("Disguised Covariance Image")
    ax2.axis("off")

    fig.suptitle("Covariance Image of original and disguised data")
    plt.show()



  def _disguise_data(self, data, mu, div):
    '''This function carrys on the generation process based on DisguiseData Method'''
    norm = data[0]
    X = data[1]

    meanVal = mu/norm
    covMat2 = np.array([[div]])
    Lcholesky2 = np.linalg.cholesky(covMat2)

    arr = []
    for inx in range((X.shape[1])):
      inx += 1
      start = inx-1
      end = inx
      temX = X[:,start:inx]

      featurMean = np.mean(temX)
      featureMeanScaled = int(featurMean * 10000)

      meanValtem = meanVal

      if featureMeanScaled < 1:
        meanValtem = meanVal * 0.1

      Y = meanValtem + temX @ Lcholesky2.T
      arr.append(Y)

    arr = np.array(arr)
    arr = arr.T
    arr = arr[0]

    Y = arr * norm
    print("Your Disguise Data is now at your hand you can reassemble that as its orignal form")
    return Y



