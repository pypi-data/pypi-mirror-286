# velocityvortex

`velocityvortex` is a Python package for calculating the Velocity Autocorrelation Function (VAF) from XML files exported by TrackMate in Fiji/ImageJ. This tool converts tracking data into velocity vectors and computes their autocorrelation over time, helping analyze cell trajectories and dynamics.

## Installation

You can install `velocityvortex` via pip:

```sh
pip install velocityvortex
```

## Velocity Autocorrelation Function (VAF)

A rapidly decreasing velocity autocorrelation function (VAF) suggests that a cell rapidly 'loses' its initial velocity information, possibly due to random interactions with its surroundings. In Brownian motion, where successive displacements are independent of each other, the VAF is zero for any finite time intervals, indicating that there is no retention of past motion.

The Velocity Autocorrelation Function (VAF) is given by:
$$
C_v(t) = \frac{\langle \vec{v}(t + t_0) \cdot \vec{v}(t_0) \rangle}{\langle \vec{v}(t_0) \cdot \vec{v}(t_0) \rangle}
$$

where,
* $\vec{v}(t)$ is the velocity vector at time $t$.
* $\langle \cdot \rangle$ denotes averaging over all particles/cells/tracks.

## Usage

To use `velocityvortex`, import the function and provide it with the path to your TrackMate XML file, the size of the image frame in microns, and the time interval between frames in minutes.

### Example

```python
from velocityvortex import VAF_Siuu

# Replace 'path_to_xml_file.xml' with the path to your XML file
# Replace 100.0 with the size of the image frame in microns
# Replace 0.5 with the time interval between frames in minutes
vaf = VAF_Siuu('path_to_xml_file.xml', 840.2, 3.0)

# The vaf variable now contains the Velocity Autocorrelation Function values
print(vaf)
```

### Parameters

* `xmlfile (str)`: Path to the XML file exported by TrackMate.
* `size_of_frame (float)`: Size of the image frame in microns. This package only supports 2D square images.
* `frame_interval (float)`: Time interval between frames in minutes.

### Output

The function returns a dictionary where:

* __Keys__ are time lags (in minutes).
* __Values__ are the computed Velocity Autocorrelation Function (VAF) for each time lag.

#### Example Output
Here’s an example of the output you might receive from the function:

```python
{
    0: 1.0,
    3: 0.5893349678210232,
    6: 0.4164878945755438,
    9: 0.30983757278577995,
    12: 0.5127183573398707,
    15: 0.3984063745019917,
    18: 0.27398099908060003,
    21: 0.11124731841863349,
    24: 0.161507814894269,
    27: 0.18522659092772978,
    30: 0.18598134932796273,
    33: 0.1877173579927783,
    36: 0.061329343260441704,
    ...
}
```


## Visualizing the Velocity Autocorrelation Function
The following example demonstrates how to visualise Velocity Autocorrelation Function data using matplotlib. This code snippet generates a 2x2 grid of subplots, with each subplot showing different aspects of VAF data and fitted lines.

