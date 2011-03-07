import math
import numpy as np
import itertools as it
import xrdoptions as xopt

#bragg's law
#n*lambda = d*sin(theta)
#2*theta = 2*asin(n*lambda/d)
#n is part of d typically

class Material(object):
	def __init__(self,parameters):
		if hasattr(parameters,'__len__'):
			a,c = parameters
			f = lambda h,k,l:spectral_angle_hexagonal(a,c,h,k,l)
			self.spectral = f
		else:
			a = parameters
			f = lambda h,k,l:spectral_angle_cubic(a,h,k,l)
			self.spectral = f

a_indium_phosphide = Material(5.8687)
a_silicon = Material(5.43095)
a_gold = Material(4.080)
a_lead = Material(4.950)
a_aluminum = Material(4.05)
a_indium_oxide = Material(10.125)
a_silicon_dioxide = Material(5.8)

#[2002 J. Phys.: Condens. Matter 14 9579]
#1/d^2=(4/3)(h**2+hk+k**2/a**2)+l**2/c**2
w_indium_phosphide = Material((4.054,6.6625)) #a,c 

lambda_copper = 1.54 #angstroms

def reciprocal(a,b,c):
	bxc = np.cross(b,c)
	return 2*np.pi*(bxc/(np.dot(a,bxc)))

def d_hkl(h,k,l,a,b,c):
	astar_v = reciprocal(a,b,c)
	bstar_v = reciprocal(b,c,a)
	cstar_v = reciprocal(c,a,b)

def spectral_angle_cubic(a,h,j,k):
	d = a/math.sqrt(h**2+j**2+k**2)
	radian_angle = 2*math.asin(lambda_copper/d)
	return radian_angle *360/(2*math.pi)

def spectral_angle_hexagonal(a,c,h,k,l):
	inv_d2 = (4./3)*(h**2+h*k+k**2)/a**2 + (l/c)**2
	d=math.sqrt(1/inv_d2)
	radian_angle = 2*math.asin(lambda_copper/d)
	return radian_angle*360/(2*math.pi)

def spectrum_angles(mat):
	ranges = [range(0,4+1)]*3
	results = []
	for h,j,k in it.product(*ranges):
		try:
			results.append(((h,j,k),mat.spectral(h,j,k)))
		except ValueError as E:
			continue
		except ZeroDivisionError as E:
			continue
	return results

def uniq(alist,key=lambda x:x):	
	result = []
	keys =set()
	for x in alist:
		if key(x) not in keys:
			result.append(x)
			keys.add(key(x))
	return result
	
def sorted_spectrum(mat):
	return uniq(sorted(spectrum_angles(mat),
			key=lambda t:t[1]),
			key=lambda t:t[1])

for res,name in [(sorted_spectrum(x[0]),x[1]) for x in [ 
			(a_indium_phosphide,"InP"), 
			(a_silicon,"Si"), 
			(a_gold,"Au"), 
			(a_lead,"Pb"),
			(a_aluminum,"Al"),
			(a_indium_oxide,"In2O3"),
			(w_indium_phosphide,"InP (W)")]]:
	for angle in res:
		if xopt.start<=float(angle[1]) <= xopt.end:
			print angle,name

