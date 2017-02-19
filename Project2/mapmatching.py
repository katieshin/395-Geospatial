# -*- coding: utf-8 -*-
import pdb; 
import csv
import numpy
from math import tan, degrees
from helper_functions import haversine

link_file = open("link_data.csv", "r")
probe_file = open("probe_point_data.csv", "r")

probe_data = csv.reader(probe_file, delimiter=',')
link_data = csv.reader(link_file, delimiter=',')

# for each probe data line, create a p_lat_lng tuple and find the
# link that contains a point with the minimum distance for that
# lat_lng tuple

# first ID = [ID,lat,long,alt]
ID1 = [0,0,0,0]

# last ID = [ID,lat,long,alt]
ID2 = [0,0,0,0]

#temp variable
current = [0,0,0,0]
i = 0
for p_line in probe_data:
    if i < 59:
        i = i + 1
        continue

    link_file.seek(0)
    p_lat_lng = [float(p_line[3]), float(p_line[4])]
    min_distance = [0, float("infinity")]

# split each link line's 15th element, which are the reference points
# into a list using the operator "|"

    for l_line in link_data:
        nodes = l_line[14].split("|")

# split each links reference points string into a list of lat_lng_alt
# strings

        for node in nodes:
            l_lat_lng = [float(node.split("/")[0]),
                         float(node.split("/")[1])]

            dist = float(haversine(p_lat_lng[0],
                                   p_lat_lng[1],
                                   l_lat_lng[0],
                                   l_lat_lng[1]))

            if dist < min_distance[1]:
                min_distance = [l_line[0], dist]

    #pdb.set_trace()
    current = [min_distance[0],float(p_line[3]),float(p_line[4]),float(p_line[5])]
    print "printing current"
    print current
    if ID1[0] == 0:
        ID1 = current
        ID2 = current
    else:
        # compare
        if ID1[0] != current[0]:
            #calculate slope
            x = float(haversine(ID1[1],
                       ID1[2],
                       ID2[1],
                       ID2[2]))
            print "printing x"
            print x
            y = ID2[3]-ID1[3]
            print "printing y"
            print y
            print ('printing slope')
            try:
                ang_radians = float(y/x)
                slope = numpy.rad2deg(numpy.arctan(ang_radians))  
            except:
                slope = 0
                pass
            print slope
            ID1 = current
            ID2 = current
        else:
            ID2 = current
            print "printing ID2"
            print ID2




    print p_lat_lng, min_distance

# for each probe data latlng, grab the latlng
probe_data.close()
link_data.close()
