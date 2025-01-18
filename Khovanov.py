from itertools import chain, combinations
from F2Algebra import *

def powerSet(iterable):
    "powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = iterable
    #s = list(iterable)
    S = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    return {frozenset(x) for x in S}

class morseLink:
    def __init__(self, moveTuple):#input (positiveCrossingNo, negativeCrossingNo)
        moveNo = len(moveTuple)
        self.moveTuple = moveTuple
        crossingNos = set()
        for n in range(len(moveTuple)):
            if moveTuple[n][1] == '+' or moveTuple[n][1] == '-':
                crossingNos.add(n)
        indexToCrossingNo = list(crossingNos)
        indexToCrossingNo.sort()
        self.indexToCrossingNo = indexToCrossingNo
        noCrossingNos = len(indexToCrossingNo)
        self.indexToCrossingNo = indexToCrossingNo
        self.noCrossingNos = noCrossingNos
        #Now we find the number of components in the link
        cupGroup = set()
        runningDict = dict({})
        for n in range(moveNo):
            activeHeight = n
            activeTuple = self.moveTuple[activeHeight][0]
            activeMove = self.moveTuple[activeHeight][1]
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
            if activeMove == '+' or activeMove == '-':
                previousRunningDictEntries = (runningDict[activeTuple[0]], runningDict[activeTuple[1]])
                for i in activeTuple:
                    runningDict[activeTuple[0]] = previousRunningDictEntries[1]
                    runningDict[activeTuple[1]] = previousRunningDictEntries[0]
        componentMins = {min(x) for x in cupGroup}
        self.componentNo = len(componentMins)
        print('components:', self.componentNo)
        #Now we figure out how many crossings are positive and negative
        crossingDirectionsDict = dict([[x,[0,0]] for x in crossingNos])
        widths = set()
        for n in range(moveNo):
            for i in self.moveTuple[n][0]:
                widths.add(i)
        movesWidthI = dict()
        for i in widths:
            movesWidthI[i] = set()
        for n in range(moveNo):
            for i in moveTuple[n][0]:
                movesWidthI[i].add(n)
        #print('widths:', movesWidthI)
        for k in componentMins:
            #print('k:', k)
            currentComponent = k
            #print('startingComponent:', currentComponent)
            currentStrandWidth = moveTuple[k][0][0]
            nextStrandWidth = moveTuple[k][0][1]
            nextComponent = min(movesWidthI[nextStrandWidth] & set(range(k+1, moveNo + 1)))
            #print('nextComponent:', nextComponent)
            direction = 'up'
            counter = 0
            while nextComponent != k:
                currentComponent = nextComponent
                currentStrandWidth = nextStrandWidth
                activeTuple = moveTuple[currentComponent][0]
                #print(currentComponent, currentStrandWidth, activeTuple)
                if currentStrandWidth == activeTuple[0]:
                    nextStrandWidth = activeTuple[1]
                elif currentStrandWidth == activeTuple[1]:
                    nextStrandWidth = activeTuple[0]
                else:
                    print('help!')
                if moveTuple[currentComponent][1] == 0:
                    nextComponent = min(movesWidthI[nextStrandWidth] & set(range(currentComponent + 1, moveNo + 1)))
                    direction = 'up'
                elif moveTuple[currentComponent][1] == 1:
                    nextComponent = max(movesWidthI[nextStrandWidth] & set(range(currentComponent)))
                    direction = 'down'
                elif moveTuple[currentComponent][1] == '+' or moveTuple[currentComponent][1] == '-':
                    if direction  == 'up':
                        if currentStrandWidth == moveTuple[currentComponent][0][0]:
                            crossingDirectionsDict[currentComponent][0] = 'up'
                        elif currentStrandWidth == moveTuple[currentComponent][0][1]:
                            crossingDirectionsDict[currentComponent][1] = 'up'
                    elif direction == 'down':
                        if currentStrandWidth == moveTuple[currentComponent][0][0]:
                            crossingDirectionsDict[currentComponent][1] = 'down'
                        elif currentStrandWidth == moveTuple[currentComponent][0][1]:
                            crossingDirectionsDict[currentComponent][0] = 'down'
                    if direction == 'up':
                        nextComponent = min(movesWidthI[nextStrandWidth] & set(range(currentComponent + 1, moveNo + 1)))
                    elif direction == 'down':
                        nextComponent = max(movesWidthI[nextStrandWidth] & set(range(currentComponent)))
        positiveCrossingNo = 0
        negativeCrossingNo = 0
        for x in crossingNos:
            if moveTuple[x][1] == '+':
                if (crossingDirectionsDict[x][0] == 'up' and crossingDirectionsDict[x][1] == 'up') or (crossingDirectionsDict[x][0] == 'down' and crossingDirectionsDict[x][1] == 'down'):
                    negativeCrossingNo += 1
                else:
                    positiveCrossingNo += 1
            elif moveTuple[x][1] == '-':
                if (crossingDirectionsDict[x][0] == 'up' and crossingDirectionsDict[x][1] == 'up') or (crossingDirectionsDict[x][0] == 'down' and crossingDirectionsDict[x][1] == 'down'):
                    positiveCrossingNo += 1
                else:
                    negativeCrossingNo += 1
            else:
                print('help')
        self.positiveCrossingNo = positiveCrossingNo
        self.negativeCrossingNo = negativeCrossingNo
            
