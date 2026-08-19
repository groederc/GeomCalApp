import numpy as npy
import math
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#           Funciones para el cálculo de propiedades geométricas
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def auxiliares(x,y):
    n = len(x)
    sx = npy.zeros(n)
    sy = npy.zeros(n)
    dx = npy.zeros(n)
    dy = npy.zeros(n)
    for i in range(n):
        if i == n-1:
            sx[i] = x[0] + x[i]
            dx[i] = x[0] - x[i]
            sy[i] = y[0] + y[i]
            dy[i] = y[0] - y[i]
        else:
            sx[i] = x[i+1] + x[i]
            dx[i] = x[i+1] - x[i]
            sy[i] = y[i+1] + y[i]
            dy[i] = y[i+1] - y[i]
    return sx,sy,dx,dy
# ------------------------------------------------------------------------
def calculaArea(x,y):
    n = len(x)
    sx,_,_,dy = auxiliares(x,y)
    suma = 0.0
    for i in range(n):
        suma += sx[i]*dy[i]
    return 0.5*suma
# ------------------------------------------------------------------------
def calculaCentroGeometrico(x,y):
    n = len(x)
    sx,sy,dx,dy = auxiliares(x,y)
    Area = calculaArea(x,y)
    sgx = 0.0
    sgy = 0.0
    for i in range(n):
        sgx += dy[i]*(sx[i]*sx[i] + dx[i]*dx[i]/3.0)
        sgy += dx[i]*(sy[i]*sy[i] + dy[i]*dy[i]/3.0)
    Xg = sgx/(8.0*Area)
    Yg =-sgy/(8.0*Area)
    return Xg,Yg
# ------------------------------------------------------------------------
def calculaProductodeInercias(x,y):
    sixy = 0.0
    n = len(x)
    _,sy,dx,dy = auxiliares(x,y)
    for i in range(n):
        if i == n-1:
            sixy += dy[i]*(x[i]*x[i]*sy[i]/2.0 + 
                    dx[i]*(x[0]*y[i] + 
                    2.0*x[i]*y[0])/3.0 + 
                    dy[i]*dx[i]*dx[i]/4.0);
        else:
            sixy += dy[i]*(x[i]*x[i]*sy[i]/2.0 +
                    dx[i]*(x[i+1]*y[i] + 
                    2.0*x[i]*y[i+1])/3.0 + 
                    dy[i]*dx[i]*dx[i]/4.0)
    Ixy = sixy/2.0
    return Ixy
# ------------------------------------------------------------------------
def calculaInercias(x,y):
    six = 0.0
    siy = 0.0
    n = len(x)
    sx,sy,dx,dy = auxiliares(x,y)
    for i in range(n):
        six += dx[i]*sy[i]*(sy[i]*sy[i] + dy[i]*dy[i])
        siy += dy[i]*sx[i]*(sx[i]*sx[i] + dx[i]*dx[i])
    Ix  =-six/24.0
    Iy  = siy/24.0
    Ixy = calculaProductodeInercias(x,y)
    return Ix,Iy,Ixy
# ------------------------------------------------------------------------
def calculaPropiedadesCentroidales(x,y):
    Area  = calculaArea(x,y)
    Xg,Yg = calculaCentroGeometrico(x,y)
    Ix,Iy,Ixy = calculaInercias(x,y)
    Ixg  = Ix - Area*Yg*Yg
    Iyg  = Iy - Area*Xg*Xg
    Ixyg = Ixy - Area*Xg*Yg
    return Area,Xg,Yg,Ix,Iy,Ixy,Ixg,Iyg,Ixyg
# ------------------------------------------------------------------------
def calculaInerciasPrincipales(Ix,Iy,Ixy):
    pi    = npy.pi
    v1    = -2.*Ixy
    v2    = Ix - Iy
    phi   = 0.
    Imax  = Ix
    Imin  = Iy

    if abs(Ixy)<=1.0E-10:
        return phi,Imax,Imin

    c     = 0.5*(Ix + Iy)
    d     = 0.5*(Ix - Iy)
    R     = math.sqrt(d**2. + Ixy**2.)
    Imax  = c + R
    Imin  = c - R

    if abs(v2) <=1.0E-10:
        if v1 >= 0. and v2 >= 0.: phi = 45.
        elif v1 >= 0. and v2 <= 0.: phi = 135.
        elif v1 <= 0. and v2 <= 0.: phi = 225.
        elif v1 >= 0. and v2 <= 0.: phi = 315.
    else:
        t    = v1/v2
        phi  = math.atan(t)*90./pi

    return phi,Imax,Imin
# -------------------------------------------------------------------------