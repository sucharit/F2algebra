class morseLink:
    def __init__(self, data):
        moveList = dict({(moveNo, data[moveNo]) for moveNo in data.keys()})
        self.moveList = moveList
        moveTurnSet = {n for n in moveList.keys()}
        crossingNos = set()
        for n in moveTurnSet:
            if moveList[n][1] == 'x':
                crossingNos.add(n)
        indexToCrossingNo = list(crossingNos)
        indexToCrossingNo.sort()
        noCrossingNos = len(indexToCrossingNo)
        self.moveTurnSet = moveTurnSet
        self.indexToCrossingNo = indexToCrossingNo
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
        components = set()
        runningDict = dict({})
        crossingToComponentsDict = dict({})
        for n in range(moveNo):
            activeHeight = activeHeights[n]
            activeTuple = self.moveList[activeHeight][0]
            activeMove = self.moveList[activeHeight][1]
            if activeMove == 0:
                components.add(frozenset({activeHeight}))
                for i in activeTuple:
                    runningDict[i] = activeHeight
            if activeMove == 1:
                setToBeAdded = frozenset()
                setsToBeRemoved = frozenset()
                for i in activeTuple:
                    curveComponentNo = runningDict[i]
                    for x in components:
                        if curveComponentNo in x:
                            setToBeAdded = setToBeAdded | x
                            setsToBeRemoved = setsToBeRemoved | frozenset({x})
                    components = components - setsToBeRemoved | frozenset({setToBeAdded})
            if activeMove == 'stay':
                crossingToComponentsDict[activeHeight] = (runningDict[activeTuple[0]], runningDict[activeTuple[1]])
                
            if activeMove == '10':
                
                setToBeAdded = frozenset()
                setsToBeRemoved = frozenset()
                for i in activeTuple:
                    curveComponentNo = runningDict[i]
                    for x in components:
                        if curveComponentNo in x:
                            setToBeAdded = setToBeAdded | x
                            setsToBeRemoved = setsToBeRemoved | frozenset({x})
                    components = components - setsToBeRemoved | frozenset({setToBeAdded})
                dictEntry1 = runningDict[activeTuple[0]]
                #ends the capping off part, starts the cup part
                components.add(frozenset({activeHeight}))
                for i in activeTuple:
                    runningDict[i] = activeHeight
                crossingToComponentsDict[activeHeight] = (dictEntry1, activeHeight)
            #print(components)
                
        self.components = components
        for n in crossingToComponentsDict.keys():
            componentSet = set()
            for x in self.components:
                if crossingToComponentsDict[n][0] in x or crossingToComponentsDict[n][1] in x:
                    componentSet.add(x)
            crossingToComponentsDict[n] = componentSet
        self.crossingToComponentsDict = crossingToComponentsDict
        
        
def resolution(x, u):
    moveList = x.moveList
    noCrossingNos = x.noCrossingNos
    indexToCrossingNo = x.indexToCrossingNo
    for n in range(noCrossingNos):
        activeTuple = moveList[indexToCrossingNo[n]][0]
        if moveList[indexToCrossingNo[n]][2] == 'lower':
            if u[n] == 0:
                moveList[indexToCrossingNo[n]] = (activeTuple, 'stay')
            if u[n] == 1:
                moveList[indexToCrossingNo[n]] = (activeTuple, '10')
        elif moveList[indexToCrossingNo[n]][2] == 'upper':
            if u[n] == 0:
                moveList[indexToCrossingNo[n]][1] = (activeTuple, '10')
            if u[n] == 1:
                moveList[indexToCrossingNo[n]][1] = (activeTuple, 'stay')
    return resolvedMorseLink(moveList)
    
 
#blobDict = dict({(1, ((1,2), 0)), (2, ((3,4), 0)), (3, ((5,6), 0)), (4, ((2,3), 1)), (5, ((1,4), 1)), (6, ((5,6), 1))})
#blobs = resolvedMorseLink(blobDict)
#blob1Dict = dict({(1,((1,4), 0)), (2,((2,3), 0)), (3,((2,3), '10')), (4,((1,2), 1)), (5,((3,4), 1))})
#blobs1 = resolvedMorseLink(blob1Dict)
#resolvedBlobs1 = resolution(blobs1,[])
#print(blobs.components)
#print(blobs1.components)
#print(resolvedBlobs1.components)

knotDict = dict({(1, ((1,2), 0)), (2, ((1,2), 'x', 'lower')), (3, ((1,2), 'x', 'lower')), (4, ((1,2), 1))})
knot = morseLink(knotDict)
knotRes = resolution(knot, [0,1])
print(knotRes.components)
print(knotRes.crossingToComponentsDict)
