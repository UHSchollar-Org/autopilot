from source.ia.heuristics.heuristic import heuristic
from source.environment._map import *

from typing import List
import random as rd
import numpy as np

class k_means(heuristic):
    def evaluate(self, intersections : List, cluster_count : int, max_iterations : int) -> List:
        """The K-means algorithm is a simple and classical distance-based clustering algorithm. It uses the distance as a similarity 
        evaluation index, that is, the closer the distance between two objects, the similar the higher the degree.

        Args:
            intersections (List[intersection]): List of nodes representing the data set to be partitioned
            cluster_count (int): The number of clusters to form as well as the number of centroids to generate.
            max_iterations (int): Maximum number of iterations of the k-means algorithm for a single run.

        Returns:
            List[intersection]: List of the centroid nodes of the partitions
        """
        #variable initialization
        self.cluster_count = cluster_count
        self.init_clusters()
        self.intersection_cluster : Dict[intersection, int] = {} 
        for _intersection in intersections:
            self.intersection_cluster[_intersection] = 0
            
        #k group centroid points are randomly selected
        self.centroids = self.get_random_centroids(intersections)
        self.assigning_cluster(intersections)
        
        #parameters to measure convergence
        time = 0
        self.tolerance = 0.001
        self.cluster_changed = True
        self.centroid_changed = True
        
        #It is iterated until one of the convergence parameters is correct.
        while time < max_iterations and self.cluster_changed and self.centroid_changed:
            new_centroids = self.recalculate_centroids()
            self.centroid_changed = self.check_centroid_change(new_centroids)
            self.centroids = new_centroids
            self.assigning_cluster(intersections)
            
        return self.centroids
            
    def init_clusters(self):
        self.clusters : List[List[intersection]] = [] 
        for _ in range(self.cluster_count):
            self.clusters.append([])
            
    def assigning_cluster(self, intersections : List):
        """Each node is assigned to the partition that has 
        the centroid with the least distance.

        Args:
            intersections (List[intersection]): Nodes to analyze
        """
        from source.tools.general_tools import distance_from_geo_coord
        cluster_change = False
        self.init_clusters()
        for intersection in intersections:
            shorter_distance = np.inf
            best_cluster = -1
            for i in range(self.cluster_count):
                distance = distance_from_geo_coord(intersection.geo_coord, self.centroids[i].geo_coord)
                if distance < shorter_distance:
                    best_cluster = i
                    shorter_distance = distance
            if self.intersection_cluster[intersection] != best_cluster:
                cluster_change = True
                self.intersection_cluster[intersection] = best_cluster
                self.clusters[best_cluster].append(intersection) 
            else:
                self.clusters[best_cluster].append(intersection)
        self.cluster_changed = cluster_change
        
    def get_random_centroids(self, intersections : List) -> List:
        """Generate the first k random centroids

        Args:
            intersections (List[intersection]): Nodes to analyze

        Returns:
            List[intersection]: Random centroids
        """
        centroids = []
        for i in range(self.cluster_count):
            new_centroid = None
            while new_centroid == None:
                rnd = rd.randint(0,len(intersections)-1)
                new_centroid = intersections[rnd]
                try:
                    centroids.index(new_centroid)
                    new_centroid = None
                except:
                    centroids.append(new_centroid)
        return centroids
    
    def recalculate_centroids(self) -> List:
        """Analyze the new centroids of the clusters

        Returns:
            List[intersection]: List of new centroids
        """
        new_centroids : List[intersection] = []
                
        for cluster in self.clusters:
            lat_sum = 0
            lon_sum = 0
            for _intersection in cluster:
                lat_sum += _intersection.geo_coord[0]
                lon_sum += _intersection.geo_coord[1]
            centroid_coord = (lat_sum/len(cluster), lon_sum/len(cluster))
            new_centroids.append(self.nearest_intersection(centroid_coord,cluster))
        return new_centroids
    
    def nearest_intersection(self, coordenates : tuple, cluster : List):
        """Given a tuple of geographic coordinates, returns the nearest map node.
        """
        from source.tools.general_tools import distance_from_geo_coord
        lower_distance = np.inf
        nearest_intersection = None
        
        for _intersection in cluster:
            distance = distance_from_geo_coord(coordenates, _intersection.geo_coord)
            if distance < lower_distance:
                lower_distance = distance
                nearest_intersection = _intersection
                
        return nearest_intersection
    
    def check_centroid_change(self, new_centroids : List) -> bool:
        """Check if in the last iteration there was any centroid change

        Args:
            new_centroids (List[intersection]): New centroids to compare with those of the previous iteration

        Returns:
            bool: True if there was a change
        """
        for i in range(len(new_centroids)):
            lat_dif = abs(self.centroids[i].geo_coord[0] - new_centroids[i].geo_coord[0])
            lon_dif = abs(self.centroids[i].geo_coord[1] - new_centroids[i].geo_coord[1])
            if lat_dif > self.tolerance or lon_dif > self.tolerance:
                break
            if i == len(new_centroids)-1:
                return False
        return True