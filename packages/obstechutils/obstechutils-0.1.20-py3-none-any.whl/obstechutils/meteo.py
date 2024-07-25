from __future__ import annotations

from scipy.integrate import trapezoid
from astropy.coordinates import EarthLocation
from astropy.table import Table
from astropy.time import Time
from astroquery.utils.tap.core import TapPlus
from astropy.table import Table

import numpy as np
from numpy import cos, sin
from typing import Union

from .types import TypeAlias

Vector: TypeAlias = Union[float, list[float], np.ndarray]

def saturated_vapour_pressure(
    T: Vector,          # m 
    P: Vector = 1013.25 # hPa
) -> Vector:            # hPa

    """Ps = saturated_vapour_pressure(T, P)

Arguments
    T - temperature (⁰C)
    P - pressure (hPa)
    Ps - saturated vapour pressure (hPa)

See "New Equations for Computing Vapor Pressure and Enhancement Factor", 
Journal of Applied Meteorology and Climatology, 20, 12, 1527-1532, using
ew6 and ei3 from Table 2, and fw3 and fi3 from Table 3. Error <~ 0.1% 
in the range -50 to +50 ⁰C.

    """

    # ensure same array size and atleast 1D.  Keep track of masked
    # data.

    scalar = np.ndim(T) == 0 and np.ndim(P) == 0
    if scalar:
        T = np.atleast_1d(T)
    t, p  = np.broadcast_arrays(T, P)

    mask = getattr(T, 'mask', False) * getattr(P, 'mask', False)

    Ps = np.empty_like(t)

    # Arden Buck equation over liquid (water) and solid (ice)
    #
    # See Buck (1981), "New Equations for Computing Vapor Pressure and 
    # Enhancement Factor", Journal of Applied Meteorology and Climatology,
    # 20, 12, 1527-1532.
    #
    # Coefficients a, b, c, d: ew6, ei3 from Table 2 
    # Coefficients A, B, C: fw3, fi3 from Table 3
    #
    # Errors in tropospheric conditions are <~ 0.05% for both in temperature
    # ranges found in the Atacama, resulting in a <0.1% error.

    # over liquid
    a = 6.1121 # hPa
    b = 18.564
    c = 255.57 # ⁰C
    d = 254.4 # ⁰C
    A = 7.2e-4
    B = 3.2e-6
    C = 5.9e-10

    liq = t >= 0.01
    tl = t[liq]
    pl = p[liq]
    ef =  1 + A + pl * (B + C * tl**2)
    Ps[liq] = a * ef * np.exp((b - tl / d) * tl / (c + tl))
   
    # over solid 
    a = 6.1115 # hPa
    b = 23.036
    c = 279.82 # ⁰C
    d = 333.7 # ⁰C
    A = 2.2e-4
    B = 3.2e-6
    C = 6.4e-10

    sol = t < 0.01
    ts = t[sol]
    ps = p[sol]
    ef =  1 + A + ps * (B + C * ts**2)
    Ps[sol] = a * ef * np.exp((b - ts / d) * ts / (c + ts))
    
    if scalar:
        return Ps[0]

    if mask is False:
        return Ps

    return np.ma.masked_array(Ps, mask)

def absolute_humidity(
    P: Vector, # hPa 
    T: Vector, # ⁰C
    h: Vector  # %
) -> Vector:   # kg/m³ 
    """ρ = absolute_humidity(P, T, h)

Arguments
    P - pressure [hPa]
    T - temperature [⁰C]
    h - humidity [%]
    ρ - mass density of water vapour [kg/m³]

"""
    Ps = 1e2 * saturated_vapour_pressure(T, P=P)
    P = h / 100 * Ps

    R = 461.5 # J/K/kg 
    ρ = P / (R * (T + 273.15))

    return ρ # kg/m³

def zwd_to_pwv_factor(
    Tm: Vector # ⁰C
) -> Vector: 
    """Π = zwd_to_pwv_factor(Tm)

    Conversion factor from zenithal wet delay to precipitable water vapour
using the humidity weighted average tropospheric temperature Tm [⁰C].  It 
should be close to 0.15 in pretty much any observatory.

    """
    ρ = 1000 # kg/m³
    R = 461 # J/kg/K
    k3 = 3.7e5 # K²/hPa
    k2 = 22 # K/hPa

    Π = 1e8 / (ρ*R*(k3 / (273.15 + Tm) + k2))

    return Π

def zenithal_hydrostatic_delay(
    P: Vector,         # hPa 
    lat: Vector = 45,  # deg 
    height: Vector = 0 # m
) -> float:
    """zhd = zenithal_hydrostatic_delay(P, lat, height)

Determine the dry tropospheric delay at zenith for radio waves.

    P: hPa
    lat: deg
    height: m

Return delay in m    
 
"""
    lat = np.deg2rad(lat)
     
    zhd0 = 2.2768e-3 # m hPa⁻¹
    A = 0.00266      # no unit
    B = 2.8e-7       # m⁻¹
    f = 1 - A * np.cos(2 * lat) - B * np.asarray(height)
    zhd = zhd0 * np.asarray(P) / f
    
    return zhd
