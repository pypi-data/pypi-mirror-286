import xml.etree.ElementTree as et
import numpy as np

def TrackusRevelio(xmlfile, size_of_frame, frame_interval):
    """ 
    Load xml files into a python dictionary with the following structure:
        tracks = {'0': {'nSpots': 20, 'trackData': numpy.array(t, x, y, z) }}
    Tracks should be xml file from 'Export tracks to XML file',
    that contains only track info but not the features.
    Similar to what 'importTrackMateTracks.m' needs.
    """
    try:
        tree = et.parse(xmlfile)
    except OSError:
        print('Failed to read XML file {}.'.format(xmlfile))
        return {}
    
    root = tree.getroot()
    nTracks = int(root.attrib['nTracks'])
    tracks = {}
    
    for i in range(nTracks):
        trackIdx = str(i)
        tracks[trackIdx] = {}
        nSpots = len(root[i].findall('detection'))
        tracks[trackIdx]['nSpots'] = nSpots
        trackData = np.array([]).reshape(0, 4)
        
        for j in range(nSpots):
            t = float(root[i][j].attrib['t'])
            x = float(root[i][j].attrib['x'])
            y = float(root[i][j].attrib['y'])
            z = float(root[i][j].attrib['z'])
            spotData = np.array([t, x, y, z])
            trackData = np.vstack((trackData, spotData))
        
        tracks[trackIdx]['trackData'] = trackData
    
    lenth_of_frame = size_of_frame
    # multiplier = 1331.20/1024
    Displacement_Matrix = {}
    Number_Of_Particles = len(tracks)
    for i in range(Number_Of_Particles):
        Coordinates_Matrix = tracks[str(i)]['trackData']
        Number_Of_Coordinates = len(Coordinates_Matrix)
        displacement = []
        for j in range(Number_Of_Coordinates):
            if j < Number_Of_Coordinates - 1:
                delta_x = abs(Coordinates_Matrix[j+1][1]-Coordinates_Matrix[j][1])
                delta_y = abs(Coordinates_Matrix[j+1][2]-Coordinates_Matrix[j][2])
                delta_x = min(delta_x, lenth_of_frame - delta_x)
                delta_y = min(delta_y, lenth_of_frame - delta_y)
                displace = np.sqrt(delta_x ** 2 + delta_y ** 2)
                displacement.append(displace)
        # displacement = [pixels * multiplier for pixels in displacement]
        Displacement_Matrix[str(i)] = displacement
    
    Speed_Martrix = {}
    for particles in range(len(Displacement_Matrix)):
        displacement = Displacement_Matrix[str(particles)]
        speed = [dis / frame_interval for dis in displacement]
        Speed_Martrix[str(particles)] = speed
    
    inst_speed_list = []
    for cells in range(len(Speed_Martrix)):
         ins_speed = Speed_Martrix[str(cells)]
         inst_speed_list = inst_speed_list + ins_speed
    return inst_speed_list
