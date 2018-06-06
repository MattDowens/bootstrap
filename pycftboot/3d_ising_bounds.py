from bootstrap import *

dim=3
k_max=20
l_max=14
n_max=4
m_max=2

table1=ConformalBlockTable(dim,k_max,l_max,m_max,n_max)
table2=ConvolvedBlockTable(table1)

lower=0.7
upper=1.7
tol=0.01
channel=0

def find_bounds():
	dim_phi=0.5
	bounds=[]
	if dim_phi<=0.8:
		sdp=SDP(dim_phi,table2)
		result=sdp.bisect(lower,upper,tol,channel)
		bounds.append([dim_phi,result])
		dim_phi+=0.001
	return bounds




