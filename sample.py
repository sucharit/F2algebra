
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
  def __init__(self, rowNo, columnNo):
    self.matrix = []
    for row in range(rowNo):
        a = []
        for column in range(columnNo):
            a.append(0)
        self.matrix.append(a)
  def __add(self,x):
    if len(self.matrix) !=len(x):
      raise Exception("You are adding matrices of different row numbers")
    row = len(self.matrix)
    column = len(self.matrix[0])
    c=F2matrix(len(self.matrix),len(self.matrix[0]))
    for i in range row:
      for j in range row[0]:
        c[i][j]=self.matrix[i][j]+x[i][j]
    return F2matrix(c)
    

class F2sparsematrix:
  def __init__(self, rowNo, columnNo):
    return 0


coolmatrix = F2matrix(2, 2)
print(coolmatrix.matrix)

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
print([1,0,1][1])
