from math import radians, cos, sin, asin, sqrt

def find3Ddist(lat1,lon1,alt1,lat2,lon2,alt2):
    a=llatoecef(lat1,lon1,alt1)
    b=llatoecef(lat2,lon2,alt2)
    ans = [0,0,0]
    total=0
    i = 0
    while i < 3:
        ans[i]=abs((b[i]-a[i]))**(2)
        total = total + ans[i]
        i = i+1
    h= sqrt(total)
    altdiff = alt2-alt1
    slope = findslope(h, altdiff)
    return[h,slope]

def findslope(h, alt):
    slope = 0
    dist = (h**2 + alt**2) **(.5)
    if dist!=0:
        slope = alt/dist
    return slope

def llatoecef(lat,lon,alt):
    a= 6378137 #in m
    b= 6356752.3142 #in m
    f= (a-b)/a
    e= (f*(2-f))**(.5)
    N= a/((1-((e**2)*((sin(lat))**2)))**(.5))

    x= alt+N*cos(lon)*cos(lat)
    y= alt+N*cos(lon)*sin(lat)
    z= alt+(1-(e**2)*N*sin(lon))
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
