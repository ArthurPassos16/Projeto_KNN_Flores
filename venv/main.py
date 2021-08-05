import csv
import random
import math
import operator

def carregarBaseDeDados(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'r') as arquivo:
        lines = csv.reader(arquivo)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

def distanciaEuclidiana(inst1, inst2, tamanho):
    distancia = 0
    for x in range(tamanho):
        distancia += pow((inst1[x] - inst2[x]), 2)
    return math.sqrt(distancia)

def getNeighbors(trainingSet, testInstance, k):
    distancias = []
    tamanho = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = distanciaEuclidiana(testInstance, trainingSet[x], tamanho)
        distancias.append((trainingSet[x], dist))
    distancias.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distancias[x][0])
    return neighbors

def getResposta(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        resposta = neighbors[x][-1]
        if resposta in classVotes:
            classVotes[resposta] += 1
        else:
            classVotes[resposta] = 1
    sortedVotes =  sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAcuracia(testSet, predctions):
    correto = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predctions[x]:
            correto += 1
    return (correto/float(len(testSet))) * 100.0

def main():
    #preparo de dados
    trainingSet=[]
    testSet=[]
    split=0.66

    carregarBaseDeDados('iris.txt', split, trainingSet, testSet)
    print('Train Set: ' + repr(len(trainingSet)))
    print('Test Set: ' + repr(len(testSet)))

    #classificação
    predctions = []
    k=10
    for x in range(len(testSet)):
        neighbors =  getNeighbors(trainingSet, testSet[x], k)
        resultado = getResposta(neighbors)
        predctions.append(resultado)
        print('> Predição=' + repr(resultado) + ', atual=' + repr(testSet[x][-1]))

    acuracia = getAcuracia(testSet, predctions)
    print('Acurácia: ' + repr(acuracia) + '%')

main()

