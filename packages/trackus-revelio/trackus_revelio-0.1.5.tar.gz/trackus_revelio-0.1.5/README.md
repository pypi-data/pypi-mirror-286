# TrackusRevelio

`TrackusRevelio` is a Python package designed to unravel and extract tracks from XML files exported by TrackMate in Fiji/ImageJ. This tool helps in converting the XML data into a Python list containing the instaneous speeds of the particles/cells/tracks for further analysis and processing.

## Installation

You can install `trackus_revelio` via pip:

```sh
pip install trackus-revelio
```

## Usage
First, import the TrackusRevelio function from the trackus_revelio package. Then, use it to parse an XML file and extract the instaneous speeds into a list.

### Example

```python
from trackus_revelio import TrackusRevelio

# Replace 'path_to_xml_file.xml' with the path to your XML file
# size_of_frame should be the one-dimensional size of the image frame in microns
# frame_time should be the time interval between each frame in minutes
Speeds = TrackusRevelio('path_to_xml_file.xml', size_of_frame=1331.20, frame_interval=3.0)

# Output is a list containing the speeds data
print(Speeds)
```
### Parameters
* `xmlfile (str)`: Path to the XML file exported by TrackMate.
* `size_of_frame (float)`: One-dimensional size of the image frame in microns. This value can usually be found at the top of the images when opened in Fiji/ImageJ. This package is only applicable to square images with equal length and width.
* `frame_time (float)`: Time interval between each frame in minutes. This is the time duration captured between two consecutive frames in your image sequence.


### Output Structure

The function `TrackusRevelio` returns a list of instantaneous speeds for all particles. Each particle's speed is calculated based on the distance traveled between consecutive frames and the given frame time.

__Example Output__
The output speeds list will contain the instantaneous speeds for all particles:

```python
[2.3, 3.1, 4.0, 2.8, ...]
```

## Acknowledgments

Special thanks to Dr. Chenyu Jin, Marie Skłodowska-Curie Postdoctoral Fellow at Uni Luxembourg, who laid the foundation for recognising the XML files exported from TrackMate. Also, thanks to Dr. Daniel O’Hanlon for introducing Poetry.


## License

This project is licensed under the MIT License.

Copyright (c) 2024 [Elephes Sung]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Contact

For any suggestion, please contact: eu23@ic.ac.uk
Many Thanks.
