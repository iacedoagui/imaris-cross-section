import numpy as np
from PIL import Image
from imaris_ims_file_reader.ims import ims

# 1. Load the Imaris file
# Replace 'your_file.ims' with the path to your actual file
ims_path = '../data_files/your_file.ims'
data = ims(ims_path)

# 2. Select specific channel and timepoint if applicable
# data shape is typically (Time, Channel, Z, Y, X)
# Here we take the first timepoint and first channel
volume = data[0, 0, :, :, :]

# 3. Extract middle cross sections (Orthoslices)
z_mid = volume.shape[0] // 2
y_mid = volume.shape[1] // 2
x_mid = volume.shape[2] // 2

# XY plane (Z-slice)
slice_xy = volume[z_mid, :, :]
# XZ plane (Y-slice)
slice_xz = volume[:, y_mid, :]
# YZ plane (X-slice)
slice_yz = volume[:, :, x_mid]

# 4. Save slices as images
def save_slice(array, filename):
    # Normalize to 0-255 for standard image formats if needed
    rescaled = (255.0 / array.max() * (array - array.min())).astype(np.uint8)
    img = Image.fromarray(rescaled)
    img.save(filename)
    print(f"Saved: {filename}")

save_slice(slice_xy, "cross_section_xy.png")
save_slice(slice_xz, "cross_section_xz.png")
save_slice(slice_yz, "cross_section_yz.png")