'''
Created on 21 Feb 2017

@author: Balázs Dukai


-*- coding: utf-8 -*-
  
The MIT License (MIT)
  
This code is part of the CityGML2OBJs package
  
Copyright (c) 2014 
Filip Biljecki
Delft University of Technology
fbiljecki@gmail.com
  
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
  
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# import polygon3dmodule
import markup3dmodule
from lxml import etree

def remove_reccuring(list_vertices):
    """Removes recurring vertices, which messes up the triangulation.
    Inspired by http://stackoverflow.com/a/1143432"""
    # last_point = list_vertices[-1]
    list_vertices_without_last = list_vertices[:-1]
    found = set()
    for item in list_vertices_without_last:
        if str(item) not in found:
            yield item
            found.add(str(item))

def parse_polygon(gml_Polygon):
    """Parses a <gml:Polygon> element into a list of coordinate triplets
    Out: list of coordinate triplets of a polygon [[],[],...]
    """
    # Decompose the polygon into exterior and interior
    e, i = markup3dmodule.polydecomposer(gml_Polygon)
    # Points forming the exterior LinearRing
    epoints = markup3dmodule.GMLpoints(e[0])
    # Clean recurring points, except the last one
    last_ep = epoints[-1]
    epoints_clean = list(remove_reccuring(epoints))
    epoints_clean.append(last_ep)
    # LinearRing(s) forming the interior
    irings = []
    for iring in i:
        ipoints = markup3dmodule.GMLpoints(iring)
        # Clean them in the same manner as the exterior ring
        last_ip = ipoints[-1]
        ipoints_clean = list(remove_reccuring(ipoints))
        ipoints_clean.append(last_ip)        
        irings.append(ipoints_clean)
        
    try:
        polygon = epoints_clean[:-1]
    except:
        polygon = []
    
    return polygon

def extract_polygons(bldg_BoundarySurface):
    """Extracts a list of <gml:Polygon> elements
    from a <bldg:AbstractBoundarySurfaceType> e.g. <bldg:GroundSurface>"""
    
    # not sure if this is the way to go if I'm anyways disregarding the 
    # semantic information

#-----------------------------------------------------------------------------
# Beginning of CityGML import

# Variables imitating user input (legacy of CityGML2OBJs)
FULLPATH = "/home/bdukai/Data/synthetic_LoD_thesis/city_100/LOD2_3_F0_copy.xml"
SEMANTICS = True
OBJECTS = False # Writes all buildings in one group (False) or or multiple groups (True)
SKIPTRI = False # Skip the triangulation (preserve polygons)

# Reading and parsing the CityGML file(s)
CITYGML = etree.parse(FULLPATH)
#-- Getting the root of the XML tree
root = CITYGML.getroot()
# Determine CityGML version
# If 1.0
if root.tag == "{http://www.opengis.net/citygml/1.0}CityModel":
    # Name spaces
    ns_citygml="http://www.opengis.net/citygml/1.0"

    ns_gml = "http://www.opengis.net/gml"
    ns_bldg = "http://www.opengis.net/citygml/building/1.0"
    ns_tran = "http://www.opengis.net/citygml/transportation/1.0"
    ns_veg = "http://www.opengis.net/citygml/vegetation/1.0"
    ns_gen = "http://www.opengis.net/citygml/generics/1.0"
    ns_xsi="http://www.w3.org/2001/XMLSchema-instance"
    ns_xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:1.0"
    ns_xlink="http://www.w3.org/1999/xlink"
    ns_dem="http://www.opengis.net/citygml/relief/1.0"
    ns_frn="http://www.opengis.net/citygml/cityfurniture/1.0"
    ns_tun="http://www.opengis.net/citygml/tunnel/1.0"
    ns_wtr="http://www.opengis.net/citygml/waterbody/1.0"
    ns_brid="http://www.opengis.net/citygml/bridge/1.0"
    ns_app="http://www.opengis.net/citygml/appearance/1.0"
# Else probably means 2.0
else:
    # Name spaces
    ns_citygml="http://www.opengis.net/citygml/2.0"

    ns_gml = "http://www.opengis.net/gml"
    ns_bldg = "http://www.opengis.net/citygml/building/2.0"
    ns_tran = "http://www.opengis.net/citygml/transportation/2.0"
    ns_veg = "http://www.opengis.net/citygml/vegetation/2.0"
    ns_gen = "http://www.opengis.net/citygml/generics/2.0"
    ns_xsi="http://www.w3.org/2001/XMLSchema-instance"
    ns_xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
    ns_xlink="http://www.w3.org/1999/xlink"
    ns_dem="http://www.opengis.net/citygml/relief/2.0"
    ns_frn="http://www.opengis.net/citygml/cityfurniture/2.0"
    ns_tun="http://www.opengis.net/citygml/tunnel/2.0"
    ns_wtr="http://www.opengis.net/citygml/waterbody/2.0"
    ns_brid="http://www.opengis.net/citygml/bridge/2.0"
    ns_app="http://www.opengis.net/citygml/appearance/2.0"

nsmap = {
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
# Empty lists for cityobjects and buildings
cityObjects = []
buildings = []
other = []

#  This denotes the dictionaries in which the surfaces are put.
output = {}
vertices_output = {}
face_output = {}

# This denotes the dictionaries in which all surfaces are put. It is later ignored in the semantic option was invoked.
output['All'] = []
# output['All'].append(header)
vertices_output['All'] = []
face_output['All'] = []

# If the semantic option was invoked, this part adds additional dictionaries.
if SEMANTICS:
    # Easy to modify list of thematic boundaries
    semanticSurfaces = ['GroundSurface', 'WallSurface', 'RoofSurface', 'ClosureSurface', 'CeilingSurface', 'InteriorWallSurface', 'FloorSurface', 'OuterCeilingSurface', 'OuterFloorSurface', 'Door', 'Window']
    for semanticSurface in semanticSurfaces:
        output[semanticSurface] = []
        # Add the material library
        vertices_output[semanticSurface] = []
        face_output[semanticSurface] = []


# Directory of vertices (indexing)
vertices = {}
vertices['All'] = []
if SEMANTICS:
    for semanticSurface in semanticSurfaces:
        vertices[semanticSurface] = []
vertices['Other'] = []
face_output['Other'] = []
output['Other'] = []

# Find all instances of cityObjectMember and put them in a list
for obj in root.getiterator('{%s}cityObjectMember'% ns_citygml):
    cityObjects.append(obj)

if len(cityObjects) > 0:
    
    # Report the progress and contents of the CityGML file
    print("\tThere are", len(cityObjects), "cityObject(s) in this CityGML file.")
    # Store each building separately
    for cityObject in cityObjects:
        for child in cityObject.getchildren():
            if child.tag == '{%s}Building' %ns_bldg:
                buildings.append(child)
    for cityObject in cityObjects:
        for child in cityObject.getchildren():
            if child.tag == '{%s}Road' %ns_tran or child.tag == '{%s}PlantCover' %ns_veg or \
            child.tag == '{%s}GenericCityObject' %ns_gen or child.tag == '{%s}CityFurniture' %ns_frn or \
            child.tag == '{%s}Relief' %ns_dem or child.tag == '{%s}Tunnel' %ns_tun or \
            child.tag == '{%s}WaterBody' %ns_wtr or child.tag == '{%s}Bridge' %ns_brid:
                other.append(child)
                
    print("\tAnalysing objects and extracting the geometry...")
    
    # Count the buildings
    b_counter = 0
    b_total = len(buildings)
    
    # Do each building separately
    for b in buildings:
        
        b = buildings[0]
        
        # Build the local list of vertices to speed up the indexing
        local_vertices = {}
        local_vertices['All'] = []
        if SEMANTICS:
            for semanticSurface in semanticSurfaces:
                local_vertices[semanticSurface] = []
                
        # Increment the building counter
        b_counter += 1
        
        # If the object option is on, get the name for each building or create one
        if OBJECTS:
            ob = b.xpath("@g:id", namespaces={'g' : ns_gml})
            if not ob:
                ob = b_counter
            else:
                ob = ob[0]
        
        # Print progress for large files every 1000 buildings.
        if b_counter == 1000:
            print("\t1000... "),
        elif b_counter % 1000 == 0 and b_counter == (b_total - b_total % 1000):
            print(str(b_counter) + "...")
        elif b_counter > 0 and b_counter % 1000 == 0:
            print(str(b_counter) + "... "),
        
        # Add the object identifier
        if OBJECTS:
            face_output['All'].append('o ' + str(ob) + '\n')

        # OBJ with all surfaces in the same bin
        gml_Polygons = markup3dmodule.polygonFinder(b)
        # Process each surface
        for poly in gml_Polygons:
            vertex_list = parse_polygon(poly)

