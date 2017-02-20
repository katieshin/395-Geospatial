# -*- coding: utf-8 -*-
import pdb 
import csv
import numpy
from math import tan, degrees
from helper_functions import haversine

link_file = open("link_data.csv", "r")
probe_file = open("probe_point_data.csv", "r")
filewrite = open("mapmatchingoutput.csv", "w")

probe_data = csv.reader(probe_file, delimiter=',')
link_data = csv.reader(link_file, delimiter=',')
filewrite.write("linkID, x, y, ourSlope, givenSlope \n")
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
    dist_from_refnode = 0
    min_distance = [0, float("infinity")]

# split each link line's 15th element, which are the reference points
# into a list using the operator "|"

    for l_line in link_data:
        nodes = l_line[14].split("|")

# ref node is the first node in the l_line index 14, so get its lat lng

        refnode = [float(nodes[0].split("/")[0]),
                   float(nodes[0].split("/")[1])]

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

# calculate dist_from_refnode everytime updating min_distance

                dist_from_refnode =  float(haversine(p_lat_lng[0],
                                                     p_lat_lng[1],
                                                     refnode[0],
                                                     refnode[1]))

    current = [min_distance[0],float(p_line[3]),float(p_line[4]),float(p_line[5])]
    # print "printing current"
    # print current
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
            # print "printing x"
            # print x
            y = ID2[3]-ID1[3]
            # print "printing y"
            # print y
            # print ('printing slope')
            try:
                slope = float(y/x)
            except:
                slope = 0
                pass
            print slope
            # filewrite.write(l_line[0]+ "," + str(x)+ "," + str(y)+ "," + str(slope)+ "," + l_line[16] + "\n")
            ID1 = current
            # ID1 = current
            # ID2 = current
        else:
            ID2 = current
            # print "printing ID2"
            # print ID2




    print p_lat_lng, min_distance, dist_from_refnode

probe_data.close()
link_data.close()
