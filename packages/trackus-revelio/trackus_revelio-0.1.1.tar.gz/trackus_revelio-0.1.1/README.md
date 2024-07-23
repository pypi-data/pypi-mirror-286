# TrackusRevelio

`TrackusRevelio` is a Python package designed to unravel and extract tracks from XML files exported by TrackMate in Fiji/ImageJ. This tool helps in converting the XML data into a Python dictionary for further analysis and processing.

## Installation

You can install `trackus_revelio` via pip:

```sh
pip install trackus-revelio
```

## Usage
First, import the TrackusRevelio function from the trackus_revelio package. Then, use it to parse an XML file and extract the track data into a dictionary.

### Example

```python
from trackus_revelio import TrackusRevelio

# Replace 'path_to_xml_file.xml' with the path to your XML file
tracks = TrackusRevelio('path_to_xml_file.xml')

# The tracks variable is now a dictionary containing the track data
print(tracks)
```
### Output Structure

```python
{
    '0': {
        'nSpots': 20,
        'trackData': numpy.array([[t1, x1, y1, z1], [t2, x2, y2, z2], ...])
    },
    '1': {
        'nSpots': 15,
        'trackData': numpy.array([[t1, x1, y1, z1], [t2, x2, y2, z2], ...])
    },
    ...
}
```
Each key in the dictionary represents a track ID. The value is another dictionary with two keys:

nSpots: The number of spots (detections) in the track.
trackData: A NumPy array where each row represents a detection with four columns: time (t), x-coordinate (x), y-coordinate (y), and z-coordinate (z).

## Acknowledgments

Special thanks to Chenyu JIN, Marie Skłodowska-Curie Postdoctoral Fellow at Uni Luxembourg, who laid the foundation of this code and helped overcome the challenges with the XML files exported from TrackMate.
