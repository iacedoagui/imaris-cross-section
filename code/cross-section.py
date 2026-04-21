from datetime import datetime, timedelta
from tifffile import tifffile
import numpy as np
from PIL import Image
from imaris_ims_file_reader import ims

start = datetime.now()
print(f"Started at: {start.strftime('%H:%M:%S')}\n")

#Load file
path = '/Volumes/Extreme SSD/Ivan/NeuN Af647 3.6x 22_029.ims'
print(f"Loading IMS file: {path}\n")

data = ims(path, ResolutionLevelLock=0)

print(data)
print(f"\nData shape: {data.shape}")
print(f"Data type: {data.dtype}")
print(f"Data dimensions: {data.ndim}")
print(f"Data ResolutionLevelLock: {data.ResolutionLevelLock}")
print(f"Data ResolutionLevels: {data.ResolutionLevels}")
print(f"Data TimePoints: {data.TimePoints}")
print(f"Data Channels: {data.Channels}")
print(f"Data chunks: {data.chunks}")
print(f"Data dimensions: {data.ndim}\n")


volume = data[0, 0, 0:(data.shape[2]-1):2, 0:(data.shape[3]-1):2, 0:(data.shape[4]-1):2]
print(f"\nVolume shape: {volume.shape}")  # Should print (Z, Y, X)


print(f"Min: {volume.min()}, Max: {volume.max()}\n")

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

save_slice(slice_xy, "cross_section_xy_Res_0.tiff")
save_slice(slice_xz, "cross_section_xz_Res_0.tiff")
save_slice(slice_yz, "cross_section_yz_Res_0.tiff")

end = datetime.now()
print(f"\nFinished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {end - start}")