class resolvedMorseLink: #data is a dictionary where the entries are of the form (n,((i,j), move))
    def __init__(self, data):
        moveTuple = tuple(data)
        self.moveTuple = moveTuple
        moveNo = len(moveTuple)
        cupGroup = set()
        runningDict = dict({})
        crossingToComponentsDict = dict({})
        for n in range(moveNo):
            activeHeight = n
            activeTuple = self.moveTuple[activeHeight][0]
            activeMove = self.moveTuple[activeHeight][1]
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
            componentList = []
            for x in cupGroup:
                if crossingToComponentsDict[n][0] in x and crossingToComponentsDict[n][1] in x:
                    componentList = [min(x)]
                    break
                elif crossingToComponentsDict[n][0] in x:
                    componentList.insert(0, min(x))
                elif crossingToComponentsDict[n][1] in x:
                    componentList.insert(1, min(x))
            crossingToComponentsDict[n] = tuple(componentList)
        self.crossingToComponentsDict = crossingToComponentsDict
        #print(crossingToComponentsDict)
        
        
def resolution(diagram, u):
    #u has to be in the power set of {0,1,...,n-1}, where n is the number of crossings
    moveList = list(diagram.moveTuple)
    noCrossingNos = diagram.noCrossingNos
    indexToCrossingNo = diagram.indexToCrossingNo
    for n in range(noCrossingNos):
        activeTuple = moveList[indexToCrossingNo[n]][0]
        if moveList[indexToCrossingNo[n]][1] == '-':
            if n in u:
                moveList[indexToCrossingNo[n]] = (activeTuple, '10')
            else:
                moveList[indexToCrossingNo[n]] = (activeTuple, 'stay')
        elif moveList[indexToCrossingNo[n]][1] == '+':
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
        minHomGrading = -1 - negativeCrossingNo
        maxHomGrading = noCrossingNos - negativeCrossingNo
        minQuantumGrading = positiveCrossingNo - 2*negativeCrossingNo - 2*noCrossingNos
        maxQuantumGrading = positiveCrossingNo - 2*negativeCrossingNo + noCrossingNos + 2*noCrossingNos
        self.minHomGrading = minHomGrading
        self.maxHomGrading = maxHomGrading
        self.minQuantumGrading = minQuantumGrading
        self.maxQuantumGrading = maxQuantumGrading
        powerSetDict = tuple(powerSet(list((i for i in range(m)))) for m in range(2*noCrossingNos + 1))
        setOfUValues = powerSet(list(n for n in range(noCrossingNos))) #locations on the Kauffman cube
        indexToComponentDict = dict({}) #going to be a dictionary that takes a cube position u and outputs a sequencing of components
        componentToIndexDict = dict({})
        gradingsToGeneratorsDict = dict({}) #This dict will take in a quantum grading and homological grading and output the generators
        componentNoDict = dict({})
        hqToSparseMatrixSetup = dict({})
        crossingToComponentsDict = dict({})
        componentToCrossingsDict = dict({})
        
        qSet = set()
        if diagram.componentNo%2 == 1:
            for q in range(minQuantumGrading, maxQuantumGrading + 1):
                if q%2 == 1:
                    qSet.add(q)
        if diagram.componentNo%2 == 0:
            for q in range(minQuantumGrading, maxQuantumGrading + 1):
                if q%2 == 0:
                    qSet.add(q)
        self.qSet = qSet
        for q in qSet:
            for n in range(minHomGrading, maxHomGrading + 1):
                gradingsToGeneratorsDict[(n,q)] = set()
                hqToSparseMatrixSetup[(n,q)] = set()
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
            homGradingU = len(u) - negativeCrossingNo
            for S in powerSetDict[componentNoDict[u]]: #S represents the components that are labeled with x
                qGrading = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (uResolution.componentNo - len(S)) - (len(S))
                gradingsToGeneratorsDict[(homGradingU,qGrading)].add((u,S))
                qGradingDict[(u,S)] = qGrading
        hqToIndexToGenerator = dict({})
        hqToGeneratorToIndex = dict({})
        hqToGeneratorNo = dict({})
        self.crossingToComponentsDict = crossingToComponentsDict
        for q in qSet:
            for n in range(minHomGrading, maxHomGrading + 1):
                generatorTuple = tuple(gradingsToGeneratorsDict[(n, q)])
                hqToGeneratorNo[(n,q)] = len(generatorTuple)
                indexToGenerator = dict({(i, generatorTuple[i]) for i in range(hqToGeneratorNo[(n,q)])})
                generatorToIndex = dict({(generatorTuple[i], i) for i in range(hqToGeneratorNo[(n,q)])})
                hqToIndexToGenerator[(n,q)] = indexToGenerator
                hqToGeneratorToIndex[(n,q)] = generatorToIndex
        self.hqToGeneratorNo = hqToGeneratorNo
        self.hqToIndexToGenerator = hqToIndexToGenerator
        self.hqToGeneratorToIndex = hqToGeneratorToIndex
        self.componentToIndexDict = componentToIndexDict
        self.indexToComponentDict = indexToComponentDict
        #Now is the Khovanov differential part
        for u in setOfUValues:
            homGradingU = len(u) - negativeCrossingNo
            for i in {j for j in range(noCrossingNos)} - u:
                v = u | {i}
                homGradingV = homGradingU + 1
                uSpecialComponents = set(crossingToComponentsDict[u][indexToCrossingNo[i]])
                vSpecialComponents = set(crossingToComponentsDict[v][indexToCrossingNo[i]])
                if componentNoDict[u] < componentNoDict[v]:
                    for uS in powerSetDict[componentNoDict[u]]:
                        uLabeling = {indexToComponentDict[u][s] for s in uS}
                        vLabelingOfOtherComponents = uLabeling - uSpecialComponents
                        qGradingU = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (componentNoDict[u] - len(uS)) - (len(uS))
                        qGradingV = qGradingU
                        jCoordinate = hqToGeneratorToIndex[(homGradingU,qGradingU)][(u,uS)]
                        if min(uSpecialComponents) in uLabeling:
                            generatorComponentForm = vLabelingOfOtherComponents | vSpecialComponents
                            vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                            #qGradingV = positiveCrossingNo - 2 * negativeCrossingNo + len(v) + (componentNoDict[v] - len(vS)) - (len(vS))
                            iCoordinate = hqToGeneratorToIndex[(homGradingV,qGradingV)][(v, vS)]
                            hqToSparseMatrixSetup[(homGradingU, qGradingU)].add((iCoordinate, jCoordinate))
                        else:
                            generatorsComponentForm = (vLabelingOfOtherComponents | {min(vSpecialComponents)}, vLabelingOfOtherComponents | {max(vSpecialComponents)})
                            vS0 = frozenset(componentToIndexDict[v][x] for x in generatorsComponentForm[0])
                            vS1 = frozenset(componentToIndexDict[v][x] for x in generatorsComponentForm[1])
                            iCoordinate0 = hqToGeneratorToIndex[(homGradingV, qGradingV)][(v, vS0)]
                            iCoordinate1 = hqToGeneratorToIndex[(homGradingV, qGradingV)][(v, vS1)]
                            hqToSparseMatrixSetup[(homGradingU, qGradingU)].update(((iCoordinate0, jCoordinate,), (iCoordinate1, jCoordinate)))
                        
                if componentNoDict[u] > componentNoDict[v]:
                    for uS in powerSetDict[componentNoDict[u]]:
                        uLabeling = {indexToComponentDict[u][s] for s in uS}
                        vLabelingOfOtherComponents = uLabeling - uSpecialComponents
                        qGradingU = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (componentNoDict[u] - len(uS)) - (len(uS))
                        qGradingV = qGradingU
                        jCoordinate = hqToGeneratorToIndex[(homGradingU, qGradingU)][(u,uS)]
                        if len(uSpecialComponents & uLabeling) == 1:
                            generatorComponentForm = vLabelingOfOtherComponents | vSpecialComponents
                            vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                            iCoordinate = hqToGeneratorToIndex[(homGradingV, qGradingV)][(v, vS)]
                            hqToSparseMatrixSetup[(homGradingU, qGradingU)].add((iCoordinate,jCoordinate))
                        elif len(uSpecialComponents & uLabeling) == 0:
                            generatorComponentForm = vLabelingOfOtherComponents
                            vS = frozenset(componentToIndexDict[v][x] for x in generatorComponentForm)
                            iCoordinate = hqToGeneratorToIndex[(homGradingV, qGradingV)][(v, vS)]
                            hqToSparseMatrixSetup[(homGradingU, qGradingU)].add((iCoordinate,jCoordinate))
        hqToSparseMatrix = dict()
        for q in qSet:
            for n in range(minHomGrading, maxHomGrading + 1):
                sparseMatrix = F2sparseMatrix(hqToSparseMatrixSetup[(n,q)])
                sparseMatrix.officialColumnRange = (0, hqToGeneratorNo[(n,q)] - 1)
                hqToSparseMatrix[(n,q)] = sparseMatrix
        self.hqToSparseMatrix = hqToSparseMatrix
        self.hqToHomology = dict()

