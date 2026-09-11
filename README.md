# QWFI-reconstruction

Python code used for image reconstruction in the manuscript
"Scaling and Accelerating Wide-Field Quantum Imaging with Source-Programmable Control".

The code processes multi-frame EMCCD TIFF stacks using temporal first-and second-order intensity moments. 

For each pixel, the following quantities are calculated:

- First moment: < I >
- Second moment: <I²>
- Temporal variance / zero-lag autocovariance:
  <I²> -  < I >²
- Normalized variance:
  (<I²> - < I >²) / (< I >² + epsilon) 

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

- covariance image

as 32-bit TIFF files.

## Usage

Edit the input file paths and output path in "Cov_Reconstruction.py" then run the code

## Code and example data
The code "Cov_Reconstruction.py" demonstrates the reconstruction algorithm used in the manuscript. Running the code on the provided example TIFF stack generates the reconstructed image as a 32-bit floating-point TIFF.

The example dataset contains a spatially cropped subset of the experimental EMCCD acquisition shown in Fig. 3a of the manuscript and is provided to demonstrate the reconstruction workflow.
