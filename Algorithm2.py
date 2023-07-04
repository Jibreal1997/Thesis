"""
Author: Jibreal Khan
Email: jibrealkhan1997@gmail.com
Department: Electrical and Computer Engineering
Description: The following Algorithm implementation is part of my thesis at University of Ottawa.
"""
#---------------------------------------------------------Importing Libraries ------------------------------------------------------------#
import math
import matplotlib.pyplot as plt
import numpy as np

#-------------------------------------------------------- System Model---------------------------------------------------------------------#
P = 31.622776601683793  # RSU max transmission power limit (converted to watts)
F = 1 * math.pow(10, 9)  # RSU CPU max frequency limit (Hz)

#Vehicle related Variables
v = []  # Velocity of the Vehicle (m/s)
Rreq = 300  # Distance of task offload from 1st RSU (meters)

# Task related Variables
Ccpu = 0 # Size of the workload in number of CPU cycles
x = []  # Ratio of the kth subtask allocated to RSU
xOpt = []  # Optimal task splitting
tcpX = []  # Computation time for a given workload at a given RSU
EcpX = []  # Computation enery consumption for computing a given workload at given RSU
EcpXSemi = []  # Semi optimal Computation energy consumption for computing a given workload
EcpXOpt = []  # Optimal computation energy consumption for computing a given workload
EtotSemi = []  # Semi optimal total energy consumption
EtotOpt = []  # Optimal Total computation energy
EnergyTotal = [] # Total Energy Consumtion by all RSUs for a give size of data.

# Network related Variables
K = [] # Set of RSUs
M = 1  # Transmit Antennas in each RSU
# Pbs = [55] * TotalRSU  # Base station max transmission power limit (dBm)
# Fbs = [1.2 * math.pow(10, 9)] * TotalRSU  # Base station max frequency limit (Hz)
# Rbs = [600] * TotalRSU  # Length of the road segment covered by Base Station.
B = 5 * math.pow(10, 6)  # Bandwidth used by RSU (Hz)
p = []  # RSU transmission power allocation
pOpt = []  # RSU optimal transmission power allocation for optimal task dist.
pOptWatt = []  # RSU optimal transmission power allocation in Watt
f = []  # RSU CPU frequency allocation
fopt = []  # RSU optimal CPU frequency allocation
y = []  # The received signal of the vehicle from the RSU
l = 500  # Maximum link length within RSU coverage area
θ = 0.95  # Successful Transmission Probability (STP)
κ = math.pow(10, -11)  # Effective switched capacitance (>= 0)
ϕ = 3 # Positive constant (>= 1)

# Variables related to transmission
α = 4  # Path loss exponent
#No = 80
No = 1 * math.pow(10,-11)  # We do not know what this is (decibel milliwatts) (converted to watts)
s = []  # Information symbol
w = []  # Normalized beamforming vector
h = []  # Vector channel
z = 0  # Complex Gaussian Noise
C = []  # Average data rate of RSU to transmit.
tcm = []  # Transmission time in a given RSU
Ecm = []  # Energy consumption during transmission
EcmSemi = []  # Energy consumption during Transmission fewer constraints
EcmOpt = []  # Optimal energy consumption during Transmission.
SNR = {}  # Signal to Noise ratio
Cmax = {}  # Maximum achievable data rate
γOpt = 0  # No idea what this is

#---------------------------------------------------------------- Algorithm Implementation -------------------------------------------------------------
def H(x, l, θ, R, ϕ, κ):
  return (((Dbit * No * math.pow(l, α) * math.log(2)) / (B * GInv(θ))) *
          math.pow(2, (x * v) /
                   (R * B))) + (math.pow(x,
                                         (ϕ - 1)) * ϕ * Ccpu * κ) * math.pow(
                                           ((v * Ccpu) / (Rreq + sum(R[:-1]))),
                                           (ϕ - 1))


def HInv(γOpt):
  return float("infinity")

def TotalEnergyConsumption():
  EnergyTotal.append(sum(EtotOpt))

