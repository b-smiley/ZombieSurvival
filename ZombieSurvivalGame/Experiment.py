
from math import atan2, degrees,pi


rads = atan2(-100,50)
print(rads)
rads %= 2*pi
print(rads)

degs = degrees(rads)
print(degs)