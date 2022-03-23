import numpy as np
from scipy.spatial.transform import Rotation as rotation

def spherical2cartesian(v):
    """
    v[0] = theta - Latitude
    v[1] = phi - Longitude
    """
    
    x = np.cos(v[0]) * np.cos(v[1])  
    y = np.cos(v[0]) * np.sin(v[1])  
    z = np.sin(v[0])  
    
    return [x,y,z]

def cartesian2spherical(v):  
    """
    Take an array of lenght 3 correspoingt to a 3-dimensional vector and returns a array of lenght 2
    with latitade (inclination) and longitude (declination)
    """
    theta = np.arcsin(v[2]) 
    phi = np.arctan2(v[1], v[0])
        
    return [theta, phi]

def GCD_cartesian(cartesian1, cartesian2):
    
    gcd =  np.arccos(np.dot(cartesian1,cartesian2))
    
    return gcd


def StageEP(ep, PPs):
    ''' 
    Given an ep [cartesian] and a APWP [X] with a starting and ending pole, computes the neccesary rotation according to the law of cosines ($\cos{c} = \cos{a} \cos{b} + \sin{a} sin{b} cos{C}$)
    input: an EP [cartesian] and a starting and ending pole,
    output: angle [radians] to rotate the first point to the second by the given EP
    '''
    s = GCD_cartesian(PPs[0], PPs[-1]) # an angular distance between the first and last pole of a track
    p1 = GCD_cartesian(PPs[0], ep) #is a distance between the rotation pole and the first pole of a track 
    p2 = GCD_cartesian(PPs[-1], ep) #is an angular distance between the rotation pole and the last pole of a track. 
    
    w = np.arccos((np.cos(s) - np.cos(p1) * np.cos(p2)) / (np.sin(p1) * np.sin(p2)))
    
    r_positive = rotation.from_rotvec(w * np.array(ep)) 
    rotated_positive = r_positive.apply(PPs[0])
    
    r_negative = rotation.from_rotvec(-w * np.array(ep))
    rotated_negative = r_negative.apply(PPs[0])   
    
    if GCD_cartesian(rotated_positive, PPs[-1]) < GCD_cartesian(rotated_negative, PPs[-1]): #tests wheter or not the rotation has to be inverted.
        return w
    else:
        return -w
    

    
