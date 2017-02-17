#!/usr/bin/env python
# coding=utf-8

import sys
#import cgml_reader
import numpy as np
import math
from geo_algorithm import *
from geo_primitives import *
from lxml import etree

def calculate(poly):
    polynormal = orient(poly)
    normal = (0,0,1)
    if polynormal==None:
        return None
    #return angle_d(orient(poly.poslist))
    return dot(polynormal,normal)

def parsing_report(path):
    geo_report = open(path).read()
    report_root = etree.XML(geo_report)
    return [f.text for f in report_root.findall('.//face')]

def semantic_val(buildings,surfaces,filterpath=None):
    # if sys.argv[1]:
    #     path = sys.argv[1]
    # else:
    #     print "please input the right parameter!"
    #     return
    # data = cgml_reader.cgml2class(path)
    # #print "start semantic validation"
    # b_ids = cgml_reader.Building_output(data)
    # #print "buildings total number: %d" % len(b_ids)
    # global inputfile
    # inputfile = path
    # if len(sys.argv)>3:
    #     r_path = sys.argv[3]
    global invalid_building

    invalid_faces = parsing_report(filterpath)

    for building in buildings:
        count=0
        for s_id in building.surfaces:
            poly = surfaces[s_id]
            if poly.polyid in invalid_faces:
                continue
            # p_array = np.array(poly.poslist[0])
            # p_array_trans = p_array.reshape(p_array.size/3,3).tolist()
            cosnormal = calculate(poly.poslist[0])
            if cosnormal==None:
                continue
            orientation = angle_d(cosnormal)
            #orientation = calculate(poly)
            poly.set_orientation(orientation)
            if (cosnormal>=math.cos(85 * math.pi / 180) or cosnormal<=math.cos(95 * math.pi / 180)) and (poly.role == 'WallSurface' or poly.role == 'InteriorWallSurface'):
                #print calculate(poly),poly.role
                poly.set_valid(False)
                count+=1
                #poly.set_planar(isPolyPlanar(p_array_trans[:-1],normal))
            elif cosnormal>=math.cos(175 * math.pi / 180) and (poly.role == 'GroundSurface' or poly.role == 'OuterCeilingSurface'  or poly.role == 'CeilingSurface'):
                #print calculate(poly),poly.role
                poly.set_valid(False)
                count+=1
                #poly.set_planar(isPolyPlanar(p_array_trans[:-1],normal))
            elif cosnormal<=math.cos(85 * math.pi / 180) and (poly.role == 'RoofSurface' or poly.role == 'OuterFloorSurface'or poly.role == 'FloorSurface'):
                #print calculate(poly),poly.role
                poly.set_valid(False)
                count+=1
                #poly.set_planar(isPolyPlanar(p_array_trans[:-1],normal))
            else:
                continue
        if count>0:
            invalid_building+=1
        # for fid in poly.fid:
        #     if poly.polyid not in cgml_reader.buildings[fid].invalidpolys:
        #         cgml_reader.buildings[fid].add_invalidpoly(poly.polyid)
    #return b_ids

