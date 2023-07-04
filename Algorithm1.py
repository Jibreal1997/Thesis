"""
Author: Jibreal Khan
Email: jibrealkhan1997@gmail.com
Department: Electrical and Computer Engineering
Description: The following Algorithm implementation is part of my thesis at University of Ottawa.
"""

#-------------------------------------------------------Importing Libraries---------------------------------------------------------------------------#
import math
#import matplotlib.pyplot as plt

#------------------------------------------------------ System Model----------------------------------------------------------------------------------#
TotalVehicles      = 5
FMec               = 105                    # Overall computing resource of the MEC server (Ghz)
pc                 = 0.015                  # Computation resources of price coefficient of Cloud.
pm                 = 0.03                   # Computation resources of price coefficient of MEC
AIFS               = 0                      # The interval of arbitration inter-frame spacing
RTS                = 0                      # Request to send interval
θi                 = 0.6                      # The weight coefficient
γi                 = 312.5                    # Transmission Rate (2.5MbPs -> 312.5 KBps)
AvgVehicleV        = 33.3333                # The Average Vehicular velocity (120Km/h) converted to m/s
VehicleVariance    = 21                     # Variance of Vehicluar Velocity
RangeRSU           = 1                      # Range of RSU (km)
β                  = 0.1                    # Arrival Rate of Vehicles
TotalRSU           = 4                      # Total Number of RSUs
μv                 = AvgVehicleV            # Vehicular/Equivalent Speed (Calculate ???)

# Frequencies and System Utilities
Vpos               = [0.1, 0.25, 0.35, 1.1, 1.25]                                          # Position of Vehicles
VresourceMec       = [0, 0, 0, 0, 0]                                          # Computation resources MEC (fiMec)
VresourceCCC       = [0, 0, 0, 0, 0]                                          # Computation resources CCC (fiCCC)
VresourceLoc       = [10, 11, 12, 13, 14]                                          # Computation resources for LOC (filoc)
VsystemUtilityMec  = [0, 0, 0, 0, 0]                                          # System Utility MEC
VsystemUtilityCCC  = [0, 0, 0, 0, 0]                                          # System Utility CCC
VsystemUtilityLoc  = [0, 0, 0, 0, 0]                                          # System utility LOC
VsystemUtilityLocCCC = [0, 0, 0, 0, 0]                                        # System utility LOC,CCC

# Task related variables
VD                 = [10, 12, 14, 16, 18]                                     # Input Data sizes in Kb (Di)
VDout              = [10, 12, 14, 16, 18]                                          # Output Data sizes (Doi)
VH                 = [0.2, 0.25, 0.30, 0.35, 0.40]                            # Service Coefficient (GHz/KB)
VC                 = [0, 0, 0, 0, 0]                                          # Computation resource for Task GHz
Vθ                 = [0.8, 0.7, 0.6, 0.5, 0.6]                               # Weight Coefficient (Not sure of these values, not mention ???)
VΛ                 = [0, 0, 0, 0, 0]                                          # This is used in suboffloading Algorithim
TranmissionDelay   = 2 * math.pow(10, -6)                                                        # This is the tranmission delay from the RSU to the cloud
Vc                 = [0, 0, 0, 0, 0]                                          # This is used in sub-offloading algorithim

#Decisions
VDecisionLoc = [0,0,0,0,0]
VDecisionCCC = [0,0,0,0,0]
VDecisionMec = [0,0,0,0,0]
SΦ = list()
ST = []
Uupdate = [0,0,0,0,0]

# Timing sets
VTMax              = [0.2, 0.4, 0.6, 0.8, 1]                                  # Max delay Tolerance of Task (s)
VTM                = [0, 0, 0, 0, 0]                                          # Time Vehicle i left RSU m
VTSen              = [0, 0, 0, 0, 0]                                          # Actual delay tolerance of Task
VTMec              = [0, 0, 0, 0, 0]                                          # Total computational Time of Task in MEC
VTCCC              = [0, 0, 0, 0, 0]                                          # Total computational Time of Task in CCC
VTLoc              = [0, 0, 0, 0, 0]                                          # Total computational Time of Task in LOC

# Plotting
Plot1              = list()
Plot2SystemUtility = list()

#SubOffloading Specifc Variables
Normalize = 0.5                             # This Horizontal Beta value

#----------------------------------------------------------Algorithm Implementation---------------------------------------------------------------------#

