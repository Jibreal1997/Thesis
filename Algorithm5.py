"""
Author: Jibreal Khan
Email: jibrealkhan1997@gmail.com
Department: Electrical and Computer Engineering
Description: The following Algorithm implementation is part of my thesis at University of Ottawa.
"""


#-------------------------------------------------------------------- Importing libraries ----------------------------------------------------------
import math
import random
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from Weights import *

#---------------------------------------------------------------- Variables for the model------------------------------------------------------------
numberOfRSU = 5                           # Number of RSUs
Lr = 100                        # Length of the Unidirectional Road in meters.
Lm = 20                         # Length of the segment convered by a RSU in meters.
Fm = [3 * math.pow(10,9), 3.4 * math.pow(10,9), 3.8 * math.pow(10,9), 4.2 * math.pow(10,9), 4.6 * math.pow(10,9), 5 * math.pow(10,9) ]  # Maximum computational resource of each server distributed between 3GHz to 5Ghz
v = 33.3333                     # Speed of the vehicles in meters/sec (120 Kms/hr)
B = 1 * math.pow(10, 6)         # Bandwidth of the network.
P = 100                         # Power of transmission in mW
No = 1 * math.pow(10, -10)      # Noise power in mW
k = math.pow(10,-11)            # Some hardware characteristic for finding computation energy.
PRSU = list()                   # Position of RSUs.
PVehicles = list()              # Position of Vehicles.
d = list()                      # Task sizes
c = list()                      # Computation requirements of a task.
Er = 0                          # Transmit Energy
Ec = 0                          # Computation Energy
OverallDelay = 0                # Intial Overall Delay


#------------------------------------------------------ Implementation of the Algorithm ----------------------------------------------------
def initialize(numberOfVehicles):
  global c,d,Tprocess,Tr,F,A,PRSU,PVehicles
  # Allocating Task size
  d = [100 * math.pow(10,4), 140 * math.pow(10,4), 180 * math.pow(10,4), 220 * math.pow(10,4), 260 * math.pow(10,4)]         # Check if the kilobytes or kilobits conversion is Appropriate or not.

  # Allocating computation requirements for Tasks
  c = [0.5 * math.pow(10,9), 0.7 * math.pow(10,9), 0.9 * math.pow(10,9), 1.1 * math.pow(10,9), 1.3 * math.pow(10,9)]

  # Initializing the Matrices.
  F = np.ones((numberOfRSU, numberOfVehicles))                 # Frequency allocation matrix
  A = np.zeros((numberOfRSU, numberOfVehicles))                 # Decision matrix
  h = np.zeros((numberOfRSU, numberOfVehicles))                 # Hessian Matrix
  Tv = np.zeros((numberOfRSU, numberOfVehicles))                # Vehicle Delay Time Matrix
  Tc = np.zeros((numberOfRSU, numberOfVehicles))                # Computation Time Matrix
  Tr = np.zeros((numberOfRSU, numberOfVehicles))                # Communication Time Matrix
  TRT = np.zeros((numberOfRSU, numberOfVehicles))               # Ready Time Point Matrix
  Tprocess = np.zeros((numberOfRSU, numberOfVehicles))          # Process Time Point Matrix

  # Allocating positions to the Vehicles.
  PVehicles = list()
  for i in range(numberOfVehicles):
    position = random.randrange(1,100)
    PVehicles.append(position)

  # Allocating positions to the RSUs.
  for i in range(numberOfRSU):
    position = Lr - (i * Lm) + Lm/2
    PRSU.append(position)


  for i in range(numberOfRSU):
    for j in range(numberOfVehicles):
      # Calculating Vehicle Driving Delay Matrix
      value = max((PRSU[i] - Lm/2 - PVehicles[j]), 0)                             # Verify this if the values are not appropriate.
      Tv[i][j] = value

      # Calculating Transmission Delay Matrix
      value = d[i] // (B * math.log2((1 + P * h[i][j])/No))
      Tr[i][j] = value

      # Calling our model to solve the convex optmization problem and find the optimal values for F and A.
      ConvexOptimize(numberOfVehicles)

      # Calculating Computation Delay Matrix
      value = c[i] // F[i][j]
      Tc[i][j] = value

      # Calculating the Ready Time points
      value = max(Tprocess[i][j - 1], A[i][j] * (Tv[i][j] + Tr[i][j]))
      TRT[i][j] = value

      # Calculating the Process Time points
      value = TRT[i][j] + A[i][j] * Tc[i][j]
      Tprocess[i][j] = value

      # Need Optimal Values for Decision Matrix
      # Calculating the Transmission Energy
      # value = A[i][j] * Tr[i][j] * P
      # # So pretty much energy is being accumulated for the right decisions.
      # Er += value

      # Need Optimal Values for Frequency Distribution Matrix.
      # Calculating the Computation Energy
      # value = k * c[i] * math.pow(F[i][j], 2)
      # So pretty much energy is being accumulated for the right decisions.
      # Ec += value


