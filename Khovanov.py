from itertools import chain, combinations
from F2Algebra import F2sparseMatrix, F2sparseEchelon, rowEchelonSparse, reduceRowSparse, columnEchelonSparse, reduceColumnSparse, kernel, image, homology

def powerSet(iterable):
    "powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = iterable
    #s = list(iterable)
    S = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    return {frozenset(x) for x in S}

class morseLink:
    def __init__(self, data, positiveCrossingNo, negativeCrossingNo):
        moveList = dict({(moveNo, data[moveNo]) for moveNo in data.keys()})
        self.moveList = moveList
        moveTurnSet = {n for n in moveList.keys()}
        crossingNos = set()
        for n in moveTurnSet:
            if moveList[n][1] == 'x':
                crossingNos.add(n)
        indexToCrossingNo = list(crossingNos)
        indexToCrossingNo.sort()
        self.indexToCrossingNo = indexToCrossingNo
        noCrossingNos = len(indexToCrossingNo)
        self.moveTurnSet = moveTurnSet
        self.indexToCrossingNo = indexToCrossingNo
        self.positiveCrossingNo = positiveCrossingNo
        self.negativeCrossingNo = negativeCrossingNo
        self.noCrossingNos = noCrossingNos
        

class resolvedMorseLink: #data is a dictionary where the entries are of the form (n,((i,j), move))
    def __init__(self, data): 
        self.moveList = dict({(moveNo, data[moveNo]) for moveNo in data.keys()})
        #self.heights = {n for n in self.moveList.keys()}
        #self.maxHeight = max(self.heights)
        #self.minHeight = min(self.heights)
        moveNo = len(self.moveList.keys())
        activeHeights = list({n for n in self.moveList.keys()})
        activeHeights.sort()
        cupGroup = set()
        runningDict = dict({})
        crossingToComponentsDict = dict({})
        for n in range(moveNo):
            activeHeight = activeHeights[n]
            activeTuple = self.moveList[activeHeight][0]
            activeMove = self.moveList[activeHeight][1]
            if activeMove == 0:
                cupGroup.add(frozenset({activeHeight}))
                for i in activeTuple:
                    runningDict[i] = activeHeight
            if activeMove == 1:
                setToBeAdded = frozenset()
                setsToBeRemoved = frozenset()
                for i in activeTuple:
                    curveComponentNo = runningDict[i]
                    for x in cupGroup:
                        if curveComponentNo in x:
                            setToBeAdded = setToBeAdded | x
                            setsToBeRemoved = setsToBeRemoved | frozenset({x})
                    cupGroup = cupGroup - setsToBeRemoved | frozenset({setToBeAdded})
            if activeMove == 'stay':
                crossingToComponentsDict[activeHeight] = (runningDict[activeTuple[0]], runningDict[activeTuple[1]])
                
            if activeMove == '10':
                
                setToBeAdded = frozenset()
                setsToBeRemoved = frozenset()
                for i in activeTuple:
                    curveComponentNo = runningDict[i]
                    for x in cupGroup:
                        if curveComponentNo in x:
                            setToBeAdded = setToBeAdded | x
                            setsToBeRemoved = setsToBeRemoved | frozenset({x})
                    cupGroup = cupGroup - setsToBeRemoved | frozenset({setToBeAdded})
                belowHeight = runningDict[activeTuple[0]]
                #ends the capping off part, starts the cup part
                cupGroup.add(frozenset({activeHeight}))
                for i in activeTuple:
                    runningDict[i] = activeHeight
                crossingToComponentsDict[activeHeight] = (belowHeight, activeHeight)           
        self.components = {min(x) for x in cupGroup}
        #components are indexed by their minimum point (which must be index 0)
        self.componentNo = len(cupGroup)
        for n in crossingToComponentsDict.keys():
            componentSet = set()
            for x in cupGroup:
                if crossingToComponentsDict[n][0] in x or crossingToComponentsDict[n][1] in x:
                    componentSet.add(min(x))
            crossingToComponentsDict[n] = componentSet
        self.crossingToComponentsDict = crossingToComponentsDict
        #print(crossingToComponentsDict)
        
        