def initialize():
  # Calcualtions for VTM
  for i in range(TotalVehicles):
    m = math.ceil(Vpos[i] / RangeRSU)
    VTM[i] = ((RangeRSU * m) - Vpos[i]) * 1000 / μv

  # Calculations for actual task delay tolerance (VTSen)
  for i in range(TotalVehicles):
    VTSen[i] = min(VTMax[i], VTM[i])

  # Calculation for Computing Resource (VC) required for Tasks
  for i in range(TotalVehicles):
    VC[i] = (VH[i] * VD[i])

  # Calculation for inital resource allocation for MEC server (VresourceMec), λ = 0
  for i in range(TotalVehicles):
      VresourceMec[i] = VC[i] + math.sqrt(VC[i]**2 - 4 * (1 + VTSen[i] - (VD[i] / γi)) *
                             (-(VC[i] * Vθ[i]) / ((1 - Vθ[i]) * pm))) / 2 * (1 + VTSen[i] - (VD[i] / γi))

  # Calculation for VΛ
  for i in range(TotalVehicles):
    VΛ[i] = 1 + VTSen[i] - (VD[i]/γi) - (VD[i] + VDout[i]) * TranmissionDelay

  # Calculation for Vc
  for i in range(TotalVehicles):
    Vc[i] = -(Vθ[i] * VC[i])/((1-Vθ[i]) * pc)

  # Calculation for VTLoc
  for i in range(TotalVehicles):
    VTLoc[i] = VC[i] / VresourceLoc[i]

  # Calculation for VTMec
  for i in range(TotalVehicles):
    VTMec[i] = (VC[i] / VresourceMec[i]) + (VD[i] / γi)

  # Calculation of the initial offloading strategy
  for i in range(TotalVehicles):
    SΦ.append([VDecisionLoc[i], VDecisionMec[i], VDecisionCCC[i]])

  print("SΦ",SΦ)
  print("VD",VD)
  print("VC", VC)
  print("Initial VresourceMec", VresourceMec)
  print("VTM",VTM)
  print("VTMax",VTMax)
  print("VTSen",VTSen)
  print("VTMec",VTMec)

#Function to update ST
def updateST(t):
  if len(ST) <= t:
    ST.append([])

  ST[t].clear()
  print("After clearing ST[0]", ST[t])
  #Calculation of the offloading strategy
  for i in range(TotalVehicles):
    ST[t].append([VDecisionLoc[i], VDecisionMec[i], VDecisionCCC[i]])

  print("ST[0]", ST[t])

# Implementing the BMACR algorithm (Sub Algorithm - 1)
# Bisection Method for Computation Resource Allocation
def BMACR(ε, λMin, λMax, λ, i, NumberOfIterations):
  # Bisection Search
  while (λMax - λMin) > ε:
    λ = (λMax + λMin) / 2
    VresourceMec[i] = VC[i] + math.sqrt(VC[i]**2 - 4 * (1 + VTSen[i] - (VD[i] / γi)) *
                             (-(VC[i] * Vθ[i]) / ((1 - Vθ[i]) * pm + λ))) / 2 * (1 + VTSen[i] - (VD[i] / γi))
    Plot1.append(VresourceMec[i])

    # Update λMax or λMin
    if sum(VresourceMec) < FMec:
      λMax = λ
    else:
      λMin = λ

    # For System Utility Plotting
    VsystemUtilityMec[i] = Vθ[i] * math.log(1 + max((VTSen[i] - VTMec[i]), 0)) - (1 - Vθ[i]) * pm * VresourceMec[i]
    Plot2SystemUtility.append(VsystemUtilityMec[i])
    NumberOfIterations += 1

  print("FrequencyAllocation: ", Plot1)
  print("System Utility: ", Plot2SystemUtility)
  print("Iterations: ", NumberOfIterations)

# Implementing the suboffloading Algortihm (Sub Algorithm - 2)
def SubOffloadingStrategy():
  for i in range(TotalVehicles):

    # Calculate cloud computing resource for that vehicle.
    # Why have we taken the absolute value here ?
    VresourceCCC[i] = (VC[i] + math.sqrt(VC[i]**2 - 4*VΛ[i]*Vc[i]))/2*VΛ[i]

    # Calculate tiloc
    VTLoc[i] = VC[i] / VresourceLoc[i]

    # Calculate uiloc
    Indicator = 1 if VTMax[i] < VTLoc[i] else 0
    VsystemUtilityLoc[i] = math.log(1 + max((VTMax[i]-VTLoc[i]), 0)) - (Indicator)

    # Calculate ticcc
    VTCCC[i] = (VD[i] / γi) + (VC[i]/VresourceCCC[i]) + (VD[i] + VDout[i]) * TranmissionDelay

    # Calculate uiccc
    VsystemUtilityCCC[i] = Vθ[i] * math.log(1 + max((VTSen[i] - VTCCC[i]), 0)) - (1 - Vθ[i]) * pc * VresourceCCC[i]


    # These if conditions are clealry wrong. Fix them.
    if VTMax[i] < VTLoc[i] and VTSen[i] < VTCCC[i]:
      VsystemUtilityLocCCC[i] = -float("infinity")
      VDecisionLoc[i] = 0
      VDecisionCCC[i] = 0
    else:
      if VsystemUtilityCCC[i] > VsystemUtilityLoc[i]:
        VDecisionCCC[i] = 1
        VDecisionLoc[i] = 0
      else:
        VDecisionLoc[i] = 1
        VDecisionCCC[i] = 0

    # Should this calculation really be after the for loop ? (Doubt)
    VsystemUtilityLocCCC[i] = (VDecisionLoc[i] * VsystemUtilityLoc[i]) + (VDecisionCCC[i] * VsystemUtilityCCC[i])

  print("VresourceCCC", VresourceCCC)
  print("VsystemUtilityCCC", VsystemUtilityCCC)
  print("VsystemUtilityLoc", VsystemUtilityLoc)
  print("VsystemUtilityLocCCC", VsystemUtilityLocCCC)
  print("VDecisionLoc", VDecisionLoc)
  print("VDecisionCCC", VDecisionCCC)

