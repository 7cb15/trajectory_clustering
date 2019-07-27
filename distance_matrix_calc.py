import scipy.io
import math
import numpy as np
import sys
import pickle
import pandas as pd
from scipy.spatial.distance import directed_hausdorff


def load_one_traj(file):
    '''function for loading the trajectories to calculate distances against'''
    with open(file,'rb') as fp: 
        traj = pickle.load(fp)        
    
    traj_np = []
    for i in traj:
        new_strut = np.asarray(i)
        traj_np.append(new_strut)
        
    return traj_np

#Create distance matrix
def hausdorff(u, v):
    '''distance function to populate dissimilarity matrix'''
    d = directed_hausdorff(u, v)[0]
    return d

def distance_matrix(traj_lst_np):
    '''calculate symmetric distance matrix'''
    traj_count = len(traj_lst_np)
    D = np.zeros((traj_count, traj_count)) #creates a matrix of 1900 x 1900

    #loop through each trajectory and calcuate the distnace to all the other trajectories
    for i in range(traj_count):
        for j in range(i + 1, traj_count):
            distance = hausdorff(traj_lst_np[i], traj_lst_np[j])
            D[i, j] = distance
            D[j, i] = distance
            
    return D

file = sys.argv[0]
file_name = sys.argv[1]

traj_lst_np = load_one_traj(file)
print("trajectory loaded")
print("calculating distance matrix")
D = distance_matrix(traj_lst_np)
print("distance matrix calculated")

np.save(file_name,D)
print("file saved")