def hqToHomologyLoader(khovanovGenerators, gradings):
    minHomGrading = khovanovGenerators.minHomGrading
    maxHomGrading = khovanovGenerators.maxHomGrading
    qSet = khovanovGenerators.qSet
    if gradings == 'all':
        for q in qSet:
            for n in range(minHomGrading + 1, maxHomGrading + 1):
                khovanovGenerators.hqToHomology[(n,q)] = homology(khovanovGenerators.hqToSparseMatrix[(n,q)], khovanovGenerators.hqToSparseMatrix[(n-1,q)])
    elif isinstance(gradings, set):
        for n,q in gradings:
            if (n,q) not in set(khovanovGenerators.hqToHomology.keys()):
                khovanovGenerators.hqToHomology[(n,q)] = homology(khovanovGenerators.hqToSparseMatrix[(n,q)], khovanovGenerators.hqToSparseMatrix[(n-1,q)])
class flowCategory:
    def __init__(self, morseLink, khovanovGenerators, gradings):
        qGrading = gradings[1]
        bottomHGrading = gradings[0]
        indexToComponentDict = khovanovGenerators.indexToComponentDict
        componentToIndexDict = khovanovGenerators.componentToIndexDict
        crossingToComponentsDict = khovanovGenerators.crossingToComponentsDict
        indexToCrossingNo = morseLink.indexToCrossingNo
        moveTuple = morseLink.moveTuple
        indexToGenerator = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading + 1, qGrading)]
        generatorToIndex = khovanovGenerators.hqToGeneratorToIndex[(bottomHGrading + 1, qGrading)]
        ladybug = 0
        nGeneratorDict = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading, qGrading)]
        nPlusOneGeneratorDict = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading + 1, qGrading)]
        nPlusTwoGeneratorDict = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading + 2, qGrading)]
        self.nGeneratorDict = nGeneratorDict 
        self.nPlusOneGeneratorDict = nPlusOneGeneratorDict
        self.nPlusTwoGeneratorDict = nPlusTwoGeneratorDict
        nMinusOneMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading - 1, qGrading)]
        nMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading, qGrading)]
        nPlusOneMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 1, qGrading)]
        nPlusTwoMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 2, qGrading)]
        pontrjaginThomBoundaries = dict({})
        pontrjaginThoms = dict({})
        boundariesY = dict({})
        yzPositionToYNoDict = dict({})
        pontrjaginThomAdjacency = dict({})
        zToXyPairs = dict({})
        for x in nMatrix.columns:
            for y in nMatrix.entriesInColumn[nMatrix.columnDict[x]]:
                if y in nPlusOneMatrix.columns:
                    for z in nPlusOneMatrix.entriesInColumn[nPlusOneMatrix.columnDict[y]]:
                        yzDifference = min(nPlusTwoGeneratorDict[z][0]-nPlusOneGeneratorDict[y][0])
                        yzPositionToYNoDict[(y,z)] = len(nPlusTwoGeneratorDict[z][0] & set(range(yzDifference)))
                        pontrjaginThomBoundaries[(x,z)] = set()
                        boundariesY[y] = set()
                        zToXyPairs[z] = set()
                        pontrjaginThomAdjacency[z] = dict({})
        self.yzPositionToYNoDict = yzPositionToYNoDict
        for x in nMatrix.columns:
            for y in nMatrix.entriesInColumn[nMatrix.columnDict[x]]:
                if y in nPlusOneMatrix.columns:
                    for z in nPlusOneMatrix.entriesInColumn[nPlusOneMatrix.columnDict[y]]:
                        pontrjaginThomBoundaries[(x,z)].add(y)
                        boundariesY[y].add(x)
                        zToXyPairs[z].add((x,y))
        self.pontrjaginThomBoundaries = pontrjaginThomBoundaries
        for xz in pontrjaginThomBoundaries.keys():
            x = xz[0]
            if len(pontrjaginThomBoundaries[xz]) == 2:
                pontrjaginThoms[xz] = {tuple(pontrjaginThomBoundaries[xz])}
            elif len(pontrjaginThomBoundaries[xz]) == 4:
                ladybug += 1
                fourTuple = tuple(pontrjaginThomBoundaries[xz])
                fourTupleGenerators = tuple(nPlusOneGeneratorDict[fourTuple[i]] for i in range(4))
                ABCrossings = tuple({min(fourTupleGenerators[i][0] - nGeneratorDict[x][0]) for i in range(4)}) #is a tuple that has the crossing 2 indices that get from where x is on the cube to where z is
                #print(ABCrossings)
                crossingAChange = ABCrossings[0]
                crossingBChange = ABCrossings[1]
                zeroAtVAAndVB = nGeneratorDict[x][0]
                oneAtVA = nGeneratorDict[x][0] | {crossingAChange} #The "u" of the (u,uS) paring that is a generator
                oneAtVB = nGeneratorDict[x][0] | {crossingBChange}
                oneAtVAComponents = crossingToComponentsDict[oneAtVA][indexToCrossingNo[crossingAChange]] #if +,left, then right at v1
                oneAtVBComponents = crossingToComponentsDict[oneAtVB][indexToCrossingNo[crossingAChange]] #if +, bottom, then top at v1
                oneAtVAComponentIndices = (componentToIndexDict[oneAtVA][oneAtVAComponents[0]], componentToIndexDict[oneAtVA][oneAtVAComponents[1]])
                oneAtVBComponentIndices = (componentToIndexDict[oneAtVB][oneAtVBComponents[0]], componentToIndexDict[oneAtVB][oneAtVBComponents[1]]) 
                u = nGeneratorDict[x][0]
                uS = nGeneratorDict[x][1]
                uLabeling = {indexToComponentDict[u][s] for s in uS} #set of positions of components labeled 'x'
                labelingWithoutLadybug = nGeneratorDict[x][1]
                #Because in a ladybug matching, the ladybug component at the 00 resoultion is always labeled with a 1 
                labelingWithoutLadybugComponentForm = frozenset({indexToComponentDict[u][i] for i in labelingWithoutLadybug})
                #positions in diagram of components of diagram labeled 'x'. Note that the ladybug isn't labeled 'x' in the first place or else it wouldn't be a ladybug matching. So no need to exclude the ladybug
                labelingWithoutLadybugIndexForm1A0B = frozenset({componentToIndexDict[oneAtVA][s] for s in labelingWithoutLadybugComponentForm})
                #indices of components labeled 'x' in the diagram where the 'A' vertex is resolved, with the ladybug components not included
                labelingWithoutLadybugIndexForm0A1B = frozenset({componentToIndexDict[oneAtVB][s] for s in labelingWithoutLadybugComponentForm})
                #indices of components labeled 'x' in the diagram where the 'B' vertex is resolved, with the ladybug components not included
                labeling1A0BIndexForm = (labelingWithoutLadybugIndexForm1A0B | frozenset({oneAtVAComponentIndices[0]}), labelingWithoutLadybugIndexForm1A0B | frozenset({oneAtVAComponentIndices[1]})) #labeling for when V1 is 0 and V2 is 1
                #A pair where each is an intermediate diagram. In the first, the bottom (or left) circle to the 'A' crossing is labeled 'x' and in the second, the top (or right) circle to the 'A' crossing is lableled 'x'
                labeling0A1BIndexForm = (labelingWithoutLadybugIndexForm0A1B | frozenset({oneAtVBComponentIndices[0]}), labelingWithoutLadybugIndexForm0A1B | frozenset({oneAtVBComponentIndices[1]}))
                #Similar to the above
                if moveTuple[indexToCrossingNo[crossingAChange]][1] == '+':
                    #0-resolution at vertex1 looks like cup and cap
                    pair1 = (generatorToIndex[(oneAtVA,labeling1A0BIndexForm[0])],generatorToIndex[(oneAtVB,labeling0A1BIndexForm[0])])
                    pair2 = (generatorToIndex[(oneAtVA,labeling1A0BIndexForm[1])],generatorToIndex[(oneAtVB,labeling0A1BIndexForm[1])])
                    
                elif moveTuple[indexToCrossingNo[crossingAChange]][1] == '-':
                    #0-resoultion at vertex1 looks like a continuation
                    pair1 = (generatorToIndex[(oneAtVA,labeling1A0BIndexForm[0])],generatorToIndex[(oneAtVB,labeling0A1BIndexForm[1])])
                    pair2 = (generatorToIndex[(oneAtVA,labeling1A0BIndexForm[1])],generatorToIndex[(oneAtVB,labeling0A1BIndexForm[0])])
                else:
                    raise ValueError('crossings!')
                pontrjaginThoms[xz] = {pair1, pair2}
                #print(pontrjaginThoms[xz])
                
            else: print('Error!')
        self.pontrjaginThoms = pontrjaginThoms
        self.boundariesY = boundariesY
        self.zToXyPairs = zToXyPairs
        #print('zToXyPairs:', zToXyPairs)
        for xz in pontrjaginThoms.keys():
            for yPair in pontrjaginThoms[xz]:
                pontrjaginThomAdjacency[xz[1]][(xz[0], yPair[0])] = (xz[0], yPair[1])
                pontrjaginThomAdjacency[xz[1]][(xz[0], yPair[1])] = (xz[0], yPair[0])
        self.pontrjaginThomAdjacency = pontrjaginThomAdjacency
        #print(pontrjaginThomAdjacency[1][(3,4)])
        #print('ladybugNumbers:', ladybug)