def resolution(diagram, u):
    #u has to be in the power set of {0,1,...,n-1}, where n is the number of crossings
    moveList = dict({(n,diagram.moveList[n]) for n in diagram.moveList.keys()})
    noCrossingNos = diagram.noCrossingNos
    indexToCrossingNo = diagram.indexToCrossingNo
    for n in range(noCrossingNos):
        activeTuple = moveList[indexToCrossingNo[n]][0]
        if moveList[indexToCrossingNo[n]][2] == 'lower':
            if n in u:
                moveList[indexToCrossingNo[n]] = (activeTuple, '10')
            else:
                moveList[indexToCrossingNo[n]] = (activeTuple, 'stay')
        elif moveList[indexToCrossingNo[n]][2] == 'upper':
            if n in u:
                moveList[indexToCrossingNo[n]] = (activeTuple, 'stay')
            else:
                moveList[indexToCrossingNo[n]] = (activeTuple, '10')
    return resolvedMorseLink(moveList)

class khovanovBasis:
    def __init__(self, diagram):
        noCrossingNos = diagram.noCrossingNos
        indexToCrossingNo = diagram.indexToCrossingNo
        negativeCrossingNo = diagram.negativeCrossingNo
        positiveCrossingNo = diagram.positiveCrossingNo
        minQuantumGrading = positiveCrossingNo - 2*negativeCrossingNo - 2*noCrossingNos
        maxQuantumGrading = positiveCrossingNo - 2*negativeCrossingNo + noCrossingNos + 2*noCrossingNos
        powerSetDict = tuple(powerSet(list((i for i in range(m)))) for m in range(2*noCrossingNos + 1))
        setOfUValues = powerSet(list(n for n in range(noCrossingNos))) #locations on the Kauffman cube
        indexToComponentDict = dict({}) #going to be a dictionary that takes a cube position u and outputs a sequencing of components
        componentToIndexDict = dict({})
        gradingsToGeneratorsDict = dict({}) #This dict will take in a quantum grading and homological grading and output the generators
        componentNoDict = dict({})
        qhToSparseMatrixSetup = dict({})
        crossingToComponentsDict = dict({})
        componentToCrossingsDict = dict({})
        for q in range(minQuantumGrading, maxQuantumGrading + 1):
            for n in range(-1, noCrossingNos + 1):
                gradingsToGeneratorsDict[(q,n)] = set()
                qhToSparseMatrixSetup[(q,n)] = set()
        qGradingDict = dict({})
        resolutionDict = dict({})
        for u in setOfUValues:
            resolutionDict[u] = resolution(diagram,u)
            uResolution = resolutionDict[u]
            crossingToComponentsDict[u] = uResolution.crossingToComponentsDict
            componentNoDict[u] = uResolution.componentNo
            componentTuple = tuple(uResolution.components)
            indexToComponentDict[u] = dict({(k, componentTuple[k]) for k in range(uResolution.componentNo)})
            componentToIndexDict[u] = dict({(componentTuple[k], k) for k in range(uResolution.componentNo)})
            homGrading = len(u)
            for S in powerSetDict[componentNoDict[u]]: #S represents the components that are labeled with x
                qGrading = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (uResolution.componentNo - len(S)) - (len(S))
                gradingsToGeneratorsDict[(qGrading, homGrading)].add((u,S))
                qGradingDict[(u,S)] = qGrading
        qhToIndexToGenerator = dict({})
        qhToGeneratorToIndex = dict({})
        qhToGeneratorNo = dict({})
        for q in range(minQuantumGrading, maxQuantumGrading + 1):
            for n in range(-1, noCrossingNos + 1):
                generatorTuple = tuple(gradingsToGeneratorsDict[(q,n)])
                qhToGeneratorNo[(q,n)] = len(generatorTuple)
                indexToGenerator = dict({(i, generatorTuple[i]) for i in range(qhToGeneratorNo[(q,n)])})
                generatorToIndex = dict({(generatorTuple[i], i) for i in range(qhToGeneratorNo[(q,n)])})
                qhToIndexToGenerator[(q,n)] = indexToGenerator
                qhToGeneratorToIndex[(q,n)] = generatorToIndex
        self.qhToGeneratorNo = qhToGeneratorNo
        self.qhToIndexToGenerator = qhToIndexToGenerator
        #Now is the Khovanov differential part
        for u in setOfUValues:
          for i in {j for j in range(noCrossingNos)} - u:
            v = u | {i}
            uSpecialComponents = crossingToComponentsDict[u][indexToCrossingNo[i]]
            vSpecialComponents = crossingToComponentsDict[v][indexToCrossingNo[i]]
            if componentNoDict[u] < componentNoDict[v]:
                for uS in powerSetDict[componentNoDict[u]]:
                    uLabeling = {indexToComponentDict[u][s] for s in uS}
                    vLabelingOfOtherComponents = uLabeling - uSpecialComponents
                    qGradingU = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (componentNoDict[u] - len(uS)) - (len(uS))
                    qGradingV = qGradingU
                    jCoordinate = qhToGeneratorToIndex[(qGradingU,len(u))][(u,uS)]
                    if min(uSpecialComponents) in uLabeling:
                        generatorComponentForm = vLabelingOfOtherComponents | vSpecialComponents
                        vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                        #qGradingV = positiveCrossingNo - 2 * negativeCrossingNo + len(v) + (componentNoDict[v] - len(vS)) - (len(vS))
                        iCoordinate = qhToGeneratorToIndex[(qGradingV, len(v))][(v, vS)]
                        qhToSparseMatrixSetup[(qGradingU,len(u))].add((iCoordinate, jCoordinate))
                    else:
                        generatorsComponentForm = (vLabelingOfOtherComponents | {min(vSpecialComponents)}, vLabelingOfOtherComponents | {max(vSpecialComponents)})
                        vS0 = frozenset(componentToIndexDict[v][x] for x in generatorsComponentForm[0])
                        vS1 = frozenset(componentToIndexDict[v][x] for x in generatorsComponentForm[1])
                        iCoordinate0 = qhToGeneratorToIndex[(qGradingV, len(v))][(v, vS0)]
                        iCoordinate1 = qhToGeneratorToIndex[(qGradingV, len(v))][(v, vS1)]
                        qhToSparseMatrixSetup[(qGradingU,len(u))].update(((iCoordinate0, jCoordinate,), (iCoordinate1, jCoordinate)))
                        
            if componentNoDict[u] > componentNoDict[v]:
                for uS in powerSetDict[componentNoDict[u]]:
                    uLabeling = {indexToComponentDict[u][s] for s in uS}
                    vLabelingOfOtherComponents = uLabeling - uSpecialComponents
                    qGradingU = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (componentNoDict[u] - len(uS)) - (len(uS))
                    qGradingV = qGradingU
                    jCoordinate = qhToGeneratorToIndex[(qGradingU,len(u))][(u,uS)]
                    if len(uSpecialComponents & uLabeling) == 1:
                        generatorComponentForm = vLabelingOfOtherComponents | vSpecialComponents
                        vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                        iCoordinate = qhToGeneratorToIndex[(qGradingV, len(v))][(v, vS)]
                        qhToSparseMatrixSetup[(qGradingU,len(u))].add((iCoordinate,jCoordinate))
                    elif len(uSpecialComponents & uLabeling) == 0:
                        generatorComponentForm = vLabelingOfOtherComponents
                        vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                        iCoordinate = qhToGeneratorToIndex[(qGradingV, len(v))][(v, vS)]
                        qhToSparseMatrixSetup[(qGradingU,len(u))].add((iCoordinate,jCoordinate))
        qhToSparseMatrix = dict({})
        for q in range(minQuantumGrading, maxQuantumGrading + 1):
            for n in range(-1, noCrossingNos + 1):
                sparseMatrix = F2sparseMatrix(qhToSparseMatrixSetup[(q,n)])
                sparseMatrix.officialColumnRange = (0, qhToGeneratorNo[(q,n)] - 1)
                qhToSparseMatrix[(q,n)] = sparseMatrix
        self.qhToSparseMatrix = qhToSparseMatrix
        
