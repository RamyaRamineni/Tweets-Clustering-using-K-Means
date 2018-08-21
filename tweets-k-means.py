import json
import sys
import re, string
from nltk.corpus import stopwords

regex = re.compile('[%s]' % re.escape(string.punctuation))
stopWordsList = stopwords.words('english')

def main(clusterNum, tweetsJson, initialSeeds):
	
	k = int(clusterNum)
	tweets = {}
	with open(tweetsJson, 'r') as tweetsFile:
		for i in tweetsFile:
			line = json.loads(i)
			tweets[line['id']] = line

	initSeeds = []		
	with open(initialSeeds, 'r') as seedsfile:
		for i in seedsfile:
			line = int(i.rstrip(',\n'))
			initSeeds.append(line)

	clustersId = {} # cluster to tweetID
	idClusters = {} # tweetID to cluster rev
	jaccardDistMatrix = {} #jaccard distance in a matrix

	# Initialize tweets to no cluster
	for i in tweets:
		idClusters[i] = -1

	# Initialize clusters with seeds
	for i in range(k):
		clustersId[i] = set([initSeeds[i]])
		idClusters[initSeeds[i]] = i

	for i in tweets:
	 	jaccardDistMatrix[i] = {}
	 	setA = set(preProcess(tweets[i]['text']))	 	
	 	for j in tweets:
	 		if j not in jaccardDistMatrix:
	 			jaccardDistMatrix[j] = {}
	 		setB = set(preProcess(tweets[j]['text']))
	 		distance = calcJaccardDistance(setA, setB)
	 		jaccardDistMatrix[i][j] = distance
	 		jaccardDistMatrix[j][i] = distance
	newClustersId, newIdClusters = buildNewClusters(tweets, clustersId, idClusters, k, jaccardDistMatrix)
	clustersId = newClustersId
	idClusters = newIdClusters

	iterations = 1
	while iterations < 1000:
		newClustersId, newIdClusters = buildNewClusters(tweets, clustersId, idClusters, k, jaccardDistMatrix)
		iterations += 1
		if idClusters != newIdClusters:
			clustersId = newClustersId
			idClusters = newIdClusters
		else:
			break
	for i in clustersId:
		print(str(i) + ':' + ','.join(map(str,clustersId[i])))


def buildNewClusters(tweets, clustersId, idClusters, k, jaccardDistMatrix):
	newClustersId = {}
	newIdClusters = {}
	for i in range(k):
		newClustersId[i] = set()
	for i in tweets:
		minDistance = float("inf")
		minCluster = idClusters[i]

            # Calculate min average distance to each cluster
		for j in clustersId:
			dist = 0
			count = 0
			for l in clustersId[j]:
				dist += jaccardDistMatrix[i][l]
				count += 1
			if count > 0:
				avgDistance = dist/float(count)
				if minDistance > avgDistance:
					minDistance = avgDistance
					minCluster = j
		newClustersId[minCluster].add(i)
		newIdClusters[i] = minCluster
	return newClustersId, newIdClusters


def preProcess(line):        
	
	words = line.lower().strip().split(' ')
	for word in words:
		word = word.rstrip().lstrip()
		#print(word)
		#if not (re.match(r'^https?:\/\/.*[\r\n]*', word)) and not (re.match('^@.*', word)) and not (re.match('\s', word)) and word not in (stopWordsList) and (word != 'rt') and (word != ''):
		if not (re.match(r'^https?:\/\/.*[\r\n]*', word)) and not (re.match('^@.*', word)) and word not in (stopWordsList):
			yield regex.sub('', word)
	#print(words)
	return words
	
#Jaccard Distance
def calcJaccardDistance(A, B):   
	#print(len(A.union(B)))    
	try: 
		return (1 - float(len(A.intersection(B))) / float(len(A.union(B))))
	except ZeroDivisionError:
		print("ERROR")
        
#Function to read input from the command line and call main function
if __name__ == "__main__":
	
	if (len(sys.argv)) < 3 :   #Print error if number of arguments is less than 3
		print("Invalid number of arguments")
	else:
		clusterNum = sys.argv[1]		
		tweetsJson = sys.argv[3]
		initialSeeds = sys.argv[2]		
		main(clusterNum, tweetsJson, initialSeeds) # main function call
		
