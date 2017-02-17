# -*- coding: utf-8 -*-
import csv
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
    if i < 50:
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

    current = [min_distance[0],float(p_line[3]),float(p_line[4]),float(p_line[5])]
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
            y = ID2[3]-ID1[3]
            print ('printing slope')
            try:
                slope = degrees(tan(y/x))
            except:
                slope = 0
                pass
            print slope
            ID1 = current
            ID2 = current
        else:
            ID2 = current




    print p_lat_lng, min_distance

# for each probe data latlng, grab the latlng
probe_data.close()
link_data.close()
