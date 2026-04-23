# Code for Debugging, stress test and just trying things. Not serious code.
# Ivan Acedo Aguilar

from datetime import datetime, timedelta
from tifffile import tifffile
import numpy as np
from PIL import Image
from imaris_ims_file_reader import ims

# 4. Save slices as images
def save_slice(array, filename):
    # Convert to float for safe normalization
    slice_float = array.astype(np.float32)

    # Normalize to 0–1
    min_val = np.min(slice_float)
    max_val = np.max(slice_float)

    if max_val > min_val:
        norm = (slice_float - min_val) / (max_val - min_val)
    else:
        norm = np.zeros_like(slice_float)

    # Scale to uint16
    slice_uint16 = (norm * 65535).astype(np.uint16)

    # Save as TIFF
    tifffile.imwrite(filename, slice_uint16)
    
    #img = Image.fromarray(slice_uint16)
    #img.save(filename)

    print(f"Saved: {filename}")


start = datetime.now()
print(f"Started at: {start.strftime('%H:%M:%S')}\n")

#Load file
path = "/mnt/e/IMS NeuN For Ivan - MQ/GLP1_NeuN_9x_missing_DONE.ims"
print(f"Loading IMS file: {path}\n")

ims_data = ims(path, ResolutionLevelLock=2)

print(ims_data)
print(f"\nData shape: {ims_data.shape}")
print(f"Data type: {ims_data.dtype}")
print(f"Data dimensions: {ims_data.ndim}")
print(f"Data ResolutionLevelLock: {ims_data.ResolutionLevelLock}")
print(f"Data ResolutionLevels: {ims_data.ResolutionLevels}")
print(f"Data TimePoints: {ims_data.TimePoints}")
print(f"Data Channels: {ims_data.Channels}")
print(f"Data chunks: {ims_data.chunks}")
print(f"Data dimensions: {ims_data.ndim}\n")


#volume = data[0, 0, 0:(data.shape[2]-1):2, 0:(data.shape[3]-1):2, 0:(data.shape[4]-1):2]


z = ims_data.shape[2]
y = ims_data.shape[3]
x = ims_data.shape[4]

# Split data into 5 different numpy arrays
z1, z2, z3, z4 = z//5, 2*z//5, 3*z//5, 4*z//5
y1, y2, y3, y4 = y//5, 2*y//5, 3*y//5, 4*y//5
x1, x2, x3, x4 = x//5, 2*x//5, 3*x//5, 4*x//5

# ims_data[Time?, Channel, Z, X?, Y]
v0 = 0 #ims_data[0, 0, :, , 0:y1]
v1 = 0 #ims_data[0, 0, :, : y1:y2]
v2 = ims_data[0, :, :, :, x2:x3]
v3 = 0 #ims_data[0, 0, :, :, y3:y4]
v4 = 0 #ims_data[0, 0, :, :, y4:y]

volume = [v0, v1, v2, v3, v4]


#print(f"\nVolume shape: {volume.shape}")  # Should print (Z, Y, X)


print(f"Min: {volume[2].min()}, Max: {volume[2].max()}\n")

# 3. Extract middle cross sections (Orthoslices)
z_mid = volume[2].shape[1] // 2
y_mid = volume[2].shape[2] // 2
x_mid = volume[2].shape[3] // 2

# XY plane (Z-slice)
#slice_xy = volume[2][:, z_mid]
# XZ plane (Y-slice)
#slice_xz = volume[2][:, :, y_mid]
# YZ plane (X-slice)
slice_yz = volume[2][:, :, :, x_mid]

#save_slice(slice_xy, "cross_section_xy_Res_0_Num_2.tiff")
#save_slice(slice_xz, "cross_section_xz_Res_0_Num_2_Channel 4.tiff")
save_slice(slice_yz, "cross_section_yz_Res_0_Num_2_W_.tiff")

print(f"Data is a Numpy array = {isinstance(ims_data, np.ndarray)}")
print(f"Volume is a Numpy array = {isinstance(volume, np.ndarray)}")

end = datetime.now()
print(f"\nFinished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {end - start}")