def write_report(buildings,surfaces):
    global invalid_wall
    global invalid_roof
    global invalid_ground
    global invalid_building
    global invalid_outerceiling
    global invalid_outerfloor
    global invalid_floor
    global invalid_ground
    global invalid_interiorwall
    global inputfile
    global wall_count
    global roof_count
    global ground_count
    global outerceiling_count
    global outerfloor_count
    global floor_count
    global ceiling_count
    global interiorwall_count
    global closure_count
    global window_count
    global door_count
    global closure_count

    root = etree.Element('Semantic')
    if len(buildings) == 0:
        print("\n")
        return
    for building in buildings:
        # if not cgml_reader.buildings.has_key(b_id):
        #     print "miss building ID %s" % b_id
        #     continue
        # building = cgml_reader.buildings[b_id]
        child = report_building(building,'building',surfaces)
        if len(child):
            root.append(child)
            # if building.invalidpolys:
            #     invalid_building+=1
    infile_node = etree.Element('inputfile')
    infile_node.text = inputfile
    root.append(infile_node)
    # tolerance_node = etree.Element('tolerance')
    # tolerance_node.text = str(tolerance)
    # root.append(tolerance_node)
    building_node = etree.Element('buildings')
    building_node.text = str(len(buildings))
    root.append(building_node)
    invalidbuilding_node = etree.Element('invalidbuildings')
    invalidbuilding_node.text = str(invalid_building)
    root.append(invalidbuilding_node)
    surfaces_node = etree.Element('surfaces')
    surfaces_node.text = str(len(surfaces))
    root.append(surfaces_node)
    invalidsurfaces_node = etree.Element('invalidsurfaces')
    invalidsurfaces_node.text = str(invalid_wall+invalid_roof+invalid_ground)
    root.append(invalidsurfaces_node)
    wall_node = etree.Element('walls')
    wall_node.text = str(wall_count)
    root.append(wall_node)
    invalidwall_node = etree.Element('invalidwalls')
    invalidwall_node.text = str(invalid_wall)
    root.append(invalidwall_node)
    roof_node = etree.Element('roofs')
    roof_node.text = str(roof_count)
    root.append(roof_node)
    invalidroof_node = etree.Element('invalidroofs')
    invalidroof_node.text = str(invalid_roof)
    root.append(invalidroof_node)
    ground_node = etree.Element('grounds')
    ground_node.text = str(ground_count)
    root.append(ground_node)
    invalidground_node = etree.Element('invalidgrounds')
    invalidground_node.text = str(invalid_ground)
    root.append(invalidground_node)
    floor_node = etree.Element('floors')
    floor_node.text = str(floor_count)
    root.append(floor_node)
    invalidfloor_node = etree.Element('invalidfloors')
    invalidfloor_node.text = str(invalid_floor)
    root.append(invalidfloor_node)
    ceiling_node = etree.Element('ceilings')
    ceiling_node.text = str(ceiling_count)
    root.append(ceiling_node)
    invalidceiling_node = etree.Element('invalidceilings')
    invalidceiling_node.text = str(invalid_ceiling)
    root.append(invalidceiling_node)
    outerfloor_node = etree.Element('outerfloors')
    outerfloor_node.text = str(outerfloor_count)
    root.append(outerfloor_node)
    invalidouterfloor_node = etree.Element('invalidouterfloors')
    invalidouterfloor_node.text = str(invalid_outerfloor)
    root.append(invalidouterfloor_node)
    outerceiling_node = etree.Element('outerceilings')
    outerceiling_node.text = str(outerceiling_count)
    root.append(outerceiling_node)
    invalidouterceiling_node = etree.Element('invalidouterceilings')
    invalidouterceiling_node.text = str(invalid_outerceiling)
    root.append(invalidouterceiling_node)
    interiorwall_node = etree.Element('interiorwalls')
    interiorwall_node.text = str(interiorwall_count)
    root.append(interiorwall_node)
    invalidinteriorwall_node = etree.Element('invalidinteriorwalls')
    invalidinteriorwall_node.text = str(invalid_interiorwall)
    root.append(invalidinteriorwall_node)
    window_node = etree.Element('windows')
    window_node.text = str(window_count)
    root.append(window_node)
    door_node = etree.Element('doors')
    door_node.text = str(door_count)
    root.append(door_node)
    closure_node = etree.Element('closures')
    closure_node.text = str(closure_count)
    root.append(closure_node)

    return root

