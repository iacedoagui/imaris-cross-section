# Code for Debugging, stress test and just trying things. Not serious code.
# Ivan Acedo Aguilar

from datetime import datetime, timedelta
from tifffile import tifffile
import numpy as np
from PIL import Image
from imaris_ims_file_reader import ims


def save_cross(array, filename):
    
    slice_float = array.astype(np.float32)

    min_val = np.min(slice_float)
    max_val = np.max(slice_float)

    norm = (slice_float - min_val) / (max_val - min_val)

    slice_uint16 = (norm * 65535).astype(np.uint16)

    tifffile.imwrite(filename, slice_uint16)
    
    #img = Image.fromarray(slice_uint16)
    #img.save(filename)

    print(f"Saved: {filename}")

count = 0
res = 1
n_slices = 20

start = datetime.now()
print(f"Started at: {start.strftime('%H:%M:%S')}\n")

path = "/Volumes/Extreme SSD/Ivan/GLP1_NeuN_9x_missing_DONE.ims"
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

# Split data

z_splits = [i * z // n_slices for i in range(n_slices + 1)]

y_splits = [i * y // n_slices for i in range(n_slices + 1)]

x_splits = [i * x // n_slices for i in range(n_slices + 1)]


# ims_data[Time?, Channel, Z, Y, X]
for i in range(n_slices):
    start_t = datetime.now()
    print(f"\n------->Slice started at: {start_t.strftime('%H:%M:%S')}")

    #slice_vol = ims_data[0, :, z_splits[i]:z_splits[i+1], :, :]
    slice_vol = ims_data[0, :, :, y_splits[i]:y_splits[i+1], :]
    #slice_vol = ims_data[0, :, :, :, x_splits[i]:x_splits[i+1]]
    


    print(f"\nVolume shape: {slice_vol.shape}")  #(c, Z, Y, X)
    
    slice_vol = np.transpose(slice_vol,(0,2,1,3)) #Y
    #slice_vol = np.transpose(slice_vol,(0,3,1,2)) #X
    print(f"\nTransposed volume shape: {slice_vol.shape}")  #(c, Z, Y, X)

    mid = slice_vol.shape[1] // 2
    
    #slice_xy = slice_vol[:, mid:mid+15, :, :]# (Z-slice)
    #slice_xy = slice_xy.max(axis=1)
    
    slice_xz = slice_vol[:, mid:mid+15, :] # (Y-slice)
    slice_xz = slice_xz.max(axis=1)
    
    #slice_yz = slice_vol[:, mid:mid+15, :, :]# (X-slice)
    #slice_yz = slice_yz.max(axis=1)

    #save_cross(slice_xy, f"GLP1_NeuN_9x_{i}_xy_{count}.tiff")
    save_cross(slice_xz, f"GLP1_NeuN_9x_{i}_xz_{count}.tiff")
    #save_cross(slice_yz, f"GLP1_NeuN_9x_{i}_yz_{count}.tiff")

    del slice_vol

    end_t = datetime.now()
    print(f"Slice finished at: {end_t.strftime('%H:%M:%S')}")
    print(f"Total slice time: {end_t - start_t}<-------\n")

end = datetime.now()
print(f"\nFinished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {end - start}")
