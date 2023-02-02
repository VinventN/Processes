import numpy as np
from numpy import absolute as abs, log
from scipy import optimize
import matplotlib.pyplot as plt

T = 50                  # run time

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

# NPP
def npp(T=T):
    # Initialize n = m = 0, t0 = s0 = 0, λ_bar = sup_{0≤t≤T} λ(t);
    m = 0
    n = 0
    t = [0]
    s = [0]
    lambda_bar = _lambda_bar()
    while s[m] < T:
        # Generate w ∼ Exp(lambda_bar);
        w = np.random.exponential(1/lambda_bar)
        # Set s(m+1) = s(m) + w;
        s.append(s[m] + w)
        # Generate D ~ uniform(0,1);
        D = np.random.uniform()
        if D <= (_lambda(s[m+1])/lambda_bar):
            t.append(s[m+1])
            n = n + 1
        m = m + 1
    # remove first 0 from list
    t.pop(0)
    # remove last element larger than T from list
    if len(t) != 0:
        t.pop()
    return t

# plot function
def npp_plot(T=T, runs=5):
    x_list = []
    y_list = []
    for i in range(runs):
        np.random.seed()
        x = npp(T=T)
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
    plt.ylabel(r"$NN^{\mu}(t)$")
    plt.xlim(0,50)
    plt.ylim(ymin=0)
    plt.show()
    
