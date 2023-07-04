"""
Author: Jibreal Khan
Email: jibrealkhan1997@gmail.com
Department: Electrical and Computer Engineering
Description: The following Algorithm implementation is part of my thesis at University of Ottawa.
"""

#---------------------------------------------------------Importing Libraries----------------------------------------------------------------#
import math
import matplotlib.pyplot as plt
from Weights import *

#------------------------------------------------------------- System Model ----------------------------------------------------------------#
K = 20  # Number of RSUs
No = -80 # Noise dBm
B = 5 * math.pow(10,6) # Bandwidth in hertz
α = 4
κk= math.pow(10,-11)    # Effective switch capacitance
ϕk = 3                  # Just a constant

# Single tier network settings
R = [500] * K   # Segment of the road covered by RSU
P = [50]  * K   # Maximum power of RSU
F = [1.1] * K   # Maximum frequency of

# Communication model
gk = 1    # large scale fading power of the channel between RSU k and vehicle u
lk = 0    # maximum link length between RSU k and vehicle u.

# Multi vehicle scenario
def initialize_multi_vehicle():
  Rreq1 =300      # Distance of vehicle-1 from the first RSU in meters
  Rreq2 =400      # Distance of vehicle-2 from the frist RSU in meters
  Rreq3 =500      # Distance of vehicle-3 from the frist RSU in meters

  δv = 5          # Difference in speeds of the vehicles. Km/hr
  δD = 0          # Difference in computation result size of the vehicles MB

  D = 50
  v = 80

  # Computation result sizes of the vehicles
  D1 = (D - δD)
  D2 = D
  D3 = (D + δD)

  # Speeds of the vehicles
  v1 = (v - δv)
  v2 = v
  v3 = (v + δv)

#--------------------------------------------------------- Implementation of Algorithms-------------------------------------------#
def GInv():
  return 1

# Single Vehicle Total energy consumption, we simply need to model and solve problems 5 and 4 respectively.
def single_vehicle_energy(velocity = 75, ComputationResultSize = 300):
  Rreq1 =300                                              # Distance from the first RSU in meters
  D1 = ComputationResultSize * 8 * math.pow(10,6)         # Size of the computation result in MB (This is supposed to be in bits)
  v1 = velocity/3.6                                       # Speed of the vehicle in Meters/second

  C1 = 1000 * D1                                          # Total computation workload of the task. (This is in hertz)

  # Time of Single Vehicle Arrival and Departure from the multiple RSUs
  Tarrival = [0] * K
  Tdeparture = [0] *  K

  # Communication model
  y = [0] * K   # Recieved signal between vehicle and K RSUs.
  p = [0] * K   # Power Allocated to each of the K RSUs.
  h = [0] * K   # Small scale fading coefficients of the channel.
  s = [0] * K   # Information symbol.
  SNR = [0] * K # Signal to noise ratio.
  z = 0         # Additive white Gaussian Noise
  w = [0] * K   # Normalized beam forming vector
  C = [0] * K   # Achievable instantaneous data rate for vehicle at each of the K RSUs.
  tcm = [0] * K # Time to trasmit the the results from RSU to vehicle.
  Ecm = [0] * K # Energy of communication for each subtask result.
  pOpt = [0] * K # Optimal power allocation.


  X = [0] * K  # Task splitting across the K RSUs.
  XOpt = [0] * K # Optimal task splitting across K RSUs.
  CuX = [0] * K # Computation workload of subtask at the RSU.
  DuX = [1.2 * math.pow(10,8)] * K # Computation result size of subtask at the RSU. (Giving it some random value)
  f = [0] * K   # Freqeuncy allocation for each subtask at each RSU.
  tcp = [0] * K # Computation Time for executing subtask at each RSU.
  Ecp = [0] * K # Energy of computation for each subtask at each RSU.
  ScpOpt = [0] * K  # Optimal computation start time for each RSU.
  ScmOpt = Tarrival # Optimal communication start time for each RSU.
  Etot = [0] * K # Optimal total energy.

  for i in range(K):
    Tarrival[i] = (1 / v1) * (Rreq1 + sum(R[:i]) - 500)    # We subtract 500 in order to not consider the range covered by the RSU.
    Tdeparture[i] = (1 / v1) * (Rreq1 + sum(R[:i]))        # Here, we consider the range of the RSU.

    # Note: For the entire communication model stuff, we need optimal power allocation and for the computation model, we need optimal task distribution.
    # This is the solution to problem 5 and is supposed to give us optimal power allocation, but the question is what is the task distribution used here.
    pOpt[i] = (No / (gk * GInv())) * (math.pow(2, ((DuX[i]) / (B *  (Tdeparture[i] - Tarrival[i])))))
    # Something that gets the Optimal task allocation must take place here.
    choice1 = ((B * (Tdeparture[i] - Tarrival[i]) / D1) * math.log2(1 + (P[i]*gk*GInv()/ No)))
    choice2 = (F[i] * Tarrival[i]) / C1
    # choice3 = max(HInv(γ∗), 0)
    XOpt[i] = min(choice1, choice2)

    # All of these rely on Optimal Task Distribution, X.
    CuX[i] = C1 * X[i]                                  # Computation workload of the subtask at RSU. (Hz)
    DuX[i] = D1 * X[i]                                  # Computation result size of the subtask at RSU. (Bits)
    #tcp[i] = CuX[i]/f[i]                                # Computation Time for executing subtask at each RSU.
    Ecp[i] = κk * CuX[i] * math.pow(Tarrival[i],(ϕk - 1)) * math.pow(X[i], ϕk)     # Energy of computation for each subtask at each RSU. (Relies on frequency allocation)

    # All of this relies upon optimal power allocation for the RSU, p.
    # Communication model stuff
    y[i] = h[i] * w[i] * math.sqrt(p[i] * gk) * s[i] + z      # Computation of the recieved signal by vehicle at RSU.
    SNR[i] = (p[i] * (abs(h[i] * w[i])**2) * gk) / No         # Computation of the Signal to noise ratio between the vehicle and RSU.
    #C[i] = B * math.log((1 + p[i] * abs(h[i])**2 * gk) / No)   # Computation of the data rate between the vehicle and the RSU.
    # CSI - Channel State Information , MRT - Maximal Ratio Transmission , This is where the probabilities start..... e -> Maximum target data rate.
    #tcm[i] = DuX[i] / e[i]                                    # Time to transmit the communication result from the RSU to the vehicle.

    Ecm[i] = pOpt[i] * (Tdeparture[i] - Tarrival[i])  # Communication energy for each subtask result.

    # At this point we have optimal communication and optimal computation energy.
    Etot[i] = Ecp[i] + Ecm[i]                                 # Total Energy.
  
  return sum(Etot)

