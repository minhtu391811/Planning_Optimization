import random as rd 

n = 100
x = [0 for i in range(n)] # x[i] is the row of the queen on column i 
T = [[0 for i in range(n)] for j in range(n)] # tabu list representation
                                              # T[q][r] > it means move (q,r: x[q] = r) is forbidden at the current iteration it
tbl = 10 # length of the tabu list: store tbl recent moves in the tabu list 
violations = 0 # global variables representing the violations of the current solution 

def Violations():
 v = 0
 for i in range(n):
  for j in range(i+1,n):
   if x[i] == x[j]:
    v += 1
   if x[i] + i == x[j] + j:
    v += 1
   if x[i] - i == x[j] - j:
    v += 1
 return v 
 
def GetDelta(q,r):
 # return the violations change if queen q is moved row r 
 oldV = x[q]
 x[q] = r # perform the move 
 newViolations = Violations() # compute new violations 
 delta = newViolations - violations
 x[q] = oldV # undo the move 
 return delta
 
def GenerateInitialSolution():
 global violations 
 
 for i in range(n):
  x[i] = 0
 violations = Violations() 

def TabuSelect(it):
 global violations 

 # it: current iteration of the tabu search 
 minD = 1e9
 # explore all possible moves which are not tabu and bring smallest violations change 
 for q in range(n):
  for r in range(n):
   if x[q] != r:
    if T[q][r] <= it: # move (q,r: x[q] = r) is not tabu (not in the tabu list), time O(1)
     delta = GetDelta(q,r)
     if delta < 0:
      L = [q, r]
      minD = delta  
      
 return L, minD  
 
def TabuSearch(maxIter):
 global violations

 GenerateInitialSolution()
 print('Initial violations = ',violations)
 for it in range(maxIter):
  if(violations == 0):
   break 
   
  [q,r],delta = TabuSelect(it)
  x[q] = r # perform the local move to generate new current solution
  T[q][r] = it + tbl # add the move(q,r) to the tabu list 
  violations = Violations()
  print('Step ',it,': Move (',q,',',r,'), delta = ',delta,' new violations = ',violations)
 for i in x:
   print(i + 1, end = " ")
  
TabuSearch(10000)  