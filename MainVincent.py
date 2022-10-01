import numpy as np

pi = np.pi

"Calcul K pour le filtre afin d'avoir un gain de -3dB a pi/1000"
K = 1
w = pi/1000
gainFinal = 0.707106 #-3dB en amplitude
gain = 1

while not (gainFinal-0.001 < gain < gainFinal+0.001):
    gain = (1/K)*np.sin(w*K/2)/np.sin(w/2)
    print(f"K : {K}")
    print(f"Gain : {gain}")
    K += 1
print(K)