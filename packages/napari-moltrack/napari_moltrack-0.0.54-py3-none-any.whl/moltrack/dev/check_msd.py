import trackpy as tp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy.spatial.distance import squareform, pdist
import pickle
import time
from numba import njit
import trackpy



path = r"D:\1 Rho-PAmCherry FOV\24-05-02 RhoPAM-plasmid-NusGsfGFP poorM9_17.03.43_18_Channel1_moltrack_tracks.csv"
path = r"D:\1 Rho-PAmCherry FOV\24-05-02 RhoPAM-plasmid-NusGsfGFP poorM9_17.03.43_18_dataset_channel_moltrack_tracks.csv"

df = pd.read_csv(path, sep=",")

pixel_size_nm = 100
pixel_size_um = 100 *1e-3
exposure_time_ms = 10
exposure_time_s = exposure_time_ms * 1e-3
fps = 1 / exposure_time_s

mpp = pixel_size_um

for particle in df.particle.unique():
    
    particle_df = df[df.particle == particle].copy()
    particle_df = particle_df[["particle", "frame", "x", "y"]]
    
    msd = trackpy.motion.msd(particle_df, mpp, fps, len(particle_df))
    
    break