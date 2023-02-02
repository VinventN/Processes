import numpy as np
from numpy import absolute as abs, log, exp
import matplotlib.pyplot as plt


T = 50                  # run time

alpha_1 = 0.9           # fractional index 1
alpha_2 = 0.5           # fractional index 2

# for homogeneous process
lambda_rate = 4         # Poisson rate

# for tempered process
c1 = 0.75
c2 = 1 - c1
tss_1 = 0.3
tss_2 = 0.7

# stable subordinator
def stable_subordinator():
    np.random.seed()
    U = np.random.random_sample(2)
    S = np.sin(alpha_1 * np.pi * U[0]) * (np.sin((1 - alpha_1) * np.pi * U[0]))**(1 / alpha_1 - 1)/(np.sin(np.pi * U[0])**(1 / alpha_1) * abs(log(U[1]))**(1 / alpha_1 - 1))
    return S

# Mixture Tempered FHPP
def mix_homo(tss_lambda, c, alpha, T=T):
    n = 0
    t = [0]
    x = [0]
    y = []
    while x[-1] < T:
        while True:
            np.random.seed()
            U = np.random.uniform()
            X = np.random.exponential(1 / lambda_rate)
            ss = stable_subordinator()
            ss_time = abs(X)**(1 / alpha)
            S = ss * ss_time
            if U <= exp(-tss_lambda * S):
                break
        S_t = S/c
        t.append(t[n] + S_t)
        n = n + 1
        x.append(x[-1] + ss_time / c)
        y.append(ss * c)
    if len(t) != 0:
        t.pop(0)
        t.pop()
        x.pop(0)
    return t, x, y

def mtfhpp(tss_1=tss_1, tss_2=tss_2, c1=c1, c2=c2, T=T, alpha_1=alpha_1, alpha_2=alpha_2):
    S_1, x1, y1 = mix_homo(tss_lambda=tss_1, c=c1, alpha=alpha_1, T=T)
    S_2, x2, y2 = mix_homo(tss_lambda=tss_2, c=c2, alpha=alpha_2, T=T)
    S_2.pop(0)
    S = S_1 + S_2
    S.sort()
    x = x1 + x2
    y = y1 + y2
    zipped = zip(x, y)
    zipped_sorted = sorted(zipped)
    zipped_list = list(zip(*zipped_sorted))
    x_sorted = list(zipped_list[0])
    y_sorted = list(zipped_list[1])
    x_plot = [0]
    y_plot = [0]
    n = 0
    while True:
        x_plot.extend([x_plot[-1] + x_sorted[n], x_plot[-1] + x_sorted[n]])
        y_plot.extend([y_plot[-1], y_plot[-1] + y_sorted[n]])
        n += 1
        if y_plot[-1] > T:
            break
    return S, x_plot, y_plot


def mtfhpp_plot(T=T, runs=5):
    x_list = []
    y_list = []
    for i in range(5):
        while True: # only for plotting purpose, to ensure that the graph will have lines across the graph
            np.random.seed()
            result = mtfhpp(T=T)
            x, y = result[1], result[2]
            x_list.append(x)
            y_list.append(y)
            if max(x) >= T:
                break
    plt.figure(figsize=(6, 4.5))
    for i in range(runs):
        plt.plot(x_list[i], y_list[i])
    plt.xlabel("time")
    plt.ylabel(r"$Z_{m}(t)$")
    plt.xlim(0,T)
    plt.ylim(ymin=0)
    plt.show()