#-------------------------------------------------------- Plotting the graphs -----------------------------------------------------------------------

# Total Energy consumption(J) vs Vehicle's velocity v1 (Km/hr)
#Two-tier
x1 = [30,40,50,60,70,80,90,100,110,120,130,140,150]                   # This is the Change is Vehicluar Velocity
# Basically for each change in Vehicluar velocity you will need to recall the function to calculate the total energy of all the RSUs.
EtotSum1 = list()
for velocity in x1:
    EtotSum1.append(single_vehicle_energy(velocity,300))
#Single-tier
x2 = [30,40,50,60,70,80,90,100,110,120,130,140,150,160]
# Basically for each change in Vehicluar velocity you will need to recall the function to calculate the total energy of all the RSUs.
EtotSum2 = list()
for velocity in x2:
    EtotSum2.append(single_vehicle_energy(velocity))
EtotSum1, EtotSum2 = Algorithm4InitializeWeights_1(EtotSum1,EtotSum2)
# For ticking
x = [20,40,60,80,100,120,140,160]
# Resizing the graph
plt.figure(figsize=(5,3), dpi=300)
# Label helps us identify a line.
# Line number 1
plt.plot(x1,EtotSum1, label="Proposed (Single-tier)", color='red', linewidth =2, marker=".", markersize=10, linestyle="--")            # Takes 1 dimensional arrays as arguments.
plt.plot(x2,EtotSum2, label="Proposed (Two-tier)", color='yellow', linewidth =2, marker=".", markersize=10, linestyle="--")
plt.title("Fig3(a) Total Energy consumption versus the velcity of the vehicle v1 in single and two tier network.")        # Adding title to the graph
plt.xlabel("Vehicle's velocity, v1(KM/hr)")               # Adding the X label
plt.ylabel("Total Energy consumption (J)")              # Adding the y label
plt.xticks(x)                       # To get rid of decimal points
# plt.yticks(y)                       # To get rid of decimal points
plt.legend()                        # Shows the legend, labels
plt.show()


# Total Energy consumption(J) vs Computation Result Size, D1(MB)
#Two-tier
x1 = [50,100,150,200,250,300,350,400,450,500,550,600]
# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
EtotSum1 = list()
for ComputationResultSize in x1:
    EtotSum1.append(single_vehicle_energy(ComputationResultSize))
#Single-tier
x2 = [50,100,150,200,250,300,350,400,450,500,550,600,650]
# Basically for each change in Computation result size you will need to recall the function to calculate the total energy of all the RSUs.
EtotSum2 = list()
for ComputationResultSize in x2:
    EtotSum2.append(single_vehicle_energy(ComputationResultSize))
EtotSum1, EtotSum2 = Algorithm4InitializeWeights_2(EtotSum1,EtotSum2)
# Ticking values for x
x = [0,100,200,300,400,500,600,700]
# Resizing the graph
plt.figure(figsize=(5,3), dpi=300)
# Label helps us identify a line.
# Line number 1
plt.plot(x1,EtotSum1, label="Proposed (Single-tier)", color='red', linewidth =2, marker=".", markersize=10, linestyle="--")            # Takes 1 dimensional arrays as arguments.
plt.plot(x2,EtotSum2, label="Proposed (Two-tier)", color='yellow', linewidth =2, marker=".", markersize=10, linestyle="--")
plt.title("Fig. 3(b). Total energy consumption versus the computation result size of vehicle D1 in the single-tier and two-tier network.")        # Adding title to the graph
plt.xlabel("Computation Result Size, D1(MB)")               # Adding the X label
plt.ylabel("Total Energy consumption (J)")              # Adding the y label
plt.xticks(x)                       # To get rid of decimal points
# plt.yticks(y)                       # To get rid of decimal points
plt.legend()                        # Shows the legend, labels
plt.show()