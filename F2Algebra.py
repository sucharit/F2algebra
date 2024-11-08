class F2:
  def __init__(self, number):
    self.number = number % 2
  def __repr__(self):
    return "F2(%s)" %self.number
  def __add__(self, x):
    try:
      return F2(self.number+x.number)
    except AttributeError:
      return F2(self.number+x)
  def __radd__(self,x):
    return F2(self.number+x)
  def __mul__(self, x):
    try:
      return F2(self.number * x.number)
    except AttributeError:
      return F2(self.number * x)
  def __rmul__(self,x):
    return F2(self.number * x)
  def __sub__(self, x):
    return self + x
  def __rsub__(self, x):
    return self + x


class F2vect:
  def __init__(self, x):
    try:
      self.vect = [i % 2 for i in x]
    except TypeError:
      self.vect = [0 for i in range(x)]
    #self.dim = len(self.vect)
  def __len__(self):
    return len(self.vect)
  def __repr__(self):
    return "F2(%s)" %self.vect
  def __add__(self, x):
    if len(self.vect) != len(x):
      raise Exception("You are adding vectors of different lengths")
    return F2vect([self.vect[i]+x[i] for i in range(len(self.vect))])
  def __radd__(self,x):
    return self+x
  def __sub__(self,x):
    return self+x
  def __rsub__(self,x):
    return self+x
  def __mul__(self,x):
    if x % 2 == 0:
      return F2vect(len(self.vect))
    else:
      return F2vect(self.vect)
  def __rmul__(self,x):
    return self*x
  def __getitem__(self,i):
    return self.vect[i]
  def __iter__(self):
    yield from self.vect
  def __setitem__(self,i,x):
    self.vect[i]=x
    


class F2matrix:
  def __init__(self, data):
    try:
      self.matrix=[[y % 2 for y in x] for x in data]
      self.rowNo=len(self.matrix)
      self.columnNo=len(self.matrix[0])
    except  (SyntaxError, TypeError):
      self.rowNo=data[0]
      self.columnNo=data[1]
      self.matrix=[[0 for y in range(self.columnNo)] for x in range(self.rowNo)]
  def __repr__(self):
    return "F2matrix(%s)" %self.matrix
  def __add__(self,x):
    try:
      if self.rowNo !=x.rowNo or self.columnNo!=x.columnNo:
        raise Exception("You are adding matrices of different dimensions")      
      return F2matrix([[self.matrix[i][j]+x.matrix[i][j] for j in range(self.columnNo)] for i in range(self.rowNo)])
    except:
      return F2matrix([[self.matrix[i][j]+x[i][j] for j in range(self.columnNo)] for i in range(self.rowNo)])

  def __mul__(self,x):
    if self.columnNo != x.rowNo:
      raise Exception("You are multiplying incompatible matrices")
    multMatrix = F2matrix([self.rowNo,x.columnNo])
    for i in range(self.rowNo):
      for j in range(x.columnNo):
        s = 0
        for n in range(self.columnNo):
          s += self[i][n]*x[n][j]
        multMatrix[i][j] = s
    return F2matrix(multMatrix)
  def __rmul__(self,x):
    if self.columnNo != len(x):
      raise Exception("You are multiplying incompatible matrices")
    multMatrix = F2matrix([len(x),self.columnNo])
    for i in range(len(x)):
      for j in range(self.columnNo):
        s = 0
        for n in range(self.rowNo):
          s += x[i][n]*self[n][j]
        multMatrix[i][j] = s
    return F2matrix(multMatrix)
  def __radd__(self,x):
    return self+x
  def __getitem__(self,i):
    return self.matrix[i]
  def __setitem__(self,index,x):
    self.matrix[index[0]][index[1]]=x
    

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

class F2sparseEchelon:
  def __init__(self, data):
    try:
      self.sparseEchelon = dict({(i,data[i]) for i in data.keys()})
      self.sparseEchelonSet = {data[i] for i in data.keys()}
      self.pivots = data.keys()
    except AttributeError:
      self.sparseEchelon = dict({(min(data.entriesInRow[i]), data.entriesInRow[i]) for i in range(data.rowNo)})
      self.sparseEchelonSet = {data.entriesInRow[i] for i in range(data.rowNo)}
      self.pivots = {min(data.entriesInRow[i]) for i in range(data.rowNo)}
    self.columnMin = min(self.sparseEchelon.keys())
    self.columnMax = max(max(row) for row in self.sparseEchelonSet)
    self.nonPivots = set(range(self.columnMin, self.columnMax + 1)) - self.pivots
  def __repr__(self):
    return "F2sparseEchelon(%s)" %self.sparseEchelonSet
  def __getitem__(self,i):
    return self.sparseEchelon[i]

