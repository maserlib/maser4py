#! /usr/bin/env python

import numpy
from math import pi, cos, acos, sin, asin, tan, \
    atan, atan2, sqrt, degrees

Radeg = 180./pi

# Convert rectangular coordinates [X,Y]
# to polar coordinates [rho,theta]
# Input parameters X and Y can
# be scalars or two lists of n elements.
# X.Bonnin (LESIA), 03-JUN-2012
def recpol(x,y,DEGREES=False):

    islist = isinstance(x,list)
    if not (islist):
        x = [x] ; y = [y]

    r = [] ; theta = []
    for i,xi in enumerate(x):
        xi = float(xi)
        yi = float(y[i])
        # Find radii
        r.append(sqrt(xi*xi + yi*yi))
        if (y == 0.0):
            thetai=0.0
        elif (x == 0.0):
            if (y >= 0):
                thetai=0.5*pi
            else:
                thetai-0.5*pi
        else:
            thetai = atan2(yi,xi)
        if (thetai < 0.0): thetai = thetai + 2*pi
        if (DEGREES): thetai = degrees(thetai)
        theta.append(thetai)

    if not (islist):
        r = r[0] ; theta = theta[0]

    return r, theta

# Adapted from get_sun.pro ssw routine.
# X.Bonnin (LESIA), 03-JUN-2012
def get_sun(datetime):

    islist = isinstance(datetime,list)
    if not (islist):
        datetime = [datetime]

    ephem = []
    for date in datetime:

        # Convert input datetime into julian date
        jd = sum(tim2jd(date))

        # Julian centuries from 1900.0
        t = (jd - 2415020.0)/36525.0

        # Carrington rotation number
        carr = (1./27.2753)*(jd-2398167.0) + 1.0

        # Geometric Mean Longitude (deg):
        mnl = 279.69668 + 36000.76892*t + 0.0003025*(t**2)
        mnl = mnl % 360.0

        # Mean anomaly (deg):
        mna = 358.47583 + 35999.04975*t - \
            0.000150*(t**2) - 0.0000033*(t**3)
        mna = mna % 360.0

        # Eccentricity of orbit:
        e = 0.01675104 - 0.0000418*t - 0.000000126*(t**2)

        # Sun's equation of center (deg):
        c = (1.919460 - 0.004789*t - 0.000014*(t**2))*sin(mna/Radeg) + \
            (0.020094 - 0.000100*t)*sin(2*mna/Radeg) + \
            0.000293*sin(3*mna/Radeg)

        # Sun's true geometric longitude (deg)
        # (Refered to the mean equinox of date.  Question: Should the higher
        # accuracy terms from which app_long is derived be added to true_long?)
        true_long = (mnl + c) % 360.0

        # Sun's true anomaly (deg):
        ta = (mna + c) % 360.0

        # Sun's radius vector (AU).  There are a set of higher accuracy
        #   terms not included here.  The values calculated here agree with
        #   the example in the book:
        dist = 1.0000002*(1.0 - e**2)/(1.0 + e*cos(ta/Radeg))

        # Semidiameter (arc sec):
        sd = 959.63/dist

        # Apparent longitude (deg) from true longitude:
        omega = 259.18 - 1934.142*t	
        app_long = true_long - 0.00569 - 0.00479*sin(omega/Radeg)

        # Latitudes (deg) for completeness.  Never more than 1.2 arc sec from 0,
        #   always set to 0 here:
        true_lat = 0.0 
        app_lat = 0.0

        # True Obliquity of the ecliptic (deg):
        ob1 = 23.452294 - 0.0130125*t - 0.00000164*(t**2) \
            + 0.000000503*(t**3)

        # True RA, Dec (is this correct?):
        y = cos(ob1/Radeg)*sin(true_long/Radeg)
        x = cos(true_long/Radeg)
        r, true_ra = recpol( x, y, DEGREES=True)
        true_ra = true_ra % 360.0
        if (true_ra < 0): true_ra = true_ra + 360.0
        true_ra = true_ra/15.0
        true_dec = asin(sin(ob1/Radeg)*sin(true_long/Radeg))*Radeg

        # Apparent  Obliquity of the ecliptic:
        ob2 = ob1 + 0.00256*cos(omega/Radeg)

        # Apparent  RA, Dec (agrees with example in book):
        y = cos(ob2/Radeg)*sin(app_long/Radeg)
        x = cos(app_long/Radeg)
        r, app_ra = recpol( x, y, DEGREES=True)
        app_ra = app_ra % 360.0
        if (app_ra < 0.0): app_ra = app_ra + 360.0
        app_ra = app_ra/15.0
        app_dec = asin(sin(ob2/Radeg)*sin(app_long/Radeg))*Radeg

        # Heliographic coordinates:
        theta = (jd - 2398220.0)*360.0/25.38
        i = 7.25					
        k = 74.3646 + 1.395833*t			
        lamda = true_long - 0.00569
        lamda2 = lamda - 0.00479*sin(omega/Radeg)
        diff = (lamda - k)/Radeg
        x = atan(-cos(lamda2/Radeg)*tan(ob1/Radeg))*Radeg
        y = atan(-cos(diff)*tan(i/Radeg))*Radeg

        # Position of north pole (deg):
        pa = x + y

        # Latitude at center of disk (deg):
        he_lat = asin(sin(diff)*sin(i/Radeg))*Radeg

        # Longitude at center of disk (deg):
        y = -sin(diff)*cos(i/Radeg)
        x = -cos(diff)
        r, eta = recpol(x, y, DEGREES=True)
        he_lon = (eta - theta) % 360.0
        if (he_lon < 0.0): he_lon = he_lon + 360.0

        ephem.append([dist,sd,true_long,true_lat,
                      app_long,app_lat,true_ra,true_dec,
                      app_ra, app_dec, he_lon, he_lat, pa, carr])

    if not (islist):
        ephem = ephem[0]
    return ephem

# Adapted from tim2carr.pro ssw routine
# X.Bonnin (LESIA), 03-JUN-2012
def tim2carr(date,offset=0.0,DC=False):
    max_diff = 12.0/360.0

    islist=isinstance(date,list)
    if not (islist):
        date = [date]

    carr_date = []
    for date_i in date:
        sun_data = get_sun(date_i)
        carr = sun_data[-1]
        he_lon = sun_data[-4]
        del sun_data
        if (DC):
            int_carr = int(carr)
            frac_carr = carr - int(carr)
            frac_lon = (360.0 - he_lon)/360.
            if (abs(frac_carr-frac_lon) > max_diff) and \
                (frac_carr > frac_lon):
                int_carr = int_carr + 1
            elif (abs(frac_carr-frac_lon) > max_diff) and \
                (frac_carr < frac_lon):
                int_carr = int_carr - 1
            carr_date.append(int_carr + frac_lon - offset/360.0)
        else:
            carr_date.append((he_lon - offset)%360.0)

        if not (islist):
            carr_date = carr_date[0]

        return carr_date
                


# Module to convert datetime date in julian date
def tim2jd(date):
    
    K = float(date.year)
    M = float(date.month)
    I = float(date.day)
    UT = float(date.hour) + \
        float(date.minute)/60.0 + \
        float(date.second)/3600.0
	
    jd = 367.*K - int(7*(K+int((M+9.)/12.))/4.) + int((275.*M)/9) + \
        I + 1721013.5 + UT/24. - 0.5*cmp(100.*K+M-190002.5,0) + 0.5
	
    jdint = int(jd)
    jdfrac = jd - jdint
	
    return jdint,jdfrac

