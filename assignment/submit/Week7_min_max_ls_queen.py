import random as rd 

def Violations():
 # return the number of violations 
 v = 0
 for i in range(n-1):
  for j in range(i+1,n):
   if x[i] == x[j]: # i and j are on the same row 
    v += 1
   if x[i] + i == x[j] + j: # i and j are on the same diagonal 
    v += 1
   if x[i] - i == x[j] - j: # i and j are on the same diagonal 
    v += 1 

 return v
 
def ViolationOfQueen(q):
 # return the number of violations of queen q 
 v = 0
 for i in range(n):
  if i != q:
   if x[i] == x[q]: #same row 
    v += 1 
   if x[i] + i == x[q] + q:
    v += 1 
   if x[i] - i == x[q] - q:
    v += 1
 return v 
 
def SelectMostViolatingQueen():
 max_violations = 0
 select_queen = -1
 candidate = [] # collect all the best neighbors 
 for q in range(n):
  v = ViolationOfQueen(q)
  if v > max_violations:
   max_violations = v 
   candidate = []
   candidate.append(q) 
  elif v == max_violations:
   candidate.append(q) 

 i = rd.randint(0,len(candidate)-1) # select randomly an index 
 select_queen = candidate[i] 
 return select_queen

def GetDelta(q,r):
 # return the change of the number of violations if queen q is moved to row r 
 current_row = x[q] 
 x[q] = r # temporarily move the queen q to the row r 
 new_violations = Violations() # compute new violations with the new position of queen q 
 delta = new_violations - violations 
 x[q] = current_row # restore the current row of the queen q 
 return delta 
 
def SelectMostPromissingRow(q):
 min_delta = 100000
 selected_row = -1
 candidate = []
 for r in range(n):
  delta = GetDelta(q, r) 
  if delta < min_delta:
   min_delta = delta 
   candidate = []
   candidate.append(r)
  elif delta == min_delta:
   candidate.append(r)
   
 i = rd.randint(0,len(candidate)-1)  
 selected_row = candidate[i] 
 return selected_row

def LocalSearch(maxIter):
 for it in range(maxIter):
  q = SelectMostViolatingQueen()
  r = SelectMostPromissingRow(q)
  x[q] = r
  violations = Violations()
#   print('Step ',it,' violations = ',violations)
  if violations == 0 or it == maxIter - 1:
   a = [i + 1 for i in x]
   print(n)
   print(" ".join(map(str,a)))
   break
  
n = int(input())

x = [0 for i in range(n)] # current solution x[i] is the row of the queen on column i (i = 0, ... n-1)

violations = Violations() # (global) store the violations of the current solution 

if n <= 100:
   LocalSearch(100)
else:
   LocalSearch(10)
