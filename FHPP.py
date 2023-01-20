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

# FHPP
def fhpp_ss(T=T, alpha=alpha):
    _lambda = lambda_rate
    n = 0
    t = [0]
    x = [0]
    y = [0]
    while x[-1] < T:
        np.random.seed()
        ss = stable_subordinator()
        X = np.random.exponential(1 / _lambda)
        ss_time = abs(X)**(1 / alpha)
        S_t = ss * ss_time
        t.append(t[n] + S_t)
        n = n + 1
        x.extend([x[-1] + ss_time, x[-1] + ss_time])
        y.extend([y[-1], y[-1] + S_t])
    if len(t) != 0:
        t.pop(0)        # as there is no event at t = 0
        t.pop()         # as the final event happen after the desired timeframe
        x = [n for n in x if n <= T]    # copying the time of events
        y = y[0:len(x)] # counting the number of events
    return t, x, y

# plot function
def fhpp_plot(T=T, runs=5):
    x_list = []
    y_list = []
    for i in range(5):
        np.random.seed()
        result = fhpp_ss(T=T)
        x, y = result[1], result[2]
        x.append(T)
        y.append(y[-1])
        x_list.append(x)
        y_list.append(y)
    plt.figure(figsize=(6, 4.5))
    for i in range(runs):
        plt.plot(x_list[i],y_list[i])
    plt.xlabel("time")
    plt.ylabel(r"$N_{\alpha}(t)$")
    plt.xlim(0,50)
    plt.ylim(ymin=0)
    plt.show()

fhpp_plot()