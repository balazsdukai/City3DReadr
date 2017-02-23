"""
Created on 22 Feb 2017

@author: Balázs Dukai
"""
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Segment_3
from cmath import sqrt

class Polygon(object):
    """
    classdocs
    """
    
    def __init__(self, vertices, gid):
        """
        Constructs a list of CGAL::Point_3 objects that describe the polygon
        Input: list of vertices given as coordinate triplets [[1,2,3],[],...]
        """
        self.id = gid
        self.vertex = []
        for v in vertices:
            self.vertex.append(Point_3(v[0], v[1], v[2])) # x, y, z
    
    def vertex_count(self):
        """
        Return: the number of vertices in the polygon
        """
        
        return self.vertex.__len__()
        
    def area(self):
        """
        Return: the area of the polygon
        """
        
        print("Method not implemented")
    
    def edge_length(self):
        """
        Return: list of edge lengths (complex) in units of the CRS
        """
        edge = []
        for v in range(len(self.vertex)-1): # to prevent index out of range
            edge.append(Segment_3(self.vertex[v], self.vertex[v+1]))
        edge.append(Segment_3(self.vertex[-1], self.vertex[0])) # closing edge
        edge_length = []
        for e in edge:
            # CGAL only computes the squared length of Segment_3
            edge_length.append(sqrt(e.squared_length()))
        
        return edge_length
        
    def NSCP(self):
        """
        Return: number of shape characterising points
        """ 
        
        print("Method not implemented")
        
        