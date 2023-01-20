import numpy as np
from numpy import absolute as abs, log
import matplotlib.pyplot as plt


T = 50                  # run time

alpha = 0.9             # fractional index

# for risk processes
u = 1000                # initial capital
c = 20                  # incoming capital per unit time

# for homogeneous process
lambda_rate = 4         # Poisson rate

# stable subordinator
def stable_subordinator():
    np.random.seed()
    U = np.random.random_sample(2)
    S = np.sin(alpha * np.pi * U[0]) * (np.sin((1 - alpha) * np.pi * U[0]))**(1 / alpha - 1)/(np.sin(np.pi * U[0])**(1 / alpha) * abs(log(U[1]))**(1 / alpha - 1))
    return S

# HPP
def hpp(T=T):
    # Initialise n = 0, t0 = 0;
    n = 0
    t = []
    while True:
        # Generate w ∼ Exp(lambda);
        w = np.random.exponential(1/lambda_rate)
        if n == 0:
            t.append(w)
        elif n > 0:
            t.append(t[n-1] + w)
        if t[n] > T:
            t = t[:-1]
            return t
        else:
            # Set n = n + 1
            n = n + 1

# plot function
def hpp_plot(T=T, runs=5):
    x_list = []
    y_list = []
    for i in range(runs):
        np.random.seed()
        x = hpp(T=T)
        x.append(T)
        y = list(range(0,len(x)+1))
        x = np.repeat(x,2)
        x = x.tolist()
        x.insert(0,0)
        x.append(T)
        y = np.repeat(y,2)
        x_list.append(x)
        y_list.append(y)
    plt.figure(figsize=(6, 4.5))
    for i in range(runs):
        plt.plot(x_list[i],y_list[i])
    plt.xlabel("time")
    plt.ylabel(r"$N^{\mu}(t)$")
    plt.xlim(0,50)
    plt.ylim(ymin=0)
    plt.show()
    
hpp_plot()