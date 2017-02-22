# -*- coding: utf-8 -*-
import pdb 
import csv
import numpy
from math import tan, degrees
from helper_functions import haversine, find3Ddist, perp_dist
import time

start_time = time.time()

link_file = open("link_data.csv", "r")
probe_file = open("probe_point_data.csv", "r")
slopedata = open("slopedata.csv", "w")
matchedpoints = open("mapmatchingoutput.csv", "w")

probe_data = csv.reader(probe_file, delimiter=',')
link_data = csv.reader(link_file, delimiter=',')
slopedata.write("linkID, dist_from_refnode, slope accuracy \n")
matchedpoints.write("sampleID, dateTime, sourceCode, latitude, longitude,"+ 
                    "altitude, speed, heading, linkPVID, direction,"+ 
                    "distFromRef, distFromLink\n")
# for each probe data line, create a p_lat_lng tuple and find the
# link that contains a point with the minimum distance for that
# lat_lng tuple

# first ID = [ID,lat,long,alt]
ID1 = [0,0,0,0]
# last ID = [ID,lat,long,alt]
ID2 = [0,0,0,0]
#temp variable
current = [0,0,0,0]
i=0
dist_from_refnode=0

for p_line in probe_data:
    if i < 59:
        i = i + 1
        continue

    link_file.seek(0)
    plat = float(p_line[3])
    plon = float(p_line[4])
    palt = float(p_line[5])
    pid = p_line[0]
    dist_from_refnode = 0
    lmin_distance_id = ""
    lmin_distance=float("infinity")
    # split each link line's 15th element, which are the reference points
    # into a list using the operator "|"

    for l_line in link_data:
        nodes = l_line[14].split("|")

        # ref node is the first node in the l_line index 14, so get its lat lng
        #perp_dist([plat, plon, palt],[reflat, reflon, refalt],[nonreflat, nonreflon, nonrefalt])

        
        try:
            ralt = float(nodes[0].split("/")[2])
        except:
            ralt = 0

        try:
            nralt = float(nodes[len(nodes)-1].split("/")[2])
        except:
            nralt = 0

        for node in nodes:
            llat = float(node.split("/")[0])
            llon = float(node.split("/")[1])
            
            dist = float(haversine(plat,
                                   plon,
                                   llat,
                                   llon))

            if dist < lmin_distance:
                lmin_distance_id = l_line[0] #line ID
                lmin_distance_info = l_line[14]
                lmin_distance = dist
                refnode = [float(nodes[0].split("/")[0]),float(nodes[0].split("/")[1])]
                nonrefnode = [float(nodes[len(nodes)-1].split("/")[0]),float(nodes[len(nodes)-1].split("/")[1])]

                rlat = refnode[0]
                rlon = refnode[1]
                nrlat = nonrefnode[0]
                nrlon = nonrefnode[1]

                # calculate dist_from_refnode everytime updating min_distance

                dist_from_refnode =  float(haversine(plat,
                                                     plon,
                                                     refnode[0],
                                                     refnode[1]))
            perpd = perp_dist([plat,plon,palt],[rlat,rlon,ralt],[nrlat,nrlon,nralt])
            


    current = [lmin_distance_id,plat,plon,palt]

    #calculating slope
    if ID1[0] == 0: #first case
        ID1 = current
        ID2 = current
    else:
        # if have reached a new link
        if ID1[0] != current[0]:
            dif = ""
            points = lmin_distance_info.split("|")
            #if altitude data exists for that link (can calculate actual slope)
            if (len(points)>=3) and len(points[0])>=3:
                ref = points[0].split("/")
                nonref = points[len(points)-1].split("/")
                if ref[2]!= "":
                    [actualdistance,actualslope] = find3Ddist(float(ref[0]),float(ref[1]),float(ref[2]),float(nonref[0]),float(nonref[1]),float(nonref[2]))
                    [mydistance,myslope]=find3Ddist(ID1[1],
                                               ID1[2],
                                               ID1[3],
                                               ID2[1],
                                               ID2[2],
                                               ID2[3])
                dif = abs(actualslope - myslope)
                print "dif" + str(dif)

            ID1 = current
            slopedata.write(str(lmin_distance_id) + "," + str(dist_from_refnode)+ "," + str(dif)+ "," + "\n")
        else:
            ID2 = current
    #end of calculating slope
    print "writing"
    matchedpoints.write(str(p_line[0])+ "," + str(p_line[1])+ "," + str(p_line[2])+ "," + str(p_line[3])+ "," + str(p_line[4])+ "," + 
                        str(p_line[5])+ "," + str(p_line[6])+ "," + str(p_line[7])+ "," + str(lmin_distance_id) + ",F," +  str(dist_from_refnode) + "," + str(perpd) + "\n")
print("--- %s seconds ---" % (time.time() - start_time))
probe_data.close()
link_data.close()
