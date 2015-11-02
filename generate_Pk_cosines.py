#!/usr/bin/python
import sys
from math import exp
import numpy as np
# README:
#
# This is an example python script for the external_Pk mode of Class.
# It generates the primordial spectrum of LambdaCDM.
# It can be edited and used directly, though keeping a copy of it is recommended.
#
# Two (maybe three) things need to be edited:
#
# 1. The name of the parameters needed for the calculation of Pk.
#    "sys.argv[1]" corresponds to "custom1" in Class, an so on
a=np.zeros(5)
try :
    a[0]           = float(sys.argv[1])
    a[1]           = float(sys.argv[2])
    a[2]           = float(sys.argv[3])
    a[3]           = float(sys.argv[4])
    a[4]           = float(sys.argv[5])

# Error control, no need to touch
except IndexError :
    raise IndexError("It seems you are calling this script with too few arguments.")
except ValueError :
    raise ValueError("It seems some of the arguments are not correctly formatted. "+
                     "Remember that they must be floating point numbers.")

A=2.41e-9
k_0=.05
n_s=.972
# 3. Limits for k and precision:
#    Check that the boundaries are correct for your case.
#    It is safer to set k_per_decade primordial slightly bigger than that of Class.

k_min  = 1.e-6
k_max  = 10.
k_per_decade_primordial = 200.

# 2. The function giving P(k), including the necessary import statements.
#    Insid
def P(k) :
    p=(k/k_0)**(n_s-1.)
    for i in range(5):
        p=p+a[i]*np.cos(np.log(k/k_0)*2*np.pi*(i+1)/7/np.log(10))
    return p*A

#
#
# And nothing should need to be edited from here on.
#

# Filling the array of k's
ks = [float(k_min)]
while ks[-1] <= float(k_max) :
    ks.append(ks[-1]*10.**(1./float(k_per_decade_primordial)))

# Filling the array of Pk's
for k in ks :
    P_k = P(k)
    print "%.18g %.18g" % (k, P_k)

