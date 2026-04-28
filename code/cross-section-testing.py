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

count = 5
res = 0
n_slices = 70

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

z_splits = [i * z // n_slices for i in range(n_slices + 1)]

y1, y2, y3, y4 = y//5, 2*y//5, 3*y//5, 4*y//5
x1, x2, x3, x4 = x//5, 2*x//5, 3*x//5, 4*x//5

# ims_data[Time?, Channel, Z, Y, X]
for i in range(20):
    start_t = datetime.now()
    print(f"\n------->Slice started at: {start_t.strftime('%H:%M:%S')}")

    slice_vol = ims_data[0, :, z_splits[i]:z_splits[i+1], :, :]

    print(f"\nVolume shape: {slice_vol.shape}")  # Should print (c, Z, Y, X)

    # 3. Extract middle cross sections (Orthoslices)
    z_mid = slice_vol.shape[1] // 2
    y_mid = slice_vol.shape[2] // 2
    x_mid = slice_vol.shape[3] // 2

    # XY plane (Z-slice)
    slice_xy = slice_vol[:, z_mid:z_mid+15, :, :]
    # XZ plane (Y-slice)
    #slice_xz = volume[i][:, :, y_mid, :]
    # YZ plane (X-slice)
    #slice_yz = volume[2][:, :, :, x_mid]
    
    slice_xy = slice_xy.max(axis=1)

    save_slice(slice_xy, f"24_014_Lectin488+NeuN647_{i}_xy_{count}.tiff")
    #save_slice(slice_xz, f"24_014_Lectin488+NeuN647_{i}_xz_{count}.tiff")
    #save_slice(slice_yz, f"24_014_Lectin488+NeuN647_{i}_yz_{count}.tiff")

    del slice_vol

    end_t = datetime.now()
    print(f"Slice finished at: {end_t.strftime('%H:%M:%S')}")
    print(f"Total slice time: {end_t - start_t}<-------\n")

end = datetime.now()
print(f"\nFinished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {end - start}")