```python
import matplotlib.pyplot as plt
import numpy as np

# Example VAF data
# Replace these with your actual data
VAF_NK_B = VAF_Siuu('path_to_xml_file_1.xml', 840.2, 3.0)
VAF_NK_S = VAF_Siuu('path_to_xml_file_2.xml', 840.2, 3.0)

plt.style.use('science')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=800)

# Plotting the first subplot
ax1.set_xlabel('Time (min)', fontsize=16)
ax1.set_ylabel('Mean VAF $C_{v}(t)$', fontsize=16)
ax1.set_xlim(0, 240)
ax1.set_ylim(-0.5, 1.2)
ax1.grid(True)
ax1.plot(VAF_NK_B.keys(), VAF_NK_B.values(), linewidth=3, color='DarkRed', label='Experimental Data_NK low density')
ax1.legend(fontsize=16)
ax1.set_title('Experimental Data - NK Low Density')

# Fitting and plotting the log of the mean VAF for the second subplot
Cut_Off_B = int(13)
x_1 = np.array(list(VAF_NK_B.keys()))
y_1 = np.array(list(VAF_NK_B.values()))
k1, c1 = np.polyfit(x_1[:Cut_Off_B], np.log(y_1[:Cut_Off_B]), 1)
g1 = c1 + k1 * x_1

ax2.set_xlabel('Time (min)', fontsize=16)
ax2.set_ylabel('Log of mean VAF $\\ln(C_{v}(t))$', fontsize=16)
ax2.grid(True)
ax2.plot(x_1, np.log(y_1), linewidth=3, color='DarkRed')
ax2.plot(x_1, g1, label=f'$\\ln(C_{{v}}(t))$ = {k1:.3f}t + {c1:.3f}', linewidth=3, color='Orange')
ax2.legend(fontsize=16)
ax2.set_xlim(0, 240)
ax2.set_ylim(-10, 2)
ax2.set_title('Log of Experimental VAF')

# Plotting the third subplot
ax3.set_xlabel('Time (min)', fontsize=16)
ax3.set_ylabel('Mean VAF $C_{v}(t)$', fontsize=16)
ax3.set_xlim(0, 240)
ax3.set_ylim(-0.5, 1.2)
ax3.grid(True)
ax3.plot(VAF_NK_S.keys(), VAF_NK_S.values(), linewidth=3, color='DarkBlue', label='Simulated Data_NK low density')
ax3.legend(fontsize=16)
ax3.set_title('Simulated Data - NK Low Density')

# Fitting and plotting the log of the mean VAF for the fourth subplot
Cut_Off_S = int(13)
x_2 = np.array(list(VAF_NK_S.keys()))
y_2 = np.array(list(VAF_NK_S.values()))
x_2_process = list(x_2[:Cut_Off_S])
y_2_process = list(y_2[:Cut_Off_S])

# Remove negative values
i = 0
while i < len(x_2_process):
    if y_2_process[i] < 0:
        del x_2_process[i]
        del y_2_process[i]
    else:
        i += 1

k2, c2 = np.polyfit(x_2_process, np.log(y_2_process), 1)
g2 = c2 + k2 * x_2

ax4.set_xlabel('Time (min)', fontsize=16)
ax4.set_ylabel('Log of mean VAF $\\ln(C_{v}(t))$', fontsize=16)
ax4.grid(True)
ax4.plot(x_2, np.log(y_2), linewidth=3, color='DarkBlue')
ax4.plot(x_2, g2, label=f'$\\ln(C_{{v}}(t))$ = {k2:.3f}t + {c2:.3f}', linewidth=3, color='SkyBlue')
ax4.legend(fontsize=16)
ax4.set_xlim(0, 240)
ax4.set_ylim(-10, 2)
ax4.set_title('Log of Simulated VAF')

plt.tight_layout()
plt.show()
```

### Explanation
* `plt.style.use('science')`: Applies a scientific style to the plots for a more polished look. You can find more information about the SciencePlots package at SciencePlots on [GitHub](https://github.com/skydvn/SciencePlot-for-Publication) or [PyPI](https://pypi.org/project/SciencePlots/).
* __Subplots__ (`fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=800)`): Creates a 2x2 grid of subplots.
* __Plotting and Customising__: Each subplot is configured with labels, limits, and grid lines. Lines are plotted with different colors and labels for clarity.
* __Fitting and Plotting Lines__: Linear fits are computed for the log-transformed data and plotted with corresponding equations.


### Results
The figure will contain four subplots, with each subplot displaying VAF data, log-transformed data, and fitted lines as specified. Adjust the data and parameters as necessary for your specific use case.

## Acknowledgments
Thanks to Dr. Chenyu Jin, Marie Skłodowska-Curie Postdoctoral Fellow at Uni Luxembourg, for laying the foundational work in recognizing and interpreting the XML files exported from TrackMate. Also, thanks to Dr. Daniel O’Hanlon for introducing Poetry and Mr. Cathal Hosty for his assistance with NK cell time-lapse imaging.

## License
This project is licensed under the MIT License.

MIT License

Copyright (c) 2024 Elephes Sung

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
