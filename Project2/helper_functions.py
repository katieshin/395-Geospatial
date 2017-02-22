from math import radians, cos, sin, asin, sqrt
import numpy as np

def find3Ddist(lat1,lon1,alt1,lat2,lon2,alt2):
    a=llatoecef(lat1,lon1,alt1)
    b=llatoecef(lat2,lon2,alt2)
    ans = [0,0,0]
    total=0
    i = 0
    while i < 3:
        #find distance
        ans[i]=abs((b[i]-a[i]))**(2)
        total = total + ans[i]
        i = i+1
    distance= sqrt(total)
    altdiff = alt2-alt1
    slope = altdiff/distance
    print "slope" + str(slope)
    return [distance,slope]

def llatoecef(lat,lon,alt):
    a= 6378137 #in m
    b= 6356752.3142 #in m
    f= (a-b)/a
    e= (f*(2-f))**(.5)
    N= a/((1-((e**2)*((sin(lat))**2)))**(.5))

    x= (alt+N)*cos(lon)*cos(lat)
    y= (alt+N)*cos(lon)*sin(lat)
    z= (alt+(1-(e**2)*N)*sin(lon))
    return [x,y,z]

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000# Radius of earth in meters
    return r*c

def perp_dist(probePoint,refPoint,nonRefPoint):
    """Finds the perpendicular distance between probePoint and the line connecting refPoint and nonRefPoint"""
    # Points in the form of [x,y,z]
    # Equation for distance of 3D point to line:
    # |vector(refPoint, probePoint) cross vector(refPoint,nonRefPoint)|/|vector(refPoint,nonRefPoint)|

    # vecRefToPoint = refPoint - probePoint
    # vecLine = refPoint - nonRefPoint
    if refPoint == nonRefPoint:
        return 0
    refPoint = llatoecef(refPoint[0],refPoint[1],refPoint[2])
    nonRefPoint = llatoecef(nonRefPoint[0],nonRefPoint[1],nonRefPoint[2])
    probePoint = llatoecef(probePoint[0],probePoint[1],probePoint[2])
    vecRefToPoint = vector(refPoint,probePoint)
    vecLine = vector(refPoint,nonRefPoint)
    cross_product = np.cross(vecRefToPoint,vecLine)
    numerator = magnitude(cross_product)
    denominator = magnitude(vecLine)
    return numerator/denominator

def vector(point1,point2):
    """Finds the vector between two points"""
    vector = [0,0,0]
    for i in range(3):
        vector[i] = point1[i] - point2[i]
    return vector

def magnitude(vector):
    """Finds the magnitude of a vector"""
    y = [i**2 for i in vector]
    return sqrt(sum(y))