def Sq1(khovanovGenerators, gradings, kernel):
    qGrading = gradings[1]
    bottomHGrading = gradings[0]
    nMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading, qGrading)]
    nIndexToGenerator = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading, qGrading)]
    nPlus1IndexToGenerator = khovanovGenerators.hqToIndexToGenerator[(bottomHGrading + 1, qGrading)]
    minusSignMatrixSet = set()
    plusSignMatrixSet = set()
    for ij in nMatrix.sparseMatrix:
        i = ij[0]
        j = ij[1]
        u = nIndexToGenerator[j][0]
        v = nPlus1IndexToGenerator[i][0]
        differencePoint = min(v-u)
        uvSign = len(set(u) & set(range(differencePoint))) % 2
        if uvSign == 1:
            minusSignMatrixSet.add(ij)
        if uvSign == 0:
            plusSignMatrixSet.add(ij)
    minusSignMatrix = F2sparseMatrix(minusSignMatrixSet)
    plusSignMatrix = F2sparseMatrix(plusSignMatrixSet)
    #print(minusSignMatrix+plusSignMatrix+nMatrix)
    output = set()
    for i in nMatrix.rows:
        if i in minusSignMatrix.rows:
            minusMatrixDotProduct = len(minusSignMatrix.entriesInRow[minusSignMatrix.rowDict[i]] & kernel) % 4
        else:
            minusMatrixDotProduct = 0
        if i in plusSignMatrix.rows:
            plusMatrixDotProduct = len(plusSignMatrix.entriesInRow[plusSignMatrix.rowDict[i]] & kernel) % 4
        else:
            plusMatrixDotProduct = 0
        #print(minusMatrixDotProduct + plusMatrixDotProduct)
        #print(plusMatrixDotProduct - minusMatrixDotProduct)
        if (plusMatrixDotProduct - minusMatrixDotProduct) % 4 == 2:
            output.add(i)
        elif (plusMatrixDotProduct - minusMatrixDotProduct) % 2 == 1:
            raise ValueError('Bockstein not working!')
    return output
    
