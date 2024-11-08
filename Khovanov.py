from itertools import chain, combinations

class F2sparseMatrix:
  def __init__(self, data):
    self.sparseMatrix={(x[0],x[1]) for x in data}#set of tuples
    self.rows = {x[0] for x in self.sparseMatrix}
    self.rowNo = len(self.rows)
    self.rowTuple = tuple(self.rows)
    rowRowNumber = {(self.rowTuple[n],n) for n in range(len(self.rowTuple))}
    self.rowDict = dict(rowRowNumber)
    entriesInRow = [set() for i in range(self.rowNo)]
    for x in self.sparseMatrix:
      entriesInRow[self.rowDict[x[0]]].add(x[1])
    self.entriesInRow = tuple(frozenset(entriesInRow[i]) for i in range(self.rowNo))
    
    self.columns = {x[1] for x in self.sparseMatrix}
    self.columnNo = len(self.columns)
    self.columnTuple = tuple(self.columns)
    columnColumnNumber = {(self.columnTuple[n],n) for n in range(len(self.columnTuple))}
    self.columnDict = dict(columnColumnNumber)
    entriesInColumn = [set() for i in range(self.columnNo)]
    for x in self.sparseMatrix:
      entriesInColumn[self.columnDict[x[1]]].add(x[0])
    self.entriesInColumn = tuple(frozenset(entriesInColumn[i]) for i in range(self.columnNo))
  def __repr__(self):
    return "F2sparseMatrix(%s)" %self.sparseMatrix
  def __add__(self,x):
    return F2sparseMatrix(self.sparseMatrix ^ x.sparseMatrix)
  def __radd__(self,x):
    return F2sparseMatrix(self.sparseMatrix ^ x.sparseMatrix)
  def __getitem__(self,i):
    return self.sparseMatrix[i]
  def __setitem__(self,i,x):
    self.sparseMatrix[i]=x
  def __mul__(self,x):
    multSparseMatrix = set()
    for i in range(self.rowNo):
      for j in range(x.columnNo):
        if len(self.entriesInRow[i] & x.entriesInColumn[j])%2 == 1:
          multSparseMatrix.add((self.rowTuple[i],x.columnTuple[j]))
    return F2sparseMatrix(multSparseMatrix)
  def __getitem__(self,index):
    if index in self.sparseMatrix:
      return 1
    else:
      return 0
  def __setitem__(self,index,x):
    if ((index[0],index[1]) in self.sparseMatrix and x==0):
      self.sparseMatrix.remove((index[0],index[1]))
    if ((index[0],index[1]) not in self.sparseMatrix and x == 1):
      self.sparseMatrix.add((index[0],index[1]))
    self.rows = {x[0] for x in self.sparseMatrix}
    self.rowNo = len(self.rows)
    self.rowTuple = tuple(self.rows)
    rowRowNumber = {(self.rowTuple[n],n) for n in range(len(self.rowTuple))}
    self.rowDict = dict(rowRowNumber)
    entriesInRow = [set() for i in range(self.rowNo)]
    for x in self.sparseMatrix:
      entriesInRow[self.rowDict[x[0]]].add(x[1])
    self.entriesInRow = tuple(frozenset(entriesInRow[i]) for i in range(self.rowNo))
    
    self.columns = {x[1] for x in self.sparseMatrix}
    self.columnNo = len(self.columns)
    self.columnTuple = tuple(self.columns)
    columnColumnNumber = {(self.columnTuple[n],n) for n in range(len(self.columnTuple))}
    self.columnDict = dict(columnColumnNumber)
    entriesInColumn = [set() for i in range(self.columnNo)]
    for x in self.sparseMatrix:
      entriesInColumn[self.columnDict[x[1]]].add(x[0])
    self.entriesInColumn = tuple(frozenset(entriesInColumn[i]) for i in range(self.columnNo))

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
        print(crossingToComponentsDict)
        
        
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
                moveList[indexToCrossingNo[n]][1] = (activeTuple, 'stay')
            else:
                moveList[indexToCrossingNo[n]][1] = (activeTuple, '10')
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
        componentDict = dict({}) #going to be a dictionary that takes a cube position u and outputs a sequencing of components
        gradingsToGeneratorsDict = dict({}) #This dict will take in a quantum grading and homological grading and output the generators
        componentNoDict = dict({})
        qnToSparseMatrixSetup = dict({})
        crossingToComponentsDict = dict({})
        componentToCrossingsDict = dict({})
        for q in range(minQuantumGrading, maxQuantumGrading + 1):
            for n in range(noCrossingNos + 1):
                gradingsToGeneratorsDict[(q,n)] = set()
                qnToSparseMatrixSetup[(q,n)] = set()
        
        for u in setOfUValues:
            uResolution = resolution(diagram, u)
            crossingToComponentsDict[u] = uResolution.crossingToComponentsDict
            componentNoDict[u] = uResolution.componentNo
            componentTuple = tuple(uResolution.components)
            componentDict[u] = dict({(k, componentTuple[k]) for k in range(uResolution.componentNo)})
        #print(componentDict)
        qGradingDict = dict({})
        for u in setOfUValues:
            homGrading = len(u)
            for S in powerSetDict[componentNoDict[u]]: #S represents the components that are labeled with x
                qGrading = positiveCrossingNo - 2 * negativeCrossingNo + len(u) + (uResolution.componentNo - len(S)) - (len(S))
                gradingsToGeneratorsDict[(qGrading, homGrading)].add((u,S))
                qGradingDict[(u,S)] = qGrading
        qhToIndexToGenerator = dict({})
        qhToGeneratorToIndex = dict({})
        qhToGeneratorNo = dict({})
        for q in range(minQuantumGrading, maxQuantumGrading + 1):
            for n in range(noCrossingNos + 1):
                generatorTuple = tuple(gradingsToGeneratorsDict[(q,n)])
                qhToGeneratorNo[(q,n)] = len(generatorTuple)
                indexToGenerator = dict({(i, generatorTuple[i]) for i in range(qhToGeneratorNo[(q,n)])})
                generatorToIndex = dict({(generatorTuple[i], i) for i in range(qhToGeneratorNo[(q,n)])})
                qhToIndexToGenerator[(q,n)] = indexToGenerator
                qhToGeneratorToIndex[(q,n)] = generatorToIndex
                
        for u in setOfUValues:
          for i in {j for j in range(noCrossingNos)} - u:
            v = u | {i}
            uSpecialComponents = crossingToComponentsDict[u][indexToCrossingNo[i]]
            vSpecialComponents = crossingToComponentsDict[v][indexToCrossingNo[i]]
            if componentNoDict[u] < componentNoDict[v]:
              for S in powerSetDict[componentNoDict[u]]:
                uLabeling = {componentDict[u][s] for s in S}
                #if min(uSpecialComponents )
                #xComponentsU = frozenset(crossingToComponentsDict[u][i] for i in S)
                #if min(uSpecialComponents) in 
                generator1 = 1
                generator2 = 1
            if componentNoDict[u] > componentNoDict[v]:
              for S in powerSetDict[componentNoDict[u]]:
                generator1 = 1
        #for q in range(minQuantumGrading, maxQuantumGrading + 1):
        #    for n in range(noCrossingNos + 1):
        #        qnSparseMatrix = set()
        #        for i in range(qhToGeneratorNo[(q,n)]):
        #          generator = 1# qhToIndexToGenerator[(q,n)][i]
        #        sparseMatrixSetup[(q,n)] = qnSparseMatrix
                            
            


knotDict = dict({(1, ((1,2), 0)), (2, ((1,2), 'x', 'lower')), (3, ((1,2), 'x', 'lower')), (4, ((1,2), 1))})
knot = morseLink(knotDict,1,1)
knotRes = resolution(knot, {1})
print(knotRes.components)
print(knotRes.crossingToComponentsDict)
x = khovanovBasis(knot)

#loopyknotDict = dict({(1,((1,2), 0)), (2,((3,4), 0)), (3, ((2,3), 1)), (4, ((1,4), 'x', 'lower')), (5, ((1,4), 'x', 'lower')), (6, ((1,4), 1))})
#loopyKnot = morseLink(loopyknotDict,1,1)
#loopyKnotRes = resolution(loopyKnot, {0})
#print(loopyKnotRes.moveList)
#print(loopyKnotRes.components)
#print(loopyKnotRes.crossingToComponentsDict)