class flowCategory:
    def __init__(self, khovanovGenerators, qGrading, bottomHGrading):
        nGeneratorDict = khovanovGenerators.qhToIndexToGenerator[(qGrading,bottomHGrading)]
        nPlusOneGeneratorDict = khovanovGenerators.qhToIndexToGenerator[(qGrading,bottomHGrading + 1)]
        nPlusTwoGeneratorDict = khovanovGenerators.qhToIndexToGenerator[(qGrading,bottomHGrading + 2)]
        self.nGeneratorDict = nGeneratorDict 
        self.nPlusOneGeneratorDict = nPlusOneGeneratorDict
        self.nPlusTwoGeneratorDict = nPlusTwoGeneratorDict
        nMatrix = khovanovGenerators.qhToSparseMatrix[(qGrading, bottomHGrading)]
        nPlusOneMatrix = khovanovGenerators.qhToSparseMatrix[(qGrading, bottomHGrading + 1)]
        nPlusTwoMatrix = khovanovGenerators.qhToSparseMatrix[(qGrading, bottomHGrading + 2)]
        pontrjaginThoms = dict({})
        boundaries = dict({})
        yzPositionToYNoDict = dict({})
        for x in nMatrix.columns:
            for y in nMatrix.entriesInColumn[nMatrix.columnDict[x]]:
                if y in nPlusOneMatrix.columns:
                    for z in nPlusOneMatrix.entriesInColumn[nPlusOneMatrix.columnDict[y]]:
                        yzDifference = min(nPlusTwoGeneratorDict[z][0]-nPlusOneGeneratorDict[y][0])
                        #print(nPlusTwoGeneratorDict[z][0])
                        #print(nPlusOneGeneratorDict[y][0])
                        #print(yzDifference)
                        yzPositionToYNoDict[(y,z)] = len(nPlusTwoGeneratorDict[z][0] & set(range(yzDifference)))
                        #print(yzPositionToYNoDict[(y,z)])
                        pontrjaginThoms[(x,z)] = set()
                        boundaries[(y,z)] = set()
        self.yzPositionToYNoDict = yzPositionToYNoDict
        for x in nMatrix.columns:
            for y in nMatrix.entriesInColumn[nMatrix.columnDict[x]]:
                if y in nPlusOneMatrix.columns:
                    for z in nPlusOneMatrix.entriesInColumn[nPlusOneMatrix.columnDict[y]]:
                        pontrjaginThoms[(x,z)].add(y)
                        boundaries[(y,z)].add(x)
                        
        for w in pontrjaginThoms.keys():
            if len(pontrjaginThoms[w]) == 2:
                pontrjaginThoms[w] = {tuple(pontrjaginThoms[w])}
            elif len(pontrjaginThoms[w]) == 4:
                fourTuple = tuple(pontrjaginThoms[w])
                if nPlusOneGeneratorDict[fourTuple[0]][0] == nPlusOneGeneratorDict[fourTuple[1]][0]:
                    pontrjaginThoms[w] = {tuple(fourTuple[0], fourTuple[2]), (fourTuple[1], fourTuple[3])}
                else: pontrjaginThoms[w] = {tuple(fourTuple[0], fourTuple[1]), (fourTuple[2], fourTuple[3])}
        self.pontrjaginThoms = pontrjaginThoms
        self.boundaries = boundaries


