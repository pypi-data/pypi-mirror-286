import xml.etree.ElementTree as et
import numpy as np

def TrackusRevelio(xmlfile):
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
    
    return tracks