class matchings:
    def __init__(self, flowCategory, kernel):
        pontrjaginThomBoundaries = flowCategory.pontrjaginThomBoundaries
        pontrjaginThoms = flowCategory.pontrjaginThoms
        boundariesY = flowCategory.boundariesY
        activeBoundariesY = dict({})
        boundaryMatchingAdjacency = dict({})
        zToActiveXyPairs = dict({})
        for z in flowCategory.zToXyPairs.keys():
            zToActiveXyPairs[z] = set()
            for xy in flowCategory.zToXyPairs[z]:
                if xy[0] in kernel:
                    zToActiveXyPairs[z].add(xy)
        self.zToActiveXyPairs = zToActiveXyPairs
        #print('zToActiveXyPairs:', zToActiveXyPairs)
        for y in boundariesY.keys():
            if (boundariesY[y] & kernel != set()):
                activeBoundariesY[y] = boundariesY[y] & kernel
                #print(activeBoundariesY[y])
        #print(activeBoundaries)
        boundaryMatchings = dict({})
        for y in activeBoundariesY.keys():
            yBoundaryTuple = tuple(activeBoundariesY[y])
            #print(yBoundaryTuple)
            yBoundaryNo = len(yBoundaryTuple)
            halfNo = yBoundaryNo // 2
            subTuple1 = tuple(yBoundaryTuple[n] for n in range(halfNo))
            subTuple2 = tuple(yBoundaryTuple[n] for n in range(halfNo, yBoundaryNo))
            boundaryMatchings[y] = {(subTuple1[i], subTuple2[i]) for i in range(halfNo)}
        self.boundaryMatchings = boundaryMatchings
        for y in boundaryMatchings.keys():
            for xPair in boundaryMatchings[y]:
                boundaryMatchingAdjacency[(xPair[0],y)] = (xPair[1],y)
                boundaryMatchingAdjacency[(xPair[1],y)] = (xPair[0],y)
        self.boundaryMatchingAdjacency = boundaryMatchingAdjacency
        #print('boundarymatchings:', boundaryMatchings)
        #print(self.boundaryMatchings)

