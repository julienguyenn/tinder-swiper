import subprocess
import pandas as pd
import numpy as np

def process_pics(in_file="", in_dir="") -> None:
    args = ['OpenFace_2.2.0_win_x64/FaceLandmarkImg.exe']
    
    if in_file and not in_dir:
        args += ['-f', in_file]
    elif not in_file and in_dir:
        args += ['-fdir', in_dir]
        
    subprocess.run(args, stdout=subprocess.DEVNULL)
    
def extract_array(in_csv: str) -> np.array:
    pass
    
def compare(base: np.array, comparison: np.array) -> float:
    """ Returns the l2 distance between landmark arrays of base and 
        comparison. Returns lowest distance if there are multiple
        faces and -1 if no faces.
    """
    if len(comparison.shape) == 1:
        dist = base - comparison
        
        return np.dot(dist, dist)
    
    elif not comparison:
        return -1
    
    else:
        dist = 1000000
        
        for row in comparison:
            pass
    
process_pics(in_dir='images/comparison')