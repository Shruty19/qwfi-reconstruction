# ===============================================================
# Covariance reconstruction
# Author: Shruti Sundar
#
# Description:
#   Processes multi-frame TIFF stacks acquired under one
#   experimental condition and calculates the pixel-wise
#   temporal variance:
#
#       Var[I] = <I^2> - <I>^2
#
#   Large TIFF stacks are processed in batches to limit
#   memory usage.
#
# Input:
#   One or more multi-frame TIFF stacks
#
# Output:
#   One 32-bit TIFF containing the reconstructed variance image
# ===============================================================

from pathlib import Path
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt

# TIFF stacks
input_stacks = [
    Path("example_data/stack_01.tif"),
    Path("example_data/stack_02.tif"),
]

# Optional dark-frame stack
# Set to None if dark subtraction is not used
dark_stack = None

output_dir = Path("example_output")
output_filename = "covariance_reconstruction.tif"

# Number of frames loaded into memory
batch_size = 500

# Clip negative values after dark subtraction
clip_negative = True
show_result = True


# LOAD DARK-FRAME
dark_mean = None

if dark_stack is not None:

    dark_stack = Path(dark_stack)

    dark = tiff.imread(dark_stack).astype(np.float32)

    if dark.ndim == 2:
        dark = dark[np.newaxis, ...]

    dark_mean = np.mean(
        dark,
        axis=0,
        dtype=np.float64
    )

    print("Dark-frame reference loaded.")

else:
    print("No dark-frame subtraction applied.")

# INPUT FILES CHECK
if len(input_stacks) == 0:
    raise ValueError("No input TIFF stacks were provided.")

for stack_path in input_stacks:

    if not stack_path.exists():
        raise FileNotFoundError(
            f"Input stack not found: {stack_path}"
        )

# IMAGE DIMENSIONS CHECK
with tiff.TiffFile(input_stacks[0]) as tif:

    first_frame = tif.pages[0].asarray()

if first_frame.ndim != 2:
    raise ValueError(
        "Each TIFF frame must be a two-dimensional image."
    )

height, width = first_frame.shape

print(f"Image dimensions: {height} x {width}")
print(f"Number of TIFF stacks: {len(input_stacks)}")
print(f"Batch size: {batch_size}")

# INITIALIZE ACCUMULATORS
sum_intensity = np.zeros(
    (height, width),
    dtype=np.float64
)

sum_squared_intensity = np.zeros(
    (height, width),
    dtype=np.float64
)

total_frames = 0

# PROCESS STACKS
for stack_path in input_stacks:

    print(f"\nProcessing: {stack_path}")

    with tiff.TiffFile(stack_path) as tif:

        n_frames = len(tif.pages)

        if n_frames == 0:
            raise ValueError(
                f"No frames found in: {stack_path}"
            )

        total_frames += n_frames

        for start in range(
            0,
            n_frames,
            batch_size
        ):

            end = min(
                start + batch_size,
                n_frames
            )

            batch = np.stack(
                [
                    tif.pages[i].asarray()
                    for i in range(start, end)
                ],
                axis=0
            ).astype(np.float32)


            if batch.shape[1:] != (height, width):

                raise ValueError(
                    f"Image dimensions in {stack_path} "
                    "do not match the first TIFF stack."
                )


            # dark subtraction

            if dark_mean is not None:

                batch = (
                    batch
                    - dark_mean[np.newaxis, :, :]
                )

                if clip_negative:

                    batch = np.clip(
                        batch,
                        0,
                        None
                    )


            # Accumulate temporal moments

            sum_intensity += np.sum(
                batch,
                axis=0,
                dtype=np.float64
            )

            sum_squared_intensity += np.sum(
                batch * batch,
                axis=0,
                dtype=np.float64
            )

            print(
                f"  Processed frames "
                f"{start + 1}-{end}"
            )


print(
    f"\nTotal frames processed: "
    f"{total_frames}"
)

# CALCULATE COVARIANCE
mean_image = (
    sum_intensity
    / total_frames
)

second_moment = (
    sum_squared_intensity
    / total_frames
)

variance_image = (
    second_moment
    - mean_image**2
)


# Negative values clipped to zero.
variance_image = np.clip(
    variance_image,
    0,
    None
)

variance_image = variance_image.astype(
    np.float32
)

# SAVE RECONSTRUCTED FILE
output_dir.mkdir(
    parents=True,
    exist_ok=True
)

output_path = (
    output_dir
    / output_filename
)

tiff.imwrite(
    output_path,
    variance_image
)

print(
    f"\nCovariance reconstruction saved to:"
    f"\n{output_path}"
)

# DISPLAY RECONSTRUCTION
if show_result:

    plt.figure(
        figsize=(7, 7)
    )

    plt.imshow(
        variance_image,
        cmap="gray"
    )

    plt.title(
        "Covariance reconstruction"
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()