def surface_node(surface,surfaces):
    global invalid_wall
    global invalid_roof
    global invalid_ground
    global invalid_outerceiling
    global invalid_outerfloor
    global invalid_floor
    global invalid_ceiling
    global invalid_interiorwall
    global wall_count
    global roof_count
    global ground_count
    global outerceiling_count
    global outerfloor_count
    global floor_count
    global ceiling_count
    global interiorwall_count
    global closure_count
    global window_count
    global door_count
    global closure_count

    if surface < len(surfaces):
        poly = surfaces[surface]
        child = etree.Element('surface', ID=poly.polyid, type=poly.role)
        grandchild1 = etree.Element('validity')
        grandchild1.text = str(poly.valid)
        child.append(grandchild1)
        grandchild2 = etree.Element('orientation')
        grandchild2.text = str(poly.orientation)
        child.append(grandchild2)
        #if not poly.valid:
        #grandchild0 = etree.Element('code')
        role = poly.role
        if role == 'WallSurface':
            wall_count+=1
            if not poly.valid:
                invalid_wall+=1
                #grandchild0.text = 'S102'
        elif role == 'RoofSurface':
            roof_count+=1
            if not poly.valid:
                invalid_roof+=1
            #grandchild0.text = 'S103'
        elif role == 'GroundSurface':
            ground_count+=1
            if not poly.valid:
                invalid_ground+=1
            #grandchild0.text = 'S101'
        elif role == 'OuterFloorSurface':
            outerfloor_count+=1
            if not poly.valid:
                invalid_outerfloor+=1
            #grandchild0.text = 'S104'
        elif role == 'OuterCeilingSurface':
            outerceiling_count+=1
            if not poly.valid:
                invalid_outerceiling+=1
            #grandchild0.text = 'S105'
        elif role == 'FloorSurface':
            floor_count+=1
            if not poly.valid:
                invalid_floor+=1
            #grandchild0.text = 'S106'
        elif role == 'CeilingSurface':
            ceiling_count+=1
            if not poly.valid:
                invalid_ceiling+=1
            #grandchild0.text = 'S107'
        elif role == 'InteriorWallSurface':
            interiorwall_count+=1
            if not poly.valid:
                invalid_interiorwall+=1
            #grandchild0.text = 'S108'
        #child.append(grandchild0)          
            # grandchild3 = etree.Element('planar')
            # grandchild3.text = str(poly.planar)
            # child.append(grandchild3)
        return child
    # elif cgml_reader.shells.has_key(surface):
    #     shell = cgml_reader.shells[surface]
    #     child = etree.Element('compositesurface', ID=surface, type='Compositesurface')
    #     for sh in shell.polylist:
    #         child.append(surface_node(sh))
    #     return child
    else:
        raise ValueError('generate error,%s' % surface)

def report_building(building,node_name,surfaces):
    child = etree.Element(node_name, ID=building.fid)
    if building.buildingparts:
        for bp in building.buildingparts:
            grandchild=report_building(buildings[bp],'buildingpart',surfaces)
            if len(grandchild)!=0:
                child.append(grandchild)
    else:
        #if building.invalidpolys:
        for surface in building.surfaces:
            grandchild=surface_node(surface,surfaces)
            child.append(grandchild)    

    return child
     
wall_count=0
roof_count=0
ground_count=0
outerceiling_count=0
outerfloor_count=0
floor_count=0
ceiling_count=0
interiorwall_count=0
closure_count=0
window_count=0
door_count=0
closure_count=0

invalid_wall=0
invalid_ground=0
invalid_roof=0
invalid_building=0
invalid_outerceiling=0
invalid_outerfloor=0
invalid_floor=0
invalid_ceiling=0
invalid_interiorwall=0
inputfile=None


# buildings=list()
# surfaces=list()
# if len(sys.argv)>3:
#     tolerance = int(sys.argv[2])
# else:
#     tolerance = 5.0
def val_report(gm_buildings,gm_surfaces,path):
    # global buildings
    # global surfaces
    # buildings=gm_buildings
    # surfaces=gm_surfaces
    semantic_val(gm_buildings,gm_surfaces,path)
    root = write_report(gm_buildings,gm_surfaces)
    print(etree.tostring(root,pretty_print=True))

if __name__ == "__main__":
    # bids = semantic_check()
    # #print "Building amount:%d" % len(bids)
    # root = write_report(bids)
    # print etree.tostring(root,pretty_print=True)
    pass
