from datetime import datetime, timedelta
import numpy as np
from PIL import Image
from imaris_ims_file_reader import ims

start = datetime.now()
print(f"Started at: {start.strftime('%Y-%m-%d %H:%M:%S')}")

#Load file
path = '/Volumes/Extreme SSD/Ivan/NeuN Af647 3.6x 22_029.ims'
print(f"Loading IMS file: {path}")

data = ims(path, ResolutionLevelLock=5)
print(f"Data shape: {data.shape}")  # Should print (C, T, Z, Y, X)

print(data)

print(data.dtype)  # Check data typex
volume = data[0, 0, 0:2235:200, 0:2997:200, 0:3738:200]
print(f"Volume shape: {volume.shape}")  # Should print (Z, Y, X)

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

end = datetime.now()
print(f"Finished at: {end.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total time: {end - start}")
