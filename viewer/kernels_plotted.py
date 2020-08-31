import numpy as np
from matplotlib import pyplot as mp


def gaussian(r, epsilon):
    return np.exp(-(r/epsilon)**2)


def multicuadratic(r, epsilon):
    return np.sqrt((r / epsilon) ** 2 + 1)


def inverse(r, epsilon):
    return 1 / np.sqrt((r / epsilon) ** 2 + 1)


# def thin_plate(r, epsilon):
#    return r**2 * np.log(r)

r_values = np.linspace(-0.5, 0.5, 120)
for epsilon in [.1]:
    mp.plot(r_values, gaussian(r_values, epsilon))
    mp.plot(r_values, multicuadratic(r_values, epsilon))
    mp.plot(r_values, inverse(r_values, epsilon))
    # mp.plot(r_values, thin_plate(r_values, epsilon))

mp.axvline(x=0.1, ls=":", color='gray')
mp.axvline(x=-0.1, ls=":", color='gray')
mp.legend(['Gaussian [np.exp(-(r/epsilon)**2)]',
           'Multicuadratic [np.sqrt((r/epsilon)**2 + 1)]',
           'inverse [1/np.sqrt((r/epsilon)**2 + 1)]'], loc=2)
mp.xlabel("Distance [m]")
mp.ylabel("Score")
mp.show()
