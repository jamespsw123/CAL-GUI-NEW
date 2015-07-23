import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(5.0, 10.0, 0.02)
t3 = np.arange(10.0, 15.0, 1)

plt.figure(1)
plt.plot([.5, .6],[1.0,1.1])

plt.plot([.6, .7],[1.2,1.2])

plt.plot([.7, .8],[1.3,1.3])
plt.show()