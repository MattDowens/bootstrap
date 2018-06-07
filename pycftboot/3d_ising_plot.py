import bootstrap
import matplotlib.pyplot as plt

bootstrap.cutoff=1e-10
dim=3
k_max=20
l_max=15
n_max=4
m_max=2

def find_bounds(table1,table2,lower,upper,tol,channel):
    dim_phi=0.5
    x=[]
    y=[]
    while dim_phi<0.6:
        sdp=bootstrap.SDP(dim_phi,table2)
        result=sdp.bisect(lower,upper,tol,channel)
        x.append(dim_phi)
        y.append(result)
        dim_phi+=0.002
    plt.plot(x,y)

tab1=bootstrap.ConformalBlockTable(dim,k_max,l_max,m_max,n_max)
tab2=bootstrap.ConvolvedBlockTable(tab1)

l=0.9
u=1.7
t=0.01
c=0

find_bounds(tab1,tab2,l,u,t,c)

plt.xlabel('$\Delta_{\sigma}$')
plt.ylabel('$\Delta_{\epsilon}$')
plt.show()