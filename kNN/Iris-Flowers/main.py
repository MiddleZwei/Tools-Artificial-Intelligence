import math
import operator
from pip._vendor.distlib.compat import raw_input


# 1. Handle data

def loadDataset(trainFile, testFile, trainingSet=[], testSet=[]):
    # train.txt
    with open(trainFile, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        trainDataset = list(lines)
        for x in range(len(trainDataset) - 1):
            for y in range(4):
                trainDataset[x][y] = float(trainDataset[x][y])
            trainingSet.append(trainDataset[x])

    # test.txt
    with open(testFile, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        testDataset = list(lines)
        for x in range(len(testDataset) - 1):
            for y in range(4):
                testDataset[x][y] = float(testDataset[x][y])
            testSet.append(testDataset[x])



# 2. Similarity

# Euclidean distance
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)



# 3. Neighbors

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors



# 4. Response

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]



# 5. Accuracy

def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0



# 6. Get custom input

def getCustomInput(custom):
    try:
        for i in range(4):
            # print("Enter "+i+"/4"+" number: ")
            custom[0][i] = float(input("Enter " + str(i) + "/3" + " number: "))
        custom[0][4] = raw_input("Enter the name of the flower: ")
    except ValueError:
        print("An invalid value.")
    return custom



# 7. Main

def main():
    # prepare data
    trainingSet = []
    testSet = []
    loadDataset('train.txt', 'test.txt', trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print("Test set: " + repr(len(testSet)))

    # generate predictions
    predictions = []
    k = 0
    try:
        k = int(input('Enter k: '))
    except ValueError:
        print("Not an integer value")
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))

    # custom test input
    # 1, 1, 1, 1 <- Iris-virginica
    print("CUSTOM INPUT")
    custom = [[0.0 for x in range(5)] for x in range(1)]
    custom = getCustomInput(custom)

    # predict for the custom input
    neighbors = getNeighbors(trainingSet, custom, k)
    result = getResponse(neighbors)
    predictions.append(result)
    testSet.append(custom[0])
    print('> predicted=' + repr(result) + ', actual=' + repr(custom[0][-1]))



    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')



main()