class matchings:
    def __init__(self, flowCategory, kernel):
        pontrjaginThoms = flowCategory.pontrjaginThoms
        boundaries = flowCategory.boundaries
        activePontrjaginThomsKeys = set()
        activePontrjaginThoms = dict({})
        activeBoundaryKeys = set()
        activeBoundaries = dict({})
        for v in pontrjaginThoms.keys():
            if (v[0] in kernel):
                activePontrjaginThomsKeys.add(v)
        for v in activePontrjaginThomsKeys:
            activePontrjaginThoms[v] = pontrjaginThoms[v]
        for w in boundaries.keys():
            if (boundaries[w] & kernel != frozenset({})):
                activeBoundaryKeys.add(w)
        for w in activeBoundaryKeys:
            activeBoundaries[w] = boundaries[w] & kernel
        #print(activeBoundaries)
        boundaryMatchings = dict({})
        for w in activeBoundaryKeys:
            wBoundaryTuple = tuple(activeBoundaries[w])
            wBoundaryNo = len(wBoundaryTuple)
            halfNo = wBoundaryNo // 2
            subTuple1 = tuple(wBoundaryTuple[n] for n in range(halfNo))
            subTuple2 = tuple(wBoundaryTuple[n] for n in range(halfNo, wBoundaryNo))
            boundaryMatchings[w] = {(subTuple1[i], subTuple2[i]) for i in range(halfNo)}
        self.activePontrjaginThomsKeys = activePontrjaginThomsKeys
        self.activeBoundaryKeys = activeBoundaryKeys
        self.activePontrjaginThoms = activePontrjaginThoms
        self.boundaryMatchings = boundaryMatchings
        self.activeZs = {w[1] for w in activePontrjaginThomsKeys}
        #print(self.boundaryMatchings)

        
