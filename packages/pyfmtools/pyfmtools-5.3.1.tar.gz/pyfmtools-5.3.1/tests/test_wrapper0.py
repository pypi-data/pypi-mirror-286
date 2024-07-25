import numpy as np
import pyfmtools as fm
import random
import sys




n=7
env=fm.fm_init(n)
num=1
v= fm.generate_fm_minimals(num, n, 100, 0.35, env)
print(v)

num=1
le= fm.generate_fm_minimals_le(num, n, 100, 0.35, env)
print(le)


step=0.001
Fn=None
Option=0
ret_code, v, len = fm.generate_fm_randomwalk(2, n, 3,10 , Option, step, env, Fn)
print("Random walk")
print(v)
A = fm.ShowCoalitions( env)
#for k in range(64) :
#    print(v[k], A[k],k)
print(ret_code)


fm.fm_free(env)