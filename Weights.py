def Algorithm4InitializeWeights_1(EtotSum1, EtotSum2):
  #Two-tier
  EtotSum1 = [0.5,0.55,0.6,0.7,1,1.1,1.3,1.6,1.9,2.2,2.8,3.8,4.0]
  #Single-tier
  EtotSum2 = [0.5,0.55,0.6,0.7,1,1.1,1.3,1.6,1.85,2.1,2.5,2.9,3.2,3.7]
  return EtotSum1,EtotSum2

def Algorithm4InitializeWeights_2(EtotSum1, EtotSum2):
  #Two-tier
  EtotSum1 = [0,0.1,0.2,0.3,0.4,0.55,0.7,2.1,3,4,6,8]
  #Single-tier
  EtotSum2 = [0,0.1,0.2,0.3,0.4,0.55,0.7,2.1,2.95,3.9,5,6.2,8]
  return EtotSum1,EtotSum2


def Algorithm5InitializeWeights_1(TotalDelay1, TotalDelay2):
  #Delay Minimization Algorithms
  TotalDelay1 = [0.25, 0.35, 0.45, 0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15]
  #Two Step Algorithm
  TotalDelay2 = [0.25, 0.35, 0.45, 0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15]
  return TotalDelay1, TotalDelay2

def Algorithm5InitializeWeights_2(EtotSum1, EtotSum2):
  #Delay Optimization
  EtotSum1 = [0.2,0.25,0.3,0.5,0.6,0.7,0.8,1,1.05,1.2,1.4,1.5,1.6,1.65,1.7,2,2.1]
  #Two Step Algorithm
  EtotSum2 = [0.2,0.23,0.27,0.4,0.45,0.5,0.6,0.65,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.35,1.4]
  return EtotSum1,EtotSum2