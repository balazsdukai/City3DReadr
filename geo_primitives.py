#!/usr/bin/env python
# coding=utf-8

class Point(object):

    def __init__(self):
        self.pos = (0,0,0)
        self.fid = list()
        self.polyid = list()

    def set_pos(self,pos):
        self.pos = pos

    def add_fid(self,fid):
        self.fid.append(fid)

    def add_polyid(self,polyid):
        self.polyid.append(polyid)

class Polygon(object):

    def __init__(self):
        self.poslist = list()
        self.fid = list()
        self.polyid = "None" 
        self.role = "None" 
        self.valid = True
        self.validinfo = "None"
        self.orientation = 360
        self.planar = True

    def set_role(self,role):
        if role==None:
            return
        if type(role) == 'NoneType':
            return
        self.role = role

    def set_poslist(self,poslist):
        self.poslist = poslist

    def add_fid(self,fid):
        self.fid.append(fid)

    def set_polyid(self,polyid):
        self.polyid = polyid

    def add_pos(self,pos):
        self.poslist.append(pos)

    def set_valid(self,valid_flag):
        self.valid = valid_flag

    def set_validinfo(self,validinfo):
        self.validinfo = validinfo

    def set_orientation(self,orientation):
        self.orientation = orientation

    def set_planar(self,planar):
        self.planar = planar

    # def det(a):
    #     return a[0][0]*a[1][1]*a[2][2] + a[0][1]*a[1][2]*a[2][0] + a[0][2]*a[1][0]*a[2][1] - a[0][2]*a[1][1]*a[2][0] - a[0][1]*a[1][0]*a[2][2] - a[0][0]*a[1][2]*a[2][1]

    # def unit_normal(a,b,c):
    #     x = det([[1,a[1],a[2]],
    #              [1,b[1],b[2]],
    #              [1,c[1],c[2]]])

    #     y = det([[1,a[1],a[2]],
    #              [1,b[1],b[2]],
    #              [1,c[1],c[2]]])

    #     z = det([[1,a[1],a[2]],
    #              [1,b[1],b[2]],
    #              [1,c[1],c[2]]])
        
    #     magnitude = (x**2 + y**2 + z**2)**.5
    #     if magnitude == 0.0:
    #         raise ValueError("no magnitude")
    #     return (x/magnitude, y/magnitude, z/magnitude)

    # def orient(self):
    #     self.normal = self.unit_normal(self.poslist[0][0],self.poslist[0][1],self.poslist[0][2])
    #     return self.normal

class Shell(object):
    
    def __init__(self):
        self.polylist = list()
        self.shellid = "None"
        self.fid = "None"
        self.role = "None"

    def add_poly(self,poly):
        self.polylist.append(poly)

    def set_shellid(self,shellid):
        self.shellid = shellid

    def set_fid(self,fid):
        self.fid = fid

    def set_role(self,role):
        self.role = role

class Solid(object):

    def __init__(self):
        self.shelllist = list()
        self.solidid = "None"
        self.fid = "None"
        self.role = "None"

    def add_shell(self,shell):
        self.shelllist.append(shell)
    
    def set_solidid(self,solidid):
        self.solidid = solidid

    def set_fid(self,fid):
        self.fid = fid

    def set_role(self,role):
        self.role = role

class Feature(object):
    
    def __init__(self):
        self.solids = list()
        self.surfaces = list()
        self.fid = "None"

    def add_solid(self,solid):
        self.solids.append(solid)

    def add_surfaces(self,surfaces):
        self.surfaces.append(surfaces)

    def set_fid(self,fid):
        self.fid = fid

class Building(Feature):

    def __init__(self):
        self.solids = list()
        self.surfaces = list()
        self.fid = None
        self.buildingparts = list()
        self.invalidpolys = list()
    
    def add_buildingpart(self,buildingpart):
        self.buildingparts.append(buildingpart)

    def add_invalidpoly(self,poly):
        self.invalidpolys.append(poly)
