# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:21:42 2018

@author: Will
"""


import sklearn.cluster as cluster
import sklearn.manifold as manifold
import sklearn.decomposition as decomposition
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_DAT = pd.read_excel("DAT_Output.xlsx", parse_cols=[3,4,5,6])
df_PreDAT = pd.read_excel("DAT_Output.xlsx", parse_cols=[1,2])

#Parameters are explained within the Final Report

NUMCLUSTERS = 15
"""
HEAT MAP
"""
#Heatmap used for initial visualization of the multidimensional data
correlation = df_DAT.corr()
sns.heatmap(correlation)
plt.show()
"""
***
CLUSTERING IMPLEMENTED AFTER DIMENSIONALITY REDUCTION
***
"""
df_TSNE = manifold.TSNE(n_components=2).fit_transform(df_DAT)
df_TSNE = pd.DataFrame(df_TSNE)

plt.scatter(df_TSNE[0], df_TSNE[1])
plt.title('TSNE Dimensionality Reduction')
plt.show()

TSNE_DBSCAN = cluster.DBSCAN(eps=5).fit(df_TSNE)
plt.scatter(df_TSNE[0], df_TSNE[1], c=TSNE_DBSCAN.labels_.astype(float))
plt.title('TSNE Dimensionality Reduction --> DBSCAN Clustering')
plt.show()

#Bandwidth of 20 used to obtain similar number of cluster to KMeans
TSNE_MeanShift = cluster.MeanShift(bandwidth=20, bin_seeding=True).fit(df_TSNE)
plt.scatter(df_TSNE[0],df_TSNE[1], c=TSNE_MeanShift.labels_.astype(float))
plt.title('TSNE Dimensionality Reduction --> MeanShift Clustering')
plt.show()

#Number of clusters set to 7 because DBSCAN Produced 7 Clusters
#Since visually we can see that DBSCAN is an accurate clustering methodology
#I used the same number of clusters DBSCAN produced when implementing KMeans
TSNE_KMeans = cluster.KMeans(n_clusters=7).fit(df_DAT)
plt.scatter(df_TSNE[0],df_TSNE[1],c=TSNE_KMeans.labels_.astype(float))
plt.title('TSNE Dimensionality Reduction --> KMeans')
plt.show()

TSNE_AP = cluster.AffinityPropagation().fit(df_DAT)
plt.scatter(df_TSNE[0],df_TSNE[1],c=TSNE_AP.labels_.astype(float))
plt.title('TSNE Dimensionality Reduction --> Affinity Propagation')
plt.show()

TSNE_Birch = cluster.Birch(n_clusters=5).fit(df_DAT)
plt.scatter(df_TSNE[0],df_TSNE[1],c=TSNE_Birch.labels_.astype(float))
plt.title('TSNE Dimensionality Reduction --> Birch')
plt.show()

"""
***
DIMENSIONALITY REDUCTION
***
"""

"""
TSNE (T-Distributed Stochastic Neighbor Embedding)
"""
#df_TSNE = manifold.TSNE(n_components=2).fit_transform(df_DAT)
#df_TSNE = pd.DataFrame(df_TSNE)
#TSNEPlot = df_TSNE.plot.scatter(x=0, y=1)
plt.scatter(df_TSNE[0],df_TSNE[1])
plt.title('TSNE')
plt.show()

"""
Isomap
"""
df_Isomap = manifold.Isomap(n_components=2).fit_transform(df_DAT)
df_Isomap = pd.DataFrame(df_Isomap)
#IsomapPlot = df_Isomap.plot.scatter(x=0,y=1)
plt.scatter(df_Isomap[0],df_Isomap[1])
plt.title('Isomap Dimensionality Reduction')
plt.show()

"""
Spectral Embedding
"""
df_SE= manifold.SpectralEmbedding(n_components=2)
df_SE = df_SE.fit_transform(df_DAT)

df_SE= pd.DataFrame(df_SE)
#SpectralEmbeddingPlot = df_SE.plot.scatter(x=0,y=1)
plt.scatter(df_SE[0],df_SE[1])
plt.title('Spectral Embedding')
plt.show()

"""
Principle Component Analysis
"""
df_PCA=decomposition.PCA(n_components=2).fit_transform(df_DAT)
df_PCA=pd.DataFrame(df_PCA)
#PCAPlot=df_PCA.plot.scatter(x=0,y=0)
plt.scatter(df_PCA[0],df_PCA[1])
plt.title('Principle Component Analysis')
plt.show()

"""
***
CLUSTERING
***
"""

"""
K-Means
"""
kmeans_DAT = cluster.KMeans(n_clusters=NUMCLUSTERS)
kmeans_DAT.fit(df_DAT)

kmeans_Centers = kmeans_DAT.cluster_centers_
kmeans_Results = kmeans_DAT.labels_

#print(kmeans_Centers)
df_DAT["KMeans"] = pd.Series(kmeans_Results)

"""
DBSCAN
"""
dbscan_DAT = cluster.DBSCAN(eps=2.5)
dbscan_DAT.fit(df_DAT)

dbscan_Results = dbscan_DAT.labels_
df_DAT["DBSCAN"] = pd.Series(dbscan_Results)

"""
MeanShift
"""

meanShift_DAT = cluster.MeanShift(bandwidth=20, bin_seeding=True)
meanShift_DAT.fit(df_DAT)

meanShift_Centers = meanShift_DAT.cluster_centers_
meanShift_Results = meanShift_DAT.labels_

df_DAT["MeanShift"] = pd.Series(meanShift_Results)

"""
Affinity Propogation <-- not desired results
"""
affinityP_DAT = cluster.AffinityPropagation(preference=-1)
affinityP_DAT.fit(df_DAT)

affinityP_Centers = affinityP_DAT.cluster_centers_
affinityP_Results = affinityP_DAT.labels_

df_DAT["AffinityPropogation"] = pd.Series(affinityP_Results)

"""
BIRCH
"""
birch_DAT = cluster.Birch(n_clusters=NUMCLUSTERS)
birch_DAT.fit(df_DAT)

birch_Centers = birch_DAT.subcluster_centers_
birch_Results = birch_DAT.labels_

df_DAT["Birch"] = pd.Series(birch_Results)

"""
Spectral Clustering <-- not desired results
"""
spectralC_DAT = cluster.SpectralClustering(n_clusters=NUMCLUSTERS)
spectralC_DAT.fit(df_DAT)

spectralC_Results = spectralC_DAT.labels_

#print(spectralC_Results)
df_DAT["SpectralClustering"] = pd.Series(spectralC_Results)


#TSNE DBSCAN clustering appened to the very end of the columns
df_DAT["TSNE & DBSCAN"] = pd.Series(TSNE_DBSCAN.labels_)

df_Final = df_PreDAT.join(df_DAT)

writer = pd.ExcelWriter('DAT_Clustering_Analysis.xlsx')
df_Final.to_excel(writer)
writer.save()