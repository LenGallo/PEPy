import numpy as np
from scipy.spatial.transform import Rotation as rotation


def generate_APWP_segment_noiseless(PPs, ep, omega):
    """
    Generates a np.array of N_total paleomagnetic poles following the motion of a
    random governing EP (stable in time) 
    
    -- Parameters:
    PPs = number of PPs or time (Ma) - one pole each 1Ma
    ep = Cartesian coordinates [x,y,z] if the euler pole.
    omega = angular velocity (in radians per Ma)      
    """               
    
    pp = [0,0,-1] #the [i=0] first PP represents the south pole 
    PP = np.array(pp) 
    r = rotation.from_rotvec(omega * np.array(ep))    
    
    for i in range(PPs): 
        pp = r.apply(pp) # new pp without noise                
        PP = np.vstack((PP, np.array(pp)))                           
    
    return PP