def zCoefficient(flowCategory, matchings, z):
    #zActivePontrjaginThoms = set()
    #zBoundaryMatchings = set()
    yzPositionToYNoDict = flowCategory.yzPositionToYNoDict
    pontrjaginThomAdjacency = flowCategory.pontrjaginThomAdjacency
    boundaryAdjacencies = matchings.boundaryMatchingAdjacency
    #print('activeXyPairs:', matchings.zToActiveXyPairs)
    xyPairs = matchings.zToActiveXyPairs[z]
    leftOverXyPairList = list(xyPairs)
    
    cycleSet = set()
    while leftOverXyPairList != []:
        boundaryAdjacency1 = leftOverXyPairList[0]
        boundaryAdjacency2 = boundaryAdjacencies[boundaryAdjacency1]
        leftOverXyPairList.remove(boundaryAdjacency1)
        leftOverXyPairList.remove(boundaryAdjacency2)
        cycleToAdd = [(boundaryAdjacency1,boundaryAdjacency2)]
        x = pontrjaginThomAdjacency[z][boundaryAdjacency2]
        while pontrjaginThomAdjacency[z][boundaryAdjacency2] != (cycleToAdd[0][0]):
            boundaryAdjacency1 = pontrjaginThomAdjacency[z][boundaryAdjacency2]
            boundaryAdjacency2 = boundaryAdjacencies[boundaryAdjacency1]
            cycleToAdd.append((boundaryAdjacency1,boundaryAdjacency2))
            leftOverXyPairList.remove(boundaryAdjacency1)
            leftOverXyPairList.remove(boundaryAdjacency2)
        cycleSet.add(tuple(cycleToAdd))

    Z2Element = 0
    for K in cycleSet:
        #print('K:', K)
        c = tuple(yzPositionToYNoDict[(K[i][0][1], z)] for i in range(len(K)))
        #print('c:', c)
        cLength = len(c)
        KElement = 0
        switchBackNo = 0
        for i in range(cLength): #Adds the products of adjacencies
            KElement += (c[i%cLength] * c[(i+1)%cLength])
            KElement += c[i]#Adds each vertex
            triple = (c[i], c[(i+1)%cLength], c[(i+2)%cLength])
            #Adds the middle of each triple that has the middle of the triple being the middle value
            if sorted(triple)[1] == triple[1]:
                KElement += triple[1]
            KElement += sorted(triple)[1]#Adds the middle of the value set of  each triple
            if sorted(triple)[1] != triple[1]:#Counts the number of times the path turns around (should be even)
                switchBackNo +=  1
            if triple[0] == triple[2]:
                if triple[1] < triple[0]:
                    KElement += 1
                elif triple[1] > triple[2]:
                    KElement += 0
            elif sorted(triple)[1] == triple[0]:
                KElement += 1
            if c[i] == c[(i+2)%cLength]:
                #print('hello')
                middleBoundaryArc = K[(i+1)%cLength]
                if (middleBoundaryArc[0][0], middleBoundaryArc[1][0]) not in matchings.boundaryMatchings[middleBoundaryArc[0][1]]:
                    #print(i, 'reversed')
                    KElement += 1
                elif (middleBoundaryArc[0][0], middleBoundaryArc[1][0]) in matchings.boundaryMatchings[middleBoundaryArc[0][1]]:
                    KElement += 0
                else:
                    print('help!')
        #print(switchBackNo)
        KElement += (switchBackNo // 2) #Adds half the number of times the path turns around
        KElement += 1 #adds 1 at the end
        #print('KElement:', KElement % 2)
        Z2Element += KElement
        #print('Z2Element:', Z2Element%2)
    return Z2Element%2

def Sq2(flowCategory, kernel):
    boundaryMatchings = matchings(flowCategory, kernel)
    Sq2Set = set({})
    for z in boundaryMatchings.zToActiveXyPairs.keys():
        #print('zValue:', z, '.')
        #print(matchings.zToActiveXyPairs[z])
        if zCoefficient(flowCategory, boundaryMatchings, z) == 1:
            Sq2Set.add(z)
    return Sq2Set

def Sq1Matrix(khovanovGenerators, gradings):
    bottomHGrading = gradings[0]
    qGrading = gradings[1]
    nMinus1Matrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading - 1, qGrading)]
    nMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading, qGrading)]
    nPlus1Matrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 1, qGrading)]
    hqToHomologyLoader(khovanovGenerators, {(bottomHGrading, qGrading), (bottomHGrading + 1, qGrading)})

    nHomology = khovanovGenerators.hqToHomology[(bottomHGrading, qGrading)]
    nPlus1Homology = khovanovGenerators.hqToHomology[(bottomHGrading + 1, qGrading)]
    B_N = image(nMatrix)
    nHomologyDim = len(nHomology.sortedPivots)
    Sq1SparseMatrix = set()
    for j in range(nHomologyDim):
        inputElement = nHomology.orderedSparseEchelonSet[j]
        outputElement = Sq1(khovanovGenerators, gradings, inputElement)
        column = homologyProjection(nPlus1Homology, B_N, outputElement)
        for i in column:
            Sq1SparseMatrix.add((i,j))
    Sq1SparseMatrix = F2sparseMatrix(Sq1SparseMatrix)
    Sq1SparseMatrix.officialColumnRange = (0,nHomologyDim - 1)
    return Sq1SparseMatrix

def Sq2Matrix(khovanovGenerators, flowCategory, gradings):
    bottomHGrading = gradings[0]
    qGrading = gradings[1]
    nMinus1Matrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading - 1, qGrading)]
    nMatrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading, qGrading)]
    nPlus1Matrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 1, qGrading)]
    nPlus2Matrix = khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 2, qGrading)]
    hqToHomologyLoader(khovanovGenerators, {(bottomHGrading, qGrading), (bottomHGrading + 2, qGrading)})
    nHomology = khovanovGenerators.hqToHomology[(bottomHGrading, qGrading)]
    nPlus2Homology = khovanovGenerators.hqToHomology[(bottomHGrading + 2, qGrading)]
    B_NPlus2 = image(nPlus1Matrix)
    nHomologyDim = len(nHomology.sortedPivots)
    Sq2SparseMatrix = set()
    for j in range(nHomologyDim):
        inputElement = nHomology.orderedSparseEchelonSet[j]
        outputElement = Sq2(flowCategory, inputElement)
        column = homologyProjection(nPlus2Homology, B_NPlus2, outputElement)
        for i in column:
            Sq2SparseMatrix.add((i,j))
    Sq2SparseMatrix = F2sparseMatrix(Sq2SparseMatrix)
    Sq2SparseMatrix.officialColumnRange = (0, nHomologyDim - 1)
    return Sq2SparseMatrix

