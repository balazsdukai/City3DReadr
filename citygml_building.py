#!/usr/bin/env python
# coding=utf-8

from lxml import etree
import sys
import subprocess
import numpy as np
from geo_primitives import *
import semantic_check

def grep(file,arg):
    process = subprocess.Popen(['grep','-c',arg,file],stdout=subprocess.PIPE)
    stdout,stderr = process.communicate()
    return stdout

def clear_element(elem):
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]

def parse_polygon(poly):
    global nsmap
    #global vertices
    rings = poly.getchildren()
    polyrings = []
    for ring in rings:
        poly_ring=[]
        posList = ring.find('.//{%s}posList' % nsmap["gml"])
        if posList != None:
            pos_list = np.array(posList.text.split(),dtype=np.float64)
            pos_list = pos_list.reshape(len(pos_list)/3,3)[:-1]
            # try:
            #     for pos in pos_list.tolist():
            #         if pos in vertices:
            #             poly_ring.append(vertices.index(pos))
            #         else:
            #             poly_ring.append(len(vertices))
            #             vertices.append(pos)
            # except ValueError:
            #     print vertices," : ",pos
            #     return
            poly_ring = pos_list.tolist()
        else:
            posList = ring.findall('.//{%s}pos')
            for pos_list in posList[:-1]:
                pos = [float(v) for v in pos_list.text.split()]
                # if pos in vertices:
                #     poly_ring.append(vertices.index(pos))
                # else:
                #     poly_ring.append(len(vertices))
                #     vertices.append(pos)
                poly_ring.append(pos)
        ring_role = ring.tag[len(nsmap["gml"])+2:]
        if ring_role=='exterior':
            polyrings.insert(0,poly_ring)
        else:
            polyrings.append(poly_ring)
    return polyrings


def iter_parse(context,element):
    global nsmap
    #global vertices
    global surfaces
    global buildings
    if element == "Building":
        countBuilding = 0
        for event,elem in context:
            if event=='end' and elem.tag == "{%s}%s" % (nsmap["bldg"],element):
                building = Building()
                countBuilding+=1
                idBuilding="NULL"
                if "{%s}id" % nsmap["gml"] in elem.attrib:
                    idBuilding=elem.attrib["{%s}id" % nsmap["gml"]]
                building.fid = idBuilding
                #Roof=elem.findall('.//{%s}RoofSurface' % nsmap["bldg"])
                boundedBys = elem.findall('.//{%s}boundedBy' % nsmap["bldg"])
                if len(boundedBys)==0:continue
                for bB in boundedBys:
                    gm_surface=bB.getchildren()[0]
                    role=gm_surface.tag[len(nsmap["bldg"])+2:]
                    gm_surfaceid="NULL"
                    if "{%s}id" % nsmap["gml"] in gm_surface.attrib:
                        gm_surfaceid = gm_surface.attrib["{%s}id" % nsmap["gml"]]
                    polys = gm_surface.findall('.//{%s}Polygon' % nsmap["gml"])
                    for poly in polys:
                        polyid=gm_surfaceid
                        if "{%s}id" % nsmap["gml"] in poly.attrib:
                            polyid = poly.attrib["{%s}id" % nsmap["gml"]]
                        polyrings = parse_polygon(poly)
                        surf = Polygon()
                        surf.poslist = polyrings
                        surf.polyid = polyid
                        surf.role = role
                        surfaces.append(surf)
                        building.surfaces.append(len(surfaces)-1)
                # Wall=elem.findall('.//{%s}WallSurface' % nsmap["bldg"])
                # for wall in Wall:
                #     wallpolys = wall.findall('.//{%s}Polygon' % nsmap["gml"])
                #     surfaces.extend(wallpolys)
                # Ground=elem.findall('.//{%s}GroundSurface' % nsmap["bldg"])
                # for ground in Ground:
                #     groundpolys = ground.findall('.//{%s}Polygon' % nsmap["gml"])
                #     surfaces.extend(groundpolys)
                buildings.append(building)
                clear_element(elem)
    return countBuilding

def building(infile):
    global nsmap
#     if len(sys.argv)>1:
#         infile = sys.argv[1]
#     else:
#         infile = "/Users/octeufer/OneDrive/3DGeo/Dataset/Friedrichshain-Kreuzberg/citygml.gml"
    if int(grep(infile,"citygml/2.0"))>0:
        ns_citygml = "http://www.opengis.net/citygml/2.0"
        ns_gml = "http://www.opengis.net/gml"
        ns_bldg = "http://www.opengis.net/citygml/building/2.0"
        ns_tran = "http://www.opengis.net/citygml/transportation/2.0"
        ns_veg = "http://www.opengis.net/citygml/vegetation/2.0"
        ns_gen = "http://www.opengis.net/citygml/generics/2.0"
        ns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        ns_xAL = "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
        ns_xlink = "http://www.w3.org/1999/xlink"
        ns_dem = "http://www.opengis.net/citygml/relief/2.0"
        ns_frn = "http://www.opengis.net/citygml/cityfurniture/2.0"
        ns_tun = "http://www.opengis.net/citygml/tunnel/2.0"
        ns_wtr = "http://www.opengis.net/citygml/waterbody/2.0"
        ns_brid = "http://www.opengis.net/citygml/bridge/2.0"
        ns_app = "http://www.opengis.net/citygml/appearance/2.0"
    else:
        ns_citygml = "http://www.opengis.net/citygml/2.0"
        ns_gml = "http://www.opengis.net/gml"
        ns_bldg = "http://www.opengis.net/citygml/building/2.0"
        ns_tran = "http://www.opengis.net/citygml/transportation/2.0"
        ns_veg = "http://www.opengis.net/citygml/vegetation/2.0"
        ns_gen = "http://www.opengis.net/citygml/generics/2.0"
        ns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        ns_xAL = "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
        ns_xlink = "http://www.w3.org/1999/xlink"
        ns_dem = "http://www.opengis.net/citygml/relief/2.0"
        ns_frn = "http://www.opengis.net/citygml/cityfurniture/2.0"
        ns_tun = "http://www.opengis.net/citygml/tunnel/2.0"
        ns_wtr = "http://www.opengis.net/citygml/waterbody/2.0"
        ns_brid = "http://www.opengis.net/citygml/bridge/2.0"
        ns_app = "http://www.opengis.net/citygml/appearance/2.0"
    nsmap={
        None : ns_citygml,
        'gml': ns_gml,
        'bldg': ns_bldg,
        'tran': ns_tran,
        'veg': ns_veg,
        'gen' : ns_gen,
        'xsi' : ns_xsi,
        'xAL' : ns_xAL,
        'xlink' : ns_xlink,
        'dem' : ns_dem,
        'frn' : ns_frn,
        'tun' : ns_tun,
        'brid': ns_brid,
        'app' : ns_app
        }
    context = etree.iterparse(infile, events=('start','end'))
    count = iter_parse(context,"Building")
    #global vertices
    #vertices = np.array(vertices)
    print("Surfaces: %d" % len(surfaces))
    print("Buildings: %d" % count)
    #global gses
    #gses = surfaces
#     if count>0:
#         semantic_check.val_report(buildings,surfaces,sys.argv[2])
    return count

#gses=()
nsmap={}
vertices=[]
surfaces=[]
buildings=[]

# if __name__ == "__main__":
#     main()