def zCoefficient(flowCategory, matchings, z):
    #zActivePontrjaginThoms = set()
    #zBoundaryMatchings = set()
    yzPositionToYNoDict = flowCategory.yzPositionToYNoDict
    pontrjaginThomAdjacency = dict({})
    boundaryAdjacencies = dict({})
    xyPairs = set()
    for v in matchings.activePontrjaginThomsKeys:
        if v[1] == z:
            #additionalPontrjaginThoms = {(v[0], (y[0], y[1])) for y in matchings.activePontrjaginThoms[v]}
            #print(additionalPontrjaginThoms)
            #zActivePontrjaginThoms = zActivePontrjaginThoms | additionalPontrjaginThoms
            for y in matchings.activePontrjaginThoms[v]:
                pontrjaginThomAdjacency[(v[0], y[0])] = (v[0], y[1])
                pontrjaginThomAdjacency[(v[0], y[1])] = (v[0], y[0])
                xyPairs = xyPairs | {(v[0], y[0]), (v[0], y[1])}
    for w in matchings.activeBoundaryKeys:
        if w[1] == z:
            #additionalMatchings = {((x[0], x[1]), w[0]) for x in matchings.boundaryMatchings[w]}
            #zBoundaryMatchings = zBoundaryMatchings | additionalMatchings
            for x in matchings.boundaryMatchings[w]:
                boundaryAdjacencies[(x[0], w[0])] = (x[1], w[0])
                boundaryAdjacencies[(x[1], w[0])] = (x[0], w[0])
    
    leftOverXyPairList = list(xyPairs)

    cycleSet = set()
    while leftOverXyPairList != []:
        boundaryAdjacency1 = leftOverXyPairList[0]
        boundaryAdjacency2 = boundaryAdjacencies[boundaryAdjacency1]
        leftOverXyPairList.remove(boundaryAdjacency1)
        leftOverXyPairList.remove(boundaryAdjacency2)
        cycleToAdd = [(boundaryAdjacency1, boundaryAdjacency2)]
        x = pontrjaginThomAdjacency[boundaryAdjacency2]
        while pontrjaginThomAdjacency[boundaryAdjacency2] != cycleToAdd[0][0]:
            boundaryAdjacency1 = pontrjaginThomAdjacency[boundaryAdjacency2]
            boundaryAdjacency2 = boundaryAdjacencies[boundaryAdjacency1]
            cycleToAdd.append((boundaryAdjacency1,boundaryAdjacency2))
            leftOverXyPairList.remove(boundaryAdjacency1)
            leftOverXyPairList.remove(boundaryAdjacency2)
        cycleSet.add(tuple(cycleToAdd))
    
    Z2Element = 0
    #for K in cycleSet:
    #    cycleOfNumbers = tuple(yzPositionToYNoDict[(K[i][0][1], z)] for i in range(len(K)))
    #    KElement = 0
    #    for i in range(len(K)):
    #        if i == len(K)-1:
    #            KElement = KElement + K[len(K)-1]*K[0]
    #        else:
    #            Kelement = KElement + K[i] * K[i+1]
        #noBackwardArrows
    return cycleSet

conwayKnotDict = dict({(1,((5,10), 0)), (2,((1,4), 0)), (3,((2,3), 0)), (4, ((4,5), 'x', 'lower')), (5,((6,7), 0)), (6,((8,9), 0)), (7, ((3,4), 'x', 'upper')), (8, ((5,6), 'x', 'lower')), (9, ((7,8), 'x', 'lower')), (10, ((9,10), 'x', 'upper')), (11, ((2,3), 'x', 'lower')), (12, ((4,5), 'x', 'upper')), (13, ((6,7), 'x', 'upper')), (14, ((9,10), 'x', 'upper')), (15, ((3,4), 'x', 'lower')), (16,((5,6), 1)), (17, ((3,4), 'x', 'lower')), (18,((4,7), 1)), (19,((3,8), 1)), (20,((2,9), 1)), (21,((1,10), 1))})

figure8KnotDict = dict({(1,((1,2), 0)), (2,((3,4), 0)), (3, ((2,3), 'x', 'lower')), (4, ((2,3), 'x', 'lower')), (5, ((3,4), 'x', 'upper')), (6, ((3,4), 'x', 'upper')), (7,((3,4), 1)), (8,((1,4), 1))})
ladyBugKnotDict = dict({(1,((1,2), 0)), (2,((3,4), 0)), (3, ((2,3), 'x', 'lower')), (4, ((2,3), 'x', 'upper')), (5,((1,2), 1)), (6,((3,4), 1))})
knotDict = figure8KnotDict
knotMorseLink = morseLink(knotDict,2,2)
knot = khovanovBasis(knotMorseLink)
a = knot.qhToSparseMatrix[(-1,0)]
b = knot.qhToSparseMatrix[(-1,1)]
c = knot.qhToSparseMatrix[(-1,2)]
print(a)
print(b)
print(kernel(b))
print(image(a))
print(b*a)
print('firstHomology:', homology(b,a))
print('secondHomology:', homology(c,b))
f = flowCategory(knot, -1, 1)
print('pontrjaginThoms:', f.pontrjaginThoms)
print('boundaries:', f.boundaries)
bM = matchings(f, {2,3,6,7})
print(zCoefficient(f, bM,1))