def rowEchelonSparse(x):
  try:
    rowNo = x.rowNo
    entriesInRow = x.entriesInRow
    rows = set(entriesInRow)
  except AttributeError:
    rows = x
    rowNo = len(rows)
    entriesInRow = tuple(x)
  labeledRows = {(i,entriesInRow[i]) for i in range(rowNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(entriesInRow[i])) for i in range(rowNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  #dictionary with keys that are the minimum nonzero entry of the rows. Given a minimum, the dictionary outputs the set of of codes that correspond to rows with minimumum zero entry being the key 
  for i in range(rowNo):
    minNoRowNos[labeledRowMinsDict[i]] = minNoRowNos[labeledRowMinsDict[i]] | {i}
  activeMins = {n for n in mins}
  while activeMins != set():
    selectedMin = min(activeMins)
    if len(minNoRowNos[selectedMin]) == 1:
      activeMins.remove(selectedMin)
    else:
      minRowNo = min(minNoRowNos[selectedMin])
      maxRowNo = max(minNoRowNos[selectedMin])
      diffSet = labeledRowsDict[minRowNo] ^ labeledRowsDict[maxRowNo]
      if diffSet == set():
        del labeledRowsDict[maxRowNo]
        del labeledRowMinsDict[maxRowNo]
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
      else:
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
        labeledRowsDict[maxRowNo] = diffSet
        newMin = min(diffSet)
        labeledRowMinsDict[maxRowNo] = newMin
        if newMin in minNoRowNos.keys():
          minNoRowNos[newMin] = minNoRowNos[newMin] | frozenset({maxRowNo})
        else:
          minNoRowNos[newMin] = frozenset({maxRowNo})
        activeMins.add(newMin)
        mins.add(newMin)
        #minNoRowNos represents the echelon form now
  echelonMinNoRowsDict = dict({(minKey,labeledRowsDict[min(minNoRowNos[minKey])]) for minKey in mins})
  return F2sparseEchelon(echelonMinNoRowsDict)

def reduceRowSparse(x):
  try:
    rowNo = x.rowNo
    entriesInRow = x.entriesInRow
    rows = set(entriesInRow)
  except AttributeError:
    rows = x
    rowNo = len(rows)
    entriesInRow = tuple(x)
  labeledRows = {(i,entriesInRow[i]) for i in range(rowNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(entriesInRow[i])) for i in range(rowNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  #dictionary with keys that are the minimum nonzero entry of the rows. Given a minimum, the dictionary outputs the set of of codes that correspond to rows with minimumum zero entry being the key 
  for i in range(rowNo):
    minNoRowNos[labeledRowMinsDict[i]] = minNoRowNos[labeledRowMinsDict[i]] | {i}
  activeMins = {n for n in mins}
  while activeMins != set():
    selectedMin = min(activeMins)
    if len(minNoRowNos[selectedMin]) == 1:
      activeMins.remove(selectedMin)
    else:
      minRowNo = min(minNoRowNos[selectedMin])
      maxRowNo = max(minNoRowNos[selectedMin])
      diffSet = labeledRowsDict[minRowNo] ^ labeledRowsDict[maxRowNo]
      if diffSet == set():
        del labeledRowsDict[maxRowNo]
        del labeledRowMinsDict[maxRowNo]
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
      else:
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
        labeledRowsDict[maxRowNo] = diffSet
        newMin = min(diffSet)
        labeledRowMinsDict[maxRowNo] = newMin
        if newMin in minNoRowNos.keys():
          minNoRowNos[newMin] = minNoRowNos[newMin] | frozenset({maxRowNo})
        else:
          minNoRowNos[newMin] = frozenset({maxRowNo})
        activeMins.add(newMin)
        mins.add(newMin)
        #minNoRowNos represents the echelon form now
  echelonMinNoRowsDict = dict({(minKey,labeledRowsDict[min(minNoRowNos[minKey])]) for minKey in mins})
  echelonActiveMins = {n for n in mins}
  while echelonActiveMins != set():
    selectedMin = max(echelonActiveMins)
    echelonActiveMins.remove(selectedMin)
    for n in echelonActiveMins:
      if selectedMin in echelonMinNoRowsDict[n]:
        echelonMinNoRowsDict[n] = echelonMinNoRowsDict[n] ^ echelonMinNoRowsDict[selectedMin]
  return F2sparseEchelon(echelonMinNoRowsDict)

def columnEchelonSparse(x):
  rows = set(x.entriesInColumn)
  labeledRows = {(i,x.entriesInColumn[i]) for i in range(x.columnNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(x.entriesInColumn[i])) for i in range(x.columnNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  #dictionary with keys that are the minimum nonzero entry of the rows. Given a minimum, the dictionary outputs the set of of codes that correspond to rows with minimumum zero entry being the key 
  for i in range(x.columnNo):
    minNoRowNos[labeledRowMinsDict[i]] = minNoRowNos[labeledRowMinsDict[i]] | {i}
  activeMins = {n for n in mins}
  while activeMins != set():
    selectedMin = min(activeMins)
    if len(minNoRowNos[selectedMin]) == 1:
      activeMins.remove(selectedMin)
    else:
      minRowNo = min(minNoRowNos[selectedMin])
      maxRowNo = max(minNoRowNos[selectedMin])
      diffSet = labeledRowsDict[minRowNo] ^ labeledRowsDict[maxRowNo]
      if diffSet == set():
        del labeledRowsDict[maxRowNo]
        del labeledRowMinsDict[maxRowNo]
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
      else:
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
        labeledRowsDict[maxRowNo] = diffSet
        newMin = min(diffSet)
        labeledRowMinsDict[maxRowNo] = newMin
        if newMin in minNoRowNos.keys():
          minNoRowNos[newMin] = minNoRowNos[newMin] | frozenset({maxRowNo})
        else:
          minNoRowNos[newMin] = frozenset({maxRowNo})
        activeMins.add(newMin)
        mins.add(newMin)
  echelonMinNoRowsDict = dict({(minKey,labeledRowsDict[min(minNoRowNos[minKey])]) for minKey in mins})
  return(F2sparseEchelon(echelonMinNoRowsDict))

#class subspace:
#k-dim subspaces of R^n, remember k, n, an ordered basis (k\times n sparse matrix or its transpose)
#should have function to check if a given vector in R^n is in the subspace, and if so, returns coefficients in terms of basis elts.


#class subspace of subspace:
#example im subset ker subset R^n , remember a basis of im, then a basis for ker, which contains the basis for im as its first elements.
#similar functions


def reduceColumnSparse(x):
  rows = set(x.entriesInColumn)
  labeledRows = {(i,x.entriesInColumn[i]) for i in range(x.columnNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(x.entriesInColumn[i])) for i in range(x.columnNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  #dictionary with keys that are the minimum nonzero entry of the rows. Given a minimum, the dictionary outputs the set of of codes that correspond to rows with minimumum zero entry being the key 
  for i in range(x.columnNo):
    minNoRowNos[labeledRowMinsDict[i]] = minNoRowNos[labeledRowMinsDict[i]] | {i}
  activeMins = {n for n in mins}
  while activeMins != set():
    selectedMin = min(activeMins)
    if len(minNoRowNos[selectedMin]) == 1:
      activeMins.remove(selectedMin)
    else:
      minRowNo = min(minNoRowNos[selectedMin])
      maxRowNo = max(minNoRowNos[selectedMin])
      diffSet = labeledRowsDict[minRowNo] ^ labeledRowsDict[maxRowNo]
      if diffSet == set():
        del labeledRowsDict[maxRowNo]
        del labeledRowMinsDict[maxRowNo]
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
      else:
        minNoRowNos[selectedMin] = minNoRowNos[selectedMin] - {maxRowNo}
        labeledRowsDict[maxRowNo] = diffSet
        newMin = min(diffSet)
        labeledRowMinsDict[maxRowNo] = newMin
        if newMin in minNoRowNos.keys():
          minNoRowNos[newMin] = minNoRowNos[newMin] | frozenset({maxRowNo})
        else:
          minNoRowNos[newMin] = frozenset({maxRowNo})
        activeMins.add(newMin)
        mins.add(newMin)
        #minNoRowNos represents the echelon form now
  echelonMinNoRowsDict = dict({(minKey,labeledRowsDict[min(minNoRowNos[minKey])]) for minKey in mins})
  echelonActiveMins = {n for n in mins}
  while echelonActiveMins != set():
    selectedMin = max(echelonActiveMins)
    echelonActiveMins.remove(selectedMin)
    for n in echelonActiveMins:
      if selectedMin in echelonMinNoRowsDict[n]:
        echelonMinNoRowsDict[n] = echelonMinNoRowsDict[n] ^ echelonMinNoRowsDict[selectedMin]
  return F2sparseEchelon(echelonMinNoRowsDict)

def kernel(x):
  kernel = set()
  reduceRow = reduceRowSparse(x)
  for n in reduceRow.nonPivots:
    generator = {n}
    for i in reduceRow.pivots:
      if (i < n) and (n in reduceRow.sparseEchelon[i]):
        generator.add(i)
    generator = frozenset(generator)
    kernel.add(generator)
  #return kernel
  return rowEchelonSparse(kernel)

def image(x):
  reduceColumn = columnEchelonSparse(x)
  return reduceColumn

def homology(x,y):
  xKernel = kernel(x)
  yImage = image(y)
  leftOverPivots = xKernel.pivots - yImage.pivots
  kernelSubspace = dict({(pivot, xKernel[pivot]) for pivot in leftOverPivots})
  return F2sparseEchelon(kernelSubspace)

#a=[0,1,2]
#b=a
#a[2]=4
#a[1]=7
#print(a)
#print(b)


brown = F2matrix([[2,2,3],[1,1,1],[0,0,0]])
pink = F2sparseMatrix({(1,1),(1,2),(2,2),(3,2),(3,3),(5,5),(5,6),(6,1),(6,8)})
green = F2sparseMatrix({(1,1),(2,1),(2,2),(3,2)})
#blue = F2sparseMatrix({(1,2),(2,2),(2,100)})
#green = pink * blue
#print(green)
#print(green[(2,3)]
#pink.sparseMatrix.remove((1,1))
#print(pink)
#print(pink.columnTuple)
print(pink)
print(pink.rowTuple)
print(pink.entriesInRow)
print(reduceRowSparse(pink))
print(kernel(pink))
print(image(pink))
brown = F2sparseMatrix({(4,2),(5,2),(6,2),(5,3),(6,3),(7,3)})
print(homology(pink,brown))
