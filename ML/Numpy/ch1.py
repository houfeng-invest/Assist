# import scipy.misc
# import sys
# import matplotlib.pyplot as plt
# import numpy.testing
# import numpy as np


# lena = scipy.misc.ascent()
# print(lena.shape)
# LENA_X = 512
# LENA_Y = 512
# numpy.testing.assert_equal((LENA_X,LENA_Y),lena.shape)
# yfactor = 0.8
# xfactor = 0.8
# resized = lena.repeat(yfactor,axis=0).repeat(xfactor,axis=1)
# print(reversed)
# plt.subplot(211)
# plt.imshow(lena)
# # plt.subplot(212)
# # plt.imshow(reversed)
# plt.show()


#
# import numpy as np
# a = np.array([2,0,1,5])
# print(a)
# print(a[:3])
# print(a.min())


#
# from scipy.optimize import fsolve
# from scipy import integrate
# def f(x):
#     x1 = x[0]
#     x2 = x[1]
#     return [2*x1-x2**2-1,x1**2-x2-2]
#
# result = fsolve(f,[1,1])
# print(result)
#
#
# def g(x):
#     return (1-x**2)**0.5
# pi_2 ,err = integrate.quad(g,-1,1)



import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10,1000)
y = np.sin(x) + 1
z = np.cos(x**2) + 1

# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(8,4))
plt.plot(x,y,label="$\sin x+1$",color="red",linewidth=2)
plt.plot(x,z,'b--',label="$\cos x^2 + 1$")
plt.xlabel("Time(s)")
plt.ylabel("数")
plt.ylim(0,2.2)
plt.legend()
plt.show()

