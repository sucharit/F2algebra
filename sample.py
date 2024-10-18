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
  def __len__(self):
    return len(self.matrix)
  def __repr__(self):
    return "F2(%s)" %self.matrix
  def __add__(self,x):
    if len(self.matrix) !=len(x):
      raise Exception("You are adding matrices of different row numbers")
    row = len(self.matrix)
    column = len(self.matrix[0])
    return F2matrix([[self.matrix[i][j]+x[i][j]%2 for j in range(column)] for i in range(row)])
  def __mul__(self,x):
    if self.columnNo != len(x):
      raise Exception("You are multiplying incompatible matrices")
    multMatrix = F2matrix([self.rowNo,len(x[0])])
    for i in range(self.rowNo):
      for j in range(len(x[0])):
        s = 0
        for n in range(self.columnNo):
          s += self[i][n]*x[n][j]
        multMatrix[i][j] = s
    return F2matrix(multMatrix)
  def __rmul__(self,x):
    if len(self[0]) != len(x):
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
  def __setitem__(self,i,x):
    self.matrix[i]=x
    

class F2sparseMatrix:
  def __init__(self, data):
    self.sparseMatrix=[[y for y in x] for x in data]
  def __repr__(self):
    return "F2(%s)" %self.sparseMatrix
  def __add__(self,x):
    addSparseMatrix = []
    for i in range(len(self.sparseMatrix)):
      for j in range(len(x)):
        if self.sparseMatrix[i]==x[j]: break
        if self.sparseMatrix[i]!=x[j] and len(x)-1==j: addSparseMatrix.append(self.sparseMatrix[i])
    for i in range(len(x)):
      for j in range(len(self.sparseMatrix)):
        if x[i]==self.sparseMatrix[j]: break
        if x[i]!=self.sparseMatrix[j] and len(self.sparseMatrix)-1==j: addSparseMatrix.append(x[i])
    return F2sparseMatrix(addSparseMatrix)
  def __radd__(self,x):
    return self+x
  def __getitem__(self,i):
    return self.sparseMatrix[i]
  def __setitem__(self,i,x):
    self.sparseMatrix[i]=x
  def __mul__(self,x):
    return 0
        
      
      


grey = F2matrix([2,2])

green = F2(2)
blue = F2(4)
yellow = green + blue
yellow + 2
v=F2vect(3)
v[2]=1
w=1*v
v[0]=1
print("v")
print(v)
print(w)
a=[0,1,2]
b=a
a[1]=7
print(a)
print(b)
green = F2vect([3,4,5])
pink = F2matrix([[1,33],[1,1]])
teal = F2matrix([[0,0],[0,1]])
print(pink)
pink[1][1]=0
print(pink)
print(teal)
print(pink*teal)
print([[1,33],[1,1]]*teal)
print([[0,0],[0,1]]*teal)
print("Sparse Matrix")
black = F2sparseMatrix([[1,1],[1,2]])
orange = black + [[2,2]]
print(orange)
cyan = [[3,1],[2,4]] + orange
print(cyan)
