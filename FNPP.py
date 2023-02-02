import numpy as np
from numpy import absolute as abs, log
from scipy import optimize
import matplotlib.pyplot as plt

T = 50                  # run time

alpha = 0.9             # fractional index

# for nonhomogeneous process
# Weibull's model
gamma = 0.9
beta = 0.2

# intensity function
def _lambda(t):
    return gamma/beta * (t/beta) ** (gamma-1)

# integral of intensity function
def integral_lambda(t):
    return (t/beta)**c

# max value of intensity function (to be used in thinning algorithm)
def _lambda_bar():
    t_lambda_bar = optimize.fminbound(lambda t: -_lambda(t), 0, T)
    lambda_bar = _lambda(t_lambda_bar)
    return lambda_bar

# stable subordinator
def stable_subordinator():
    np.random.seed()
    U = np.random.random_sample(2)
    S = np.sin(alpha * np.pi * U[0]) * (np.sin((1 - alpha) * np.pi * U[0]))**(1 / alpha - 1)/(np.sin(np.pi * U[0])**(1 / alpha) * abs(log(U[1]))**(1 / alpha - 1))
    return S

# FNPP
def fnpp(T=T, alpha=alpha):
    m = 0
    n = 0
    t = [0]
    s = [0]
    x = [0]
    y = [0]
    lambda_bar = _lambda_bar()
    while x[-1] < T:
        np.random.seed()
        ss = stable_subordinator()
        X = np.random.exponential(1 / lambda_bar)
        ss_time = abs(X)**(1 / alpha)
        S_t = ss * ss_time
        s.append(s[-1] + S_t)
        x.extend([x[-1] + ss_time, x[-1] + ss_time])
        y.extend([y[-1], y[-1] + S_t])
        V = np.random.uniform()
        if V <= (_lambda(s[-1])/lambda_bar):
            t.append(s[-1])
            n = n + 1
        m = m + 1
    if len(t) != 0:
        t.pop(0)    # as there is no event at t = 0
        x = [n for n in x if n <= T]    # copying the time of events
        y = y[0:len(x)] # counting the number of events
    return t, x, y

# plot function
def fnpp_plot(T=T, runs=5):
    x_list = []
    y_list = []
    for i in range(5):
        np.random.seed()
        result = fnpp(T=T)
        x, y = result[1], result[2]
        x.append(T)
        y.append(y[-1])
        x_list.append(x)
        y_list.append(y)
    plt.figure(figsize=(6, 4.5))
    for i in range(runs):
        plt.plot(x_list[i],y_list[i])
    plt.xlabel("time")
    plt.ylabel(r"$NN_{\alpha}(t)$")
    plt.xlim(0,50)
    plt.ylim(ymin=0)
    plt.show()
    