# Implementing the DCORA Algorithm (Main algorithm that calls the other two sub algorithms)
def DCORA():
  #--------------------------------------------------Initilization part--------
  #Getting Fmec* and Umec* via algorithm-1
  # BMACR Specific Variables
  ε = 1  # Max Tolerance
  λMin = 0  # Minima
  λMax = 20000000   # Maxima
  λ = 0  # Lagrange Multiplier
  NumberOfIterations = 0 # Counting Number of times the while loop runs
  # First Initialize the values that you are going to need
  initialize()
  for i in range(TotalVehicles):
    # Call the BMACR Algorithm for the vehicles
    #Fmec*
    BMACR(ε, λMin, λMax, λ, i, NumberOfIterations)

  #Umec*
  VsystemUtilityMec[i] = Vθ[i] * math.log(1 + max((VTSen[i] - VTMec[i]), 0)) - (1 - Vθ[i]) * pm * VresourceMec[i]

  #obtain stuff from Algorithm 2
  SubOffloadingStrategy()

  #----------------------------------------- First for loop ----------------
  #Based on what you got from algorithms 1 and 2 make some decision updates.
  t = 0
  for i in range(TotalVehicles):
    #if system utility of LocCCC is greater than Mec make decisions in its favour.
    if VsystemUtilityLocCCC[i] > VsystemUtilityMec[i]:
      VDecisionMec[i] = 0
      VDecisionCCC[i] = VDecisionCCC[i]
      VDecisionLoc[i] = VDecisionLoc[i]
    else:
      VDecisionMec[i] = 1
      VDecisionCCC[i] = 0
      VDecisionLoc[i] = 0
    updateST(t)

  # Incrementing t
  t = t + 1
  global SΦ
  #----------------------------------The outer while loop for the inner two loops
  while ST[t - 1] != SΦ:
    SΦ = ST[t - 1]
    i = 0

    # The first loop
    while i < TotalVehicles:
      # si' = siMec = 1, implicitly means that the other decision will be 0
      VDecisionMec[i] = 1
      VDecisionLoc[i] = 0
      VDecisionCCC[i] = 0

      # Based on the above modification we need to calculate Uupate(i), using algorithm 1 and 2
      BMACR(ε, λMin, λMax, λ, i, NumberOfIterations)  # Call to algorithm 1
      SubOffloadingStrategy()                         # Call to algorithm 2
      #Based on those calls we are getting something Uupdate.
      Uupdate[i] = VDecisionMec[i] * VsystemUtilityMec[i] + VDecisionCCC[i]*VsystemUtilityCCC[i] + VDecisionLoc[i]*VsystemUtilityLoc[i]
      i = i + 1

    ST.append([])
    print("ST",ST)
    #The second loop
    for i in range(TotalVehicles):
      # In both case we will be update the offloading strategy of the vehicle for ST
      if max(Uupdate) == Uupdate[i] or SΦ[i] == [0,1,0]:
        # Because it says si', I am assuming si' - simec
        ST[t].append([0,1,0])
      else:
        ST[t].append(ST[t- 1][i])

    t = t + 1
#-------------------------------------------------------------Running the Algorithms----------------------------------------------------------------------#
# Running the BMACR Algorithm alone
# # BMACR Specific Variables
# ε = 1  # Max Tolerance
# λMin = 0  # Minima
# λMax = 20000000   # Maxima
# λ = 0  # Lagrange Multiplier
# i = 0  # Doing it for Vehicle 1
# NumberOfIterations = 0 # Counting Number of times the while loop runs

# # First Initialize the values that you are going to need
# initialize()
# # Call the BMACR Algorithm for the first vehicles
# BMACR(ε, λMin, λMax, λ, i, NumberOfIterations)

# Running the DCORA Algorithim, which calls the BMACR and the Suboffloading Algorithm.
DCORA()