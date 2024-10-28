import numpy as np


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
    
def minNoRowNos(x):
  rows = set(x.entriesInRow)
  labeledRows = {(i,x.entriesInRow[i]) for i in range(x.rowNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(x.entriesInRow[i])) for i in range(x.rowNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  for i in range(x.rowNo):
    minNoRowNos[labeledRowMinsDict[i]] = minNoRowNos[labeledRowMinsDict[i]] | {i}
  return minNoRowNos

def reduceRowSparse(x):
  rows = set(x.entriesInRow)
  labeledRows = {(i,x.entriesInRow[i]) for i in range(x.rowNo)}
  labeledRowsDict = dict(labeledRows)
  labeledRowMins = {(i,min(x.entriesInRow[i])) for i in range(x.rowNo)}
  labeledRowMinsDict = dict(labeledRowMins)
  mins = {min(row) for row in rows}
  minNoRowNos = dict({(i,frozenset()) for i in mins})
  for i in range(x.rowNo):
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
  reducedRowEchelon = {echelonMinNoRowsDict[i] for i in echelonMinNoRowsDict.keys()}
  return reducedRowEchelon
    


#a=[0,1,2]
#b=a
#a[2]=4
#a[1]=7
#print(a)
#print(b)


brown = F2matrix([[2,2,3],[1,1,1],[0,0,0]])
pink = F2sparseMatrix({(1,1),(1,2),(2,2),(3,2),(3,3),(5,5),(5,6),(6,1),(6,8)})
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
print(minNoRowNos(pink))
print(reduceRowSparse(pink))
green = F2sparseMatrix({(1,1), (1,2), (2,2)})
print(minNoRowNos(green))
print(reduceRowSparse(green))
