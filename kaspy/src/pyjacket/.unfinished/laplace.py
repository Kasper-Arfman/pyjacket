"""Determine if a signal(t) containts periodic components and/or exponential components"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import CZT
from scipy.fft import rfft, rfftfreq

def discrete_laplace_transform(signal, t):
    N = len(signal)
    s = np.zeros(N, dtype=complex)
    for i in range(N):
        for j in range(N):
            s[i] += signal[j] * np.exp(-t[i]*j*1j)
    return s



def fft_simple(t, yt):
    f = rfftfreq(len(yt), t[1] - t[0])
    yf = rfft(yt)
    return f, yf
    


t = np.linspace(0, 10, 400)
yt = 2 * np.sin(2 * np.pi * t* 4) ##* np.exp(-t * 2)


plt.plot(t, yt)
plt.show()


f, yf = fft_simple(t, yt)

plt.plot(f, np.abs(yf))
plt.show()

# print(s.shape)





# fig, axs = plt.subplots(2, 1, figsize=(8, 6))

# axs[0].plot(np.real(s), np.imag(s))
# axs[0].set_xlabel('Real')
# axs[0].set_ylabel('Imaginary')

# axs[1].plot(np.angle(s))
# axs[1].set_xlabel('Index')
# axs[1].set_ylabel('Phase')

# plt.tight_layout()
# plt.show()


# plt.show()