# qwfi-reconstruction
Python code for camera-based quantum wide-field image reconstruction using spatial photon correlations.

# QWFI reconstruction

Python code used for image reconstruction in the manuscript
"Scaling and Accelerating Wide-Field Quantum Imaging with Source-Programmable Control".

The code processes multi-frame EMCCD TIFF stacks using temporal first-
and second-order intensity moments.

For each pixel, the following quantities are calculated:

- First moment: <I>
- Second moment: <I²>
- Temporal variance / zero-lag autocovariance:
  <I²> - <I>²
- Normalized variance:
  (<I²> - <I>²) / (<I>² + epsilon) 

Large TIFF stacks are processed in batches to limit memory usage.

## Requirements

- Python 3.10 or newer
- NumPy
- tifffile
- Matplotlib

## Input

Multi-frame TIFF stacks with dimensions:

frames × height × width

## Output

The script saves:

- mean intensity image
- second-moment image
- variance image
- normalized variance image

as 32-bit TIFF files.

## Usage

Edit the input file paths and output path in `reconstruction.py`,
then run:

python reconstruction.py