"""
Function to compute OptimalTask Distribution, Optimal Power Allocation, Optimal CPU Freuqency Allocation,
Optimal Communication Time Allocation, Optimal Total Energy Consumption
"""
def optimalSolution(Dbit = 8 * math.pow(10, 8), v = 27.7778, TotalRSU = 20):
  #Performing initial calcualtions
  Ccpu = 1000 * Dbit
  R =  [400] * TotalRSU  # Length of interval of road covered by RSU

  for i in range(TotalRSU):
    # Optimal (xOpt) Task allocation ratio
    choice1 = 0
    choice2 = (((R[i] * B) / (Dbit * v)) * math.log2(((P * math.log(1 / θ)) / (No * math.pow(l, α))) + 1))
    choice3 = (((F) / (v * Ccpu)) * (Rreq + sum(R[:i])))
    choice4 = HInv(γOpt)
    xOpt.append(max(choice1, min(choice2, choice3, choice4)))
    # print(choice1, choice2, choice3, choice4)

    #Optimal (pOpt) Power allocation
    pOpt.append(((No * math.pow(l, α)) / math.log(1 / θ)) *
                (math.pow(2, ((Dbit * xOpt[i]) * v) / (R[i] * B)) - 1))
    pOptWatt.append(math.pow(10, (pOpt[i] - 30) / 10))
    #print(f"Optimal Power: {pOpt[i]}")

    #Optimal (fopt) CPU Frequency allocation
    fopt.append(((v * (Ccpu * xOpt[i])) / (Rreq + sum(R[:i]))))
    #print(f"Optimal Frequency: {fopt[i] / math.pow(10,9)} Ghz")

    #Optimal (tcm) Communication Time Allocation
    tcm.append((Dbit * xOpt[i]) / (B * math.log2(1 + (
      (pOptWatt[i] * math.pow(l, -α)) / No) * math.log(1 / θ))))
    #print(f"Optimal Time: {tcm[i]}")

    #Optimal energy (EcmOpt) consumption during communication
    EcmOpt.append(((Dbit * xOpt[i]) * pOptWatt[i]) / (B * math.log2(1 + (
      (pOptWatt[i] * math.pow(l, -α)) / No) * math.log(1 / θ))))
    #print(f"Communication Energy: {EcmOpt[i]}")

    #Optimal energy (EcpXOpt) consumtion during computation
    EcpXOpt.append(
      math.pow(xOpt[i], ϕ) * Ccpu * κ * math.pow(
        ((v * Ccpu) / (Rreq + sum(R[:i]))), ϕ - 1))
    #print(f"Computation Energy: {EcpXOpt[i]}")

    # Optimal total energy (EtotOpt) consumption
    EtotOpt.append(EcmOpt[i] + EcpXOpt[i])
    #print(f"Total Energy: {EtotOpt[i]}")

  # Once the optimal energy for each RSU is achieved sum them all.
  TotalEnergyConsumption()



def Plots(Qty1, EnergyTotal):
  # ax.set_title('Optimal Total Energy Consumption for K = 40')
  plt.rcParams['figure.figsize'] = (9, 6)
  plt.xlabel("Qty1")
  plt.ylabel("Total Energy Consumption")
  plt.title("Total Energy Consumtion")
  plt.plot(Qty1, EnergyTotal)

#---------------------------------------------------------------------------- Generation of plots -------------------------------------------------------

# Generation of Total Energy consumption vs Data Size
# For each call the size of the data needs to be modified.
# Size of the computation result in MB 1,50,100,150,200,250,300,350
Dbit = [4 * math.pow(10, 8), 8 * math.pow(10, 8), 1.2 * math.pow(10,9), 1.6 * math.pow(10,9), 1.75 * math.pow(10,9), 2 * math.pow(10,9), 2.2 * math.pow(10,9), 2.4 * math.pow(10,9),2.6 * math.pow(10,9), 2.8 * math.pow(10,9), 3 * math.pow(10,9), 3.2 * math.pow(10,9), 3.4 * math.pow(10,9), 3.6 * math.pow(10,9), 3.8 * math.pow(10,9), 4.0 * math.pow(10,9)]
v = 27.777
TotalRSU = 20
for dataSize in Dbit:
  optimalSolution(dataSize, v, TotalRSU)
print(len(Dbit),len(EnergyTotal))
Plots(Dbit,EnergyTotal)
print(Dbit)
print(EnergyTotal)

# Generating plot for Total Energy Consumption vs Vehicular Speed
# For each call the speed of the Vehicular Velocity needs to be modified.
v = [11.1111, 16.6667, 22.2222, 27.7778, 33.3333, 38.8889, 44.4444, 50, 55.5556]
Dbit = 2 * math.pow(10,9)
TotalRSU = 20
EnergyTotal = []
for velocity in v:
  optimalSolution(Dbit,velocity,TotalRSU)
print(len(v),len(EnergyTotal))
Plots(v,EnergyTotal)
print(v)
print(EnergyTotal)

# Generating plot for total Energy Consumption vs Total RSUs
# For each call the Total Number of RSUs need to be modified.
K = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
v = 27.7778
Dbit = 2 * math.pow(10,9)
EnergyTotal = []
for TotalRSU in K:
  optimalSolution(Dbit,v,TotalRSU)
print(len(K), len(EnergyTotal))
Plots(K,EnergyTotal)
print(K)
print(EnergyTotal)