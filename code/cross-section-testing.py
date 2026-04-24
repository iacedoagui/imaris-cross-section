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

count = 3
res = 0

start = datetime.now()
print(f"Started at: {start.strftime('%H:%M:%S')}\n")

#Load file
path = "/mnt/d/Jeremy/20241209_15_52_55_24_014_Hindbrain_lectin488+NeuN_Destripe_DONE/24_014_Lectin488+NeuN647.ims"
print(f"Loading IMS file: {path}\n")

ims_data = ims(path, ResolutionLevelLock=res)

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
z1 = z // 20
z2 = 2 * z // 20
z3 = 3 * z // 20
z4 = 4 * z // 20
z5 = 5 * z // 20
z6 = 6 * z // 20
z7 = 7 * z // 20
z8 = 8 * z // 20
z9 = 9 * z // 20
z10 = 10 * z // 20
z11 = 11 * z // 20
z12 = 12 * z // 20
z13 = 13 * z // 20
z14 = 14 * z // 20
z15 = 15 * z // 20
z16 = 16 * z // 20
z17 = 17 * z // 20
z18 = 18 * z // 20
z19 = 19 * z // 20
y1, y2, y3, y4 = y//5, 2*y//5, 3*y//5, 4*y//5
x1, x2, x3, x4 = x//5, 2*x//5, 3*x//5, 4*x//5

# ims_data[Time?, Channel, Z, Y, X]
for i in range(20):
    volume = [None] * 20

    v0 = None
    v1 = None
    v2 = None
    v3 = None
    v4 = None
    v5 = None
    v6 = None
    v7 = None
    v8 = None
    v9 = None
    v10 = None
    v11 = None
    v12 = None
    v13 = None
    v14 = None
    v15 = None
    v16 = None
    v17 = None
    v18 = None
    v19 = None

    if i == 0:
        v0 = ims_data[0, :, 0:z1, :, :]
    elif i == 1:
        v1 = ims_data[0, :, z1:z2, :, :]
    elif i == 2:
        v2 = ims_data[0, :, z2:z3, :, :]
    elif i == 3:
        v3 = ims_data[0, :, z3:z4, :, :]
    elif i == 4:
        v4 = ims_data[0, :, z4:z5, :, :]
    elif i == 5:
        v5 = ims_data[0, :, z5:z6, :, :]
    elif i == 6:
        v6 = ims_data[0, :, z6:z7, :, :]
    elif i == 7:
        v7 = ims_data[0, :, z7:z8, :, :]
    elif i == 8:
        v8 = ims_data[0, :, z8:z9, :, :]
    elif i == 9:
        v9 = ims_data[0, :, z9:z, :, :]
    elif i == 10:
        v10 = ims_data[0, :, 0:z1, :, :]
    elif i == 11:
        v11 = ims_data[0, :, z1:z2, :, :]
    elif i == 12:
        v12 = ims_data[0, :, z2:z3, :, :]
    elif i == 13:
        v13 = ims_data[0, :, z3:z4, :, :]
    elif i == 14:
        v14 = ims_data[0, :, z4:z5, :, :]
    elif i == 15:
        v15 = ims_data[0, :, z5:z6, :, :]
    elif i == 16:
        v16 = ims_data[0, :, z6:z7, :, :]
    elif i == 17:
        v17 = ims_data[0, :, z7:z8, :, :]
    elif i == 18:
        v18 = ims_data[0, :, z8:z9, :, :]
    elif i == 19:
        v19 = ims_data[0, :, z9:z, :, :]

    volume = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20]



    print(f"\nVolume shape: {volume[i].shape}")  # Should print (c, Z, Y, X)

    # 3. Extract middle cross sections (Orthoslices)
    z_mid = volume[i].shape[1] // 2
    y_mid = volume[i].shape[2] // 2
    x_mid = volume[i].shape[3] // 2

    # XY plane (Z-slice)
    slice_xy = volume[i][:, z_mid, :, :]
    # XZ plane (Y-slice)
    #slice_xz = volume[i][:, :, y_mid, :]
    # YZ plane (X-slice)
    #slice_yz = volume[2][:, :, :, x_mid]

    save_slice(slice_xy, f"24_014_Lectin488+NeuN647_{i}_xy_{count}.tiff")
    #save_slice(slice_xz, f"24_014_Lectin488+NeuN647_{i}_xz_{count}.tiff")
    #save_slice(slice_yz, f"24_014_Lectin488+NeuN647_{i}_yz_{count}.tiff")

end = datetime.now()
print(f"\nFinished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {end - start}")
