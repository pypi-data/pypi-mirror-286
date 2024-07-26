# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:23:08 2024

@author: Peter
"""
#from . import __flatchain__,__rng__
import numpy as np
import scipy

from pathlib import Path



rng = np.random.default_rng()

chainpath=Path(__file__).parent/ 'chain4b.txt'
flatchain=np.genfromtxt(chainpath.open())

uncpath=Path(__file__).parent/ 'ErrorsBigList.dat'
PrhoUnc=np.genfromtxt(uncpath.open())
PrhoUncsplines=scipy.interpolate.interp1d(PrhoUnc[:,0],PrhoUnc[:,1:],axis=0)

__all__=["get_Rsamp","get_Psamp","get_Psamp_Unc"]


#print("haha")

def MRddo(m,rho):
    a= -0.492
    mu = np.sqrt(1-m)
    mu2=1-m
    c=0.8284271247461903
    return 1+mu*(a+c*rho) + mu2*(-2.-np.sqrt(2)*a+c*rho)



def get_Rsamp(M,Nsamp=1):
     sel=flatchain[:,3]>M
     chain_sel=rng.choice(flatchain[sel],size=Nsamp)

     Rs=chain_sel[:,4]*MRddo(M/chain_sel[:,3],chain_sel[:,2])
     return Rs

def fddo(pmax,rhomax,vec):
    (a,b,c,d)=vec
    return c*(pmax**a)*(rhomax**b)+d

vecM=[1.4092,-1.3914,5.8621,0.27259]
vecR=[0.5182,-0.5937,2.744,-0.07410]
vecc=[0.764,-0.780,3.27,0.187]    
    
def gamma_ddo(pmax,rhomax):
    return fddo(pmax,rhomax,vecc)/fddo(pmax,rhomax,vecR)

def relPhigh(relrho,pmax,rhomax):
    gamma=gamma_ddo(pmax,rhomax)
    zeta=np.sqrt(pmax/rhomax)*gamma
    a0=-0.392;b0=-0.869;b1=1.69;p=2.98
    
    return (relrho**(gamma**2-a0))/(1+a0*(1-relrho)+(b0+b1*zeta)*(1-relrho)**p)

def Pddo(rho,pmax,rhomax,r12):

    relrho=rho/rhomax
    Phigh=pmax*relPhigh(relrho,pmax,rhomax)

    u0=-61.2;u1=81.9; u2=-27.2; v=1.33

    return Phigh*np.exp((u0+u1*r12+u2*r12**2)*(np.exp(-v*rho)- np.exp(-v*rhomax)))

def get_Psamp(rho,Nsamp=1):
    
    sel=flatchain[:,1]>rho
    chain_sel=rng.choice(flatchain[sel],size=Nsamp)
    Ps=Pddo(rho,chain_sel[:,0],chain_sel[:,1],chain_sel[:,2])
    
    
    return Ps

def get_Psamp_Unc(rho,Nsamp=1):
    

    sel=flatchain[:,1]>rho
    chain_sel=rng.choice(flatchain[sel],size=Nsamp)
    Ps=Pddo(rho,chain_sel[:,0],chain_sel[:,1],chain_sel[:,2])
    
    relrhomaxes=(rho-1.)/(chain_sel[:,1]-1.)

  
    BoostUnc=np.apply_along_axis(rng.choice,1,PrhoUncsplines(relrhomaxes))
    Ps=Ps*(1+BoostUnc)

   # print(BoostUnc)
    
    return Ps