def St(flowCategory, khovanovGenerators, gradings):
    bottomHGrading = gradings[0]
    qGrading = gradings[1]
    if khovanovGenerators.hqToSparseMatrix[gradings].sparseMatrix == set() or khovanovGenerators.hqToSparseMatrix[(bottomHGrading + 2, qGrading)].sparseMatrix == set():
        return (0,0,0,0)
    #print(1)
    matrixSq2 = Sq2Matrix(khovanovGenerators, flowCategory, gradings)
    #print(2)
    matrixSq1iGrading = Sq1Matrix(khovanovGenerators, gradings)
    #print(3)
    matrixSq1iPlus1Grading = Sq1Matrix(khovanovGenerators,(bottomHGrading + 1, qGrading))
    #print(4)
    kernelMatrixSq1iGrading = kernel(matrixSq1iGrading)
    #print(5)    
    Sq2RestrictedToKernelColumns = {frozenset(matrixSq2 * v) for v in kernelMatrixSq1iGrading.sparseEchelonSet}
    r1 = rank(matrixSq2)
    Sq2RestrictedToKernelImage = reduceRowSparse(Sq2RestrictedToKernelColumns)
    Sq2RestrictedToKernelRank = len(Sq2RestrictedToKernelImage.pivots)
    r2 = Sq2RestrictedToKernelRank
    r3 = intersectionDim(image(matrixSq2),image(matrixSq1iPlus1Grading))
    r4 = intersectionDim(image(matrixSq1iPlus1Grading),Sq2RestrictedToKernelImage)
    return (r2-r4,r1-r2-r3+r4,r4,r3-r4)

def StList(diagram, homologies):
    if homologies == set():
        return tuple()
    else:
        khovanovGenerators = khovanovBasis(diagram)
        hValues = range(khovanovGenerators.minHomGrading + 1, khovanovGenerators.maxHomGrading - 2 + 1)
        #print(hValues)
        qSet = khovanovGenerators.qSet
        #print(qSet)
        print('done with Khovanov Generators')
        if isinstance(homologies, set):
            l = []
            homologiesPlusMirrorHomologies = set()
            for n,q in homologies:
                if n in hValues and q in qSet:
                    homologiesPlusMirrorHomologies.add((n,q))
                if -n-2 in hValues and -q in qSet:
                    homologiesPlusMirrorHomologies.add((-n-2,-q))
            for n,q in homologiesPlusMirrorHomologies:
                hqFlowCategory = flowCategory(diagram, khovanovGenerators, (n,q))
                StOutput = St(hqFlowCategory, khovanovGenerators, (n,q))
                if StOutput != (0,0,0,0):
                    l.append(((n,q), StOutput))
        elif homologies == 'all':
            l = []
            for n in hValues:
                for q in qSet:
                    hqToHomologyLoader(khovanovGenerators, {(n,q)})
            for n in hValues:
                for q in qSet:
                    hqFlowCategory = flowCategory(diagram, khovanovGenerators, (n,q))
                    StOutput = St(hqFlowCategory, khovanovGenerators, (n,q))
                    if StOutput != (0,0,0,0):
                        l.append(((n,q), StOutput))
    return tuple(l)
        
    

linkL6n1Dict = (((1,4),0), ((6,5), 0), ((2,3), 0), ((4,5),'-'), ((1,2),'+'), ((3,4),'+'), ((2,3),'+'), ((1,2),'-'), ((3,4),'-'), ((2,3),1), ((4,5),1), ((1,6),1))
knot10_124Dict = (((1,2), 0), ((3,8),0), ((2,3), '-'), ((4,5), 0), ((6,7), 0), ((5,6), '-'), ((7,8), '+'), ((4,5), '+'), ((7,8), '+'), ((4,5), '+'), ((6,7), '+'), ((4,5), '+'), ((6,7), '+'), ((3,4), '-'), ((4,5), 1), ((3,6), 1), ((2,7), 1), ((1,8), 1))
knot10_124CrossingTuple = (0, 10)
knot10_132Dict = (((1,4), 0), ((5,8), 0), ((2,3), 0), ((4,5), '-'), ((6,7), 0), ((3,4), '-'), ((7,8), '+'), ((4,5), '+'), ((7,8), '+'), ((4,5), '+'), ((4,5), '+'), ((5,6), '-'), ((5,6), '-'), ((4,5), 1), ((3,6), '-'), ((2,3), 1), ((6,7), 1), ((1,8), 1))
knot10_132CrossingTuple = (7,3)
#pretzelKnotDict = (((1,2),0), ((3,8), 0), ((2,3), '-'), ((4,5), 0), ((6,7), 0), ((5,6), '-'), ((7,8), '+'), ((4,5), '+'), ((7,8), '+'), ((3,4), '-'), ((6,7), '+'), ((4,5), 1), ((6,7), '+'), ((3,6), 1), ((2,7), 1), ((1,8), 1))
#pretzelCrossingTuple = (0,8)
knot11_n6Dict = (((1, 12), 0), ((13, 14), 0), ((12, 13), "+"), ((7, 2), 0), ((1, 2), "-"), ((1, 2), "-"), ((3, 6), 0), ((2, 3), "+"), ((8, 9), 0), ((7, 8), "-"), ((6, 7), "+"), ((7, 8), 1), ((5, 4), 0), ((3, 4), "+"), ((4, 5), "-"), ((5, 6), 1), ((11, 10), 0), ((9, 10), "+"), ((11, 12), "+"), ((9, 10), "+"), ((9, 4), 1), ((10, 11), 1), ((3, 12), 1), ((13, 2), 1), ((14, 1), 1))
conwayKnotDict = (((5,10), 0), ((1,4), 0), ((2,3), 0), ((4,5), '-'), ((6,7), 0), ((8,9), 0), ((3,4), '+'), ((5,6), '-'), ((7,8), '-'), ((9,10), '+'), ((2,3), '-'), ((4,5), '+'), ((6,7), '+'), ((9,10), '+'), ((3,4), '-'), ((5,6), 1), ((3,4), '-'), ((4,7), 1), ((3,8), 1), ((2,9), 1), ((1,10), 1))


#linkDict = knot8_10Dict
#linkMorseLink = morseLink(linkDict)
#print('componentNo:', linkMorseLink.componentNo)
#link = khovanovBasis(linkMorseLink)
#print(knot.hqToSparseMatrix)
#Q = -3

#mh = link.hqToSparseMatrix[(-8,Q)]
#mg = link.hqToSparseMatrix[(-7,Q)]
#mf = link.hqToSparseMatrix[(-6,Q)]
#me = link.hqToSparseMatrix[(-5,Q)]
#md = link.hqToSparseMatrix[(-4,Q)]
#mc = link.hqToSparseMatrix[(-3,Q)]
#mb = link.hqToSparseMatrix[(-2,Q)]
#ma = link.hqToSparseMatrix[(-1, Q)]
#a = link.hqToSparseMatrix[(0, Q)]
#b = link.hqToSparseMatrix[(1, Q)]
#c = link.hqToSparseMatrix[(2, Q)]
#d = link.hqToSparseMatrix[(3, Q)]
#e = link.hqToSparseMatrix[(4, Q)]
#f = link.hqToSparseMatrix[(5, Q)]
#g = link.hqToSparseMatrix[(6, Q)]
#h = link.hqToSparseMatrix[(7, Q)]
#i = link.hqToSparseMatrix[(8, Q)]
#j = link.hqToSparseMatrix[(9, Q)]

#print(a)
#print(b)
#print(kernel(b))
#print(image(a))
#print(b*a)
#print(a)
#print(b)
#print(c)
#print(d)
#print(e)
#print(b*a)
#print(c*b)
#print(d*c)
#print(e*d)

"""
print('-7Homology:', homology(mg,mh))
print('-6Homology:', homology(mf,mg))
print('-5Homology:', homology(me,mf))
print('-4Homology:', homology(md,me))
print('-3Homology:', homology(mc,md))
print('-2Homology:', homology(mb,mc))
print('-1Homology:', homology(ma,mb))
print('0Homology:', homology(a,ma))
print('1Homology:', homology(b,a))
print('2Homology:', homology(c,b))
print('3Homology:', homology(d,c))
print('4Homology:', homology(e,d))
print('5Homology:', homology(f,e))
print('6Homology:', homology(g,f))
print('7Homology:', homology(h,g))
print('8Homology:', homology(i,h))
print('9Homology:', homology(j,i))
"""

#fC = flowCategory(linkMorseLink, link, (3, 11))
#print('done creating flow category')
#kernelElement = set({0})
#bM = matchings(fC, kernelElement)
#print(bM.boundaryMatchings)
#print(zCoefficient(fC,bM,0))
#square = Sq2(fC, kernelElement)
#kernel1 = {769, 514, 771, 516, 517, 518, 775, 522, 780, 526, 529, 530, 786, 789, 790, 534, 535, 537, 538, 791, 540, 541, 794, 799, 544, 800, 546, 549, 807, 552, 554, 559, 563, 567, 312, 570, 572, 573, 581, 584, 329, 333, 589, 590, 592, 339, 598, 599, 602, 348, 605, 610, 611, 357, 360, 616, 617, 618, 366, 369, 627, 629, 632, 386, 642, 643, 647, 394, 395, 656, 405, 665, 666, 413, 669, 670, 675, 420, 676, 677, 680, 425, 426, 683, 431, 688, 433, 434, 689, 439, 184, 443, 446, 447, 449, 707, 709, 711, 714, 463, 464, 719, 466, 467, 468, 723, 726, 730, 732, 222, 478, 735, 481, 736, 483, 486, 742, 743, 745, 234, 492, 748, 496, 752, 753, 501, 761, 763, 765, 511}
#kernel2 = {768, 771, 774, 776, 783, 784, 785, 798, 542, 802, 807, 809, 810, 811, 820, 823, 827, 830, 834, 580, 836, 839, 843, 846, 593, 597, 598, 604, 608, 613, 614, 616, 617, 619, 629, 634, 635, 645, 654, 658, 660, 663, 665, 674, 676, 677, 679, 685, 686, 690, 691, 692, 694, 696, 699, 701, 709, 712, 714, 715, 719, 722, 724, 735, 736, 739, 746, 749, 751, 758, 761, 766}
#print(mb * kernel1)
#square1 = Sq2(fC, kernel1)
#square2 = Sq2(fC, kernel2)
#print('Square:', square1)
#print(square2)
#square1Plus2 = Sq2(fC, kernel1 ^ kernel2)
#square1PlusSquare2 = Sq2(fC, kernel1) ^ Sq2(fC, kernel2)
#print(square1Plus2)
#print(square1PlusSquare2)
#print(e * square1)
#print(f * square2)
#print(image(e))
#print(square1Plus2 ^ square1PlusSquare2)
#square1 = Sq1(link, (-2,-3), {0, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 26})
#print('square1:', square1)
#print(ma * square1)
#matrix = Sq2Matrix(link, fC, (3,9))
#matrixOne = Sq1Matrix(link, (-3,-13))
#print(matrixOne)
#print('image:', image(ma))
#print('kernel:', kernel(a))
#print(len(image(ma).pivots))
#print(len(kernel(a).pivots))
#print(matrix)
#print(St(fC, link, (3, 11)))
#print(StList(linkMorseLink, 'all'))

#print('Square:', square)

#print(e * square)
