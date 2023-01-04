# Modified from https://gist.github.com/JoanTheSpark/e3fab5a8af44f7f8779c
import sys, os
import shutil
import math
import itertools
from copy import deepcopy

#              0        1          2      3      4        5    6
LIST_elmt = ["  ("," (start ",") (end ",") "," (layer ",") ","))"]
#LIST_elmt = ["  (gr_line (start 131.571908 182.314571) (end 112.874456 120.68499) (angle 90) (layer Dwgs.User) (width 0.1))"]
#LIST_elmt = ["  (segment (start 118.7 106.7) (end 119.4 106.7) (width 0.25) (layer B.Cu) (net 0))"]
DICT_elmt = {"seg" : ["segment", "(width ", "(net "],
             "arc" : ["gr_arc", "(angle ", "(width "],
             "lne" : ["gr_line", "(angle ", "(width "],
             }
DICT_lyr = { "dwg" : "Dwgs.User",
             "cmt" : "Cmts.User",
             "cut" : "Edge.Cuts",
             "fcu" : "F.Cu",
             "bcu" : "B.Cu",
             }

def FNC_string (element,
                STR_start, #1
                STR_end, #2
                Angle, #4
                layer, #5
                width,
                ):
    STR_line = ""
    """
                      0          1         2    3          4           5
    LIST_elmt = ["  ("," (start ",") (end ",") "," (layer ",") (width ","))"]
    """
    for i in range(len(LIST_elmt)):
        STR_line += LIST_elmt[i]
        if i == 0:
            STR_line += DICT_elmt[element][0]
        if i == 1:
            STR_line += STR_start
        if i == 2:
            STR_line += STR_end
        if i == 3:
            if element == "seg":
                STR_line += DICT_elmt[element][1]
                STR_angle = "{:.1f}".format(width)
            else:
                STR_line += DICT_elmt[element][1]
                if element == "lne":
                    STR_angle = "90"
                else:
                    STR_angle = str(Angle)
            STR_line += STR_angle + ")"
        if i == 4:
            STR_line += DICT_lyr[layer]
        if i == 5:
            if element == "seg":
                STR_line += DICT_elmt[element][2]
                STR_line += str(Angle)
            else:
                STR_line += DICT_elmt[element][2]
                STR_line += "{:.2f}".format(width)
    STR_line += "\n"
    return STR_line

def FNC_polygon (element,
                STR_start, #1
                STR_end, #2
                Angle, #4
                layer, #5
                width,
                ):
    STR_line = ""
    """
                      0          1         2    3          4           5
    LIST_elmt = ["  ("," (start ",") (end ",") "," (layer ",") (width ","))"]
    """
    for i in range(len(LIST_elmt)):
        STR_line += LIST_elmt[i]
        if i == 0:
            STR_line += DICT_elmt[element][0]
        if i == 1:
            STR_line += STR_start
        if i == 2:
            STR_line += STR_end
        if i == 3:
            if element == "seg":
                STR_line += DICT_elmt[element][1]
                STR_angle = "{:.1f}".format(width)
            else:
                STR_line += DICT_elmt[element][1]
                if element == "lne":
                    STR_angle = "90"
                else:
                    STR_angle = str(Angle)
            STR_line += STR_angle + ")"
        if i == 4:
            STR_line += DICT_lyr[layer]
        if i == 5:
            if element == "seg":
                STR_line += DICT_elmt[element][2]
                STR_line += str(Angle)
            else:
                STR_line += DICT_elmt[element][2]
                STR_line += "{:.2f}".format(width)
    STR_line += "\n"
    return STR_line


def FNC_spiral (cntr, # (x,y)
                radius,
                sides,
                startangle,
                tw, # track width
                td, # track distance
                turns,
                layer,
                net,
                ):

    STR_data = ""
    baseX = cntr[0]
    baseY = cntr[1]
    segangle = 360 / sides
    segradius = td / sides

    for i in range(turns * sides):
        # central rings for HV and SNS
        startX = baseX + (radius + segradius * i) * math.sin(math.radians(segangle*(i) + startangle))
        startY = baseY + (radius + segradius * i) * math.cos(math.radians(segangle*(i) + startangle))
        endX = baseX + (radius + segradius * (i+1.0)) * math.sin(math.radians(segangle*(i+1.0) + startangle))
        endY = baseY + (radius + segradius * (i+1.0)) * math.cos(math.radians(segangle*(i+1.0) + startangle))
        STR_data += FNC_string ("seg", #type of line
                                "{:.6f}".format(startX) + " " + "{:.6f}".format(startY), # start point
                                "{:.6f}".format(endX) + " " + "{:.6f}".format(endY), # end point
                                net, # angle or net value
                                layer, # layer on pcb
                                tw, # track width
                                )
    return STR_data

def FNC_circle(cntr, # (x,y)
                radius,
                sides,
                startradius,
                tw, # track width
                ncircles,
                layer,
                net,
                ):
    STR_data = ""
    baseX = cntr[0]
    baseY = cntr[1]
    segangle = 360 / sides
    segradius = (radius - startradius) / (ncircles-1)
    for n in range(ncircles):

        for i in range(sides):
            # central rings for HV and SNS
            startX = baseX + (startradius + segradius * (n)) * math.sin(math.radians(segangle*(i)))
            startY = baseY + (startradius + segradius * (n)) * math.cos(math.radians(segangle*(i)))
            endX = baseX + (startradius + segradius * (n)) * math.sin(math.radians(segangle*(i+1.0)))
            endY = baseY + (startradius + segradius * (n)) * math.cos(math.radians(segangle*(i+1.0)))
            STR_data += FNC_string ("seg", #type of line
                                    "{:.6f}".format(startX) + " " + "{:.6f}".format(startY), # start point
                                    "{:.6f}".format(endX) + " " + "{:.6f}".format(endY), # end point
                                    net, # angle or net value
                                    layer, # layer on pcb
                                    tw, # track width
                                    )
    return STR_data


if __name__ == '__main__':
    Center = [105.0,105.0] # x/y coordinates of the centre of the pcb sheet
    Radius = 0.01 # start radius in mm
    EndRadius = 0.5
    Sides = 60
    StartAngle = 0.0 # degrees
    TrackWidth = 0.05
    TrackDistance = 0.04
    Turns = 15
    ncircles = 5
    Layer = "fcu"
    Net = "0"
    # Hexagonal lattice
    centers_spirals = [[105.0, 105.0],[106.55, 105.0],[105.77499999999999, 106.34233937586588],[104.225, 106.34233937586588],[103.45, 105.0],[104.22500000000001, 103.65766062413412],[105.775, 103.65766062413412]]
    centers = [[105.0, 105.0],[106.5, 105.0],[105.75, 106.29903810567666],[104.25, 106.29903810567666],[103.5, 105.0],[104.25, 103.70096189432334],[105.75, 103.70096189432334]]
    """for c in centers:
        print(FNC_spiral (c,
                      Radius,
                      Sides,
                      StartAngle,
                      TrackWidth,
                      TrackDistance,
                      Turns,
                      Layer,
                      Net,
                      ))"""
    for c in centers:
        print(FNC_circle (c,
                      EndRadius,
                      Sides,
                      Radius,
                      TrackWidth,
                      ncircles,
                      Layer,
                      Net,
                      ))