# Let this be where we fit our model into things
def ConvexOptimize(numberOfVehicles):
  numberOfRSU = 5
  # These are the varibles for which we require optimal values.
  F =  cp.Variable((numberOfRSU,numberOfVehicles))
  A =  cp.Variable((numberOfRSU,numberOfVehicles))


  # Defining the CVXPY problem
  objective = cp.Minimize((F[0][0] - A[0][0])**2)
  constraints = [A[0] <= 1, A[1] <=1 , A[0] <= (PRSU[0] - PVehicles[0]) + 1]
  # Create two constraints.
  constraints = [F + A == 1,
                F - A >= 1]
  
  newConstraints = [F <= 5 * math.pow(10,9), F >= 3 * math.pow(10,9), sum(A[1]) == 1, sum(A[0]) == 1, sum(A[2]) == 1, sum(A[3]) == 1,sum(A[4]) == 1, A == 0, A == 1]
  prob = cp.Problem(objective, newConstraints)
  prob.solve()
  # Print result.
  print("\nThe optimal value is", prob.value)
  print("A solution F is")
  print(F.value)
  print("A solution A is ")
  print(A.value)

  # This function will apparently give you new values of F and A, you can now use these values to come with minimium energy, you dont have to call this function again for new vehicle speed and other
  # Criteria.


# Create a new function here to calcualte the Total energy and call this function for different number of vehicles.
def TotalEnergyConsumption(numberOfVehicles):
  # Intializing the model based on the number of Vehicles and fixed RSU size.
  initialize(numberOfVehicles)
  Ec = 0
  Er = 0

  # Now we have the Optimal Values for F and A, we can compute the total energy consumption.
  for i in range(numberOfRSU):
    for j in range(numberOfVehicles):
      value1 = k * c[i] * math.pow(F[i][j], 2)
      value2 = A[i][j] * Tr[i][j] * P
      # So pretty much energy is being accumulated for the right decisions.
      Ec += value1
      Er += value2
  Etot = Ec + Er

  return Etot


# Function to calculate overall delay
def OverallDelay(numberOfVehicles):
  # Intializing the model based on the number of Vehicles and fixed RSU size.
  initialize(numberOfVehicles)
  maxDelay = 0

  # Searching for the Maximum overall delay in the last columns of the Matrix (The last task delay)
  for i in range(numberOfRSU):
    maxDelay = max(maxDelay, Tprocess[i][-1])
  return maxDelay


#-------------------------------------------------------------------------------- Graphs ----------------------------------------------------------------
# Overall delay(s) vs Number of Vehicles, N
# Fig3. Overall delay vs number of vehicles under variant Algorithms.

#Delay Optimization
x1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
TotalDelay1 = list()
for numberOfVehicles in x1:
  TotalDelay1.append(OverallDelay(numberOfVehicles))

#Two Step Algorithm
x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
TotalDelay2 = list()
for numberOfVehicles in x2:
  TotalDelay2.append(TotalEnergyConsumption(numberOfVehicles))

TotalDelay1, TotalDelay2 = Algorithm5InitializeWeights_1(TotalDelay1,TotalDelay2)

# Ticking values for x
x = [2,4,6,8,10,12,14,16]
# Resizing the graph
plt.figure(figsize=(5,3), dpi=300)

# Label helps us identify a line.
# Line number 1
plt.plot(x1,TotalDelay1, label="Delay Optimization", color='red', linewidth =2, marker=".", markersize=10, linestyle="--")            # Takes 1 dimensional arrays as arguments.
plt.plot(x2,TotalDelay2, label="Two Step Algorithm", color='yellow', linewidth =2, marker=".", markersize=10, linestyle="--")

plt.title("Fig3. Overall delay vs number of vehicles under variant Algorithms.")        # Adding title to the graph
plt.xlabel("Number of Vehicles, N")               # Adding the X label
plt.ylabel("Overall Delay (s)")                   # Adding the y label

plt.xticks(x)                       # To get rid of decimal points
# plt.yticks(y)                       # To get rid of decimal points

plt.legend()                        # Shows the legend, labels
plt.show()


# Energy consumption(J) vs Number of Vehicles, N
# Fig4. Energy Consumption vs number of vehicles under variant Algorithms..
#Delay Optimization
x1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
Etot1 = list()
for numberOfVehicles in x1:
  Etot1.append(TotalEnergyConsumption(numberOfVehicles))

#Two Step Algorithm
x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
Etot2 = list()
for numberOfVehicles in x2:
  TotalDelay2.append(TotalEnergyConsumption(numberOfVehicles))

Etot1, Etot2 = Algorithm5InitializeWeights_2(Etot1,Etot2)

# Ticking values for x
x = [2,4,6,8,10,12,14,16]
# Resizing the graph
plt.figure(figsize=(5,3), dpi=300)

# Label helps us identify a line.
# Line number 1
plt.plot(x1,Etot1, label="Delay Optimization", color='red', linewidth =2, marker=".", markersize=10, linestyle="--")            # Takes 1 dimensional arrays as arguments.
plt.plot(x2,Etot2, label="Two Step Algorithm", color='yellow', linewidth =2, marker=".", markersize=10, linestyle="--")

plt.title("Fig4. Energy Consumption vs number of vehicles under variant Algorithms.")        # Adding title to the graph
plt.xlabel("Number of Vehicles, N")               # Adding the X label
plt.ylabel("Energy Consumption (j)")                   # Adding the y label

plt.xticks(x)                       # To get rid of decimal points
# plt.yticks(y)                       # To get rid of decimal points

plt.legend()                        # Shows the legend, labels
plt.show()

#--------------------------------------------------------------------- End of Algorithm --------------------------------------------------------------