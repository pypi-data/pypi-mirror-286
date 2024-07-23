MDANCE (Molecular Dynamics Analysis with *N*-ary Clustering Ensembles) is a flexible *n*-ary clustering package that provides a set of tools for clustering Molecular Dynamics trajectories. The package is written in Python and an extension of the *n*-ary similarity framework. The package is designed to be modular and extensible, allowing for the addition of new clustering algorithms and similarity metrics.
<h3 align="center">
    <p><a href="https://github.com/mqcomplab/MDANCE"><img src="https://img.shields.io/badge/-MDANCE-000000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/mqcomplab/MDANCE" alt="MDANCE" width=auto height="25"></a></p>
    </h3>

## Background
Molecular Dynamics (MD) simulations are a powerful tool for studying the dynamics of biomolecules. However, the analysis of MD trajectories is challenging due to the large amount of data generated. Clustering is an unsupervised machine learning approach to group similar frames into clusters. The clustering results can be used to reveal the structure of the data, identify the most representative structures, and to study the dynamics of the system.

## Installation
```bash
$ pip install mdance
```
To check for proper installation, run the following command:
```python
>>> import mdance
>>> mdance.__version__
```

## Clustering Algorithms
### NANI

*k*-Means *N*-Ary Natural Initiation ([NANI](https://pubs.acs.org/doi/10.1021/acs.jctc.4c00308)) is an algorithm for selecting initial centroids for *k*-Means clustering. NANI is an extension of the *k*-Means++ algorithm. NANI stratifies the data to high density region and perform diversity selection on top of the it to select the initial centroids. This is a deterministic algorithm that will always select the same initial centroids for the same dataset and improve on *k*-means++ by reducing the number of iterations required to converge and improve the clustering quality.

**[A tutorial is available for NANI](https://github.com/mqcomplab/MDANCE/blob/main/tutorials/nani.md).**

Please refer to the [NANI paper](https://pubs.acs.org/doi/10.1021/acs.jctc.4c00308).

Example usage:

```python
from mdance.cluster.nani import KmeansNANI

data = np.load('data.npy')
n_clusters = 4
mod = KmeansNANI(data=data, n_clusters=n_clusters, metric='MSD', N_atoms=1,
                 init_type='comp_sim', percentage=10)
initiators = mod.initiate_kmeans()
initiators = initiators[:n_clusters]
kmeans = KMeans(n_clusters, init=initiators, n_init=1, random_state=None)
kmeans.fit(data)
```

## Clustering Postprocessing
### PRIME
Protein Retrieval via Integrative Molecular Ensembles (PRIME)</b> is a novel algorithm that predicts the native structure of a protein from simulation or clustering data. These methods perfectly mapped all the structural motifs in the studied systems and required unprecedented linear scaling.

**[A tutorial is available for PRIME](https://github.com/mqcomplab/MDANCE/blob/main/tutorials/prime.md).**

Please refer to the [PRIME paper](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.4c00362). 