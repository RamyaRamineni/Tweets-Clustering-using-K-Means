# Tweets-Clustering-using-K-Means
To cluster tweets by utilizing Jaccard Distance metric and K-means clustering algorithm.

Development Environment:
Tweets Clustering using k-means program is developed in python and tested in Windows Operating System

Usage:
The program is compatible with Python 3.5 and 3.6.

Inputs Required:
(1) The number of clusters K (default to K=25).
(2) A real world dataset sampled from Twitter during the Boston Marathon Bombing event in
April 2013 that contains 251 tweets. The tweet dataset is in JSON format and can be downloaded
from http://www.utdallas.edu/~axn112530/cs6375/unsupervised/Tweets.json
(3) The list of initial centroids can be downloaded from:
http://www.utdallas.edu/~axn112530/cs6375/unsupervised/InitialSeeds.txt


Steps to COMPILE and RUN:
tweets-k-means.py <numberOfClusters> <initialSeedsFile> <TweetsDataFile> > <outputFile>

The current code was run like below command in cmd:
python tweets-k-means.py 25 InitialSeeds.txt Tweets.json > result.txt
