# Ivan Acedo Aguilar
from datetime import datetime, timedelta
from tifffile import tifffile
from imaris_ims_file_reader import ims
import numpy as np
import os

#Divide the data from the imaris file into several numpy arrays that I can work with individually.
def get_volume(ims_data):
    
    z = ims_data.shape[2]
    y = ims_data.shape[3]
    x = ims_data.shape[4]

    # Split data into 5 different numpy arrays
    y1, y2, y3, y4 = y//5, 2*y//5, 3*y//5, 4*y//5

    v0 = ims_data[0, 0, :, 0:y1, :]
    v1 = ims_data[0, 0, :, y1:y2, :]
    v2 = ims_data[0, 0, :, y2:y3, :]
    v3 = ims_data[0, 0, :, y3:y4, :]
    v4 = ims_data[0, 0, :, y4:y, :]
    
    return [v0, v1, v2, v3, v4]

def get_slice(slice):
    # Normalize values
    slice_float = slice.astype(np.float32)
    min_val = slice_float.min()
    max_val = slice_float.max()

    if max_val > min_val:
        norm = (slice_float - min_val) / (max_val - min_val)
    else:
        norm = np.zeros_like(slice_float)

    slice_uint16 = (norm * 65535).astype(np.uint16)

    return slice_uint16

def main(path = "", res = 5):
    
    #If the file exists get the file data
    if os.path.exists(path):
        ims_data = ims(path, res)
        print(f"\nImaris file Data Shape = {ims_data.shape}")
    else: 
        print("\nNo valid .ims file")
        return
    
    volume = get_volume(ims_data) #Retrieve a list of numpy arrays containing ims_data
    print(f"\nVolume shape: {volume.shape}")  # Should print (Z, Y, X)
    
    #Do a loop???? or something to iterate through the list and get each one of the slices
    vol_slices = get_slice(volume)
    
    filename = ""
    
    tifffile.imwrite(filename, vol_slices)
    
    return

if __name__ == "__main__":   
     
    #Print starting time
    start = datetime.now()
    print(f"Started at: {start.strftime('%H:%M:%S')}\n")
    
    path = "" #Path to .ims file
    res = 0 # ResolutionLockLevel 0 highest, 8 lowest
    
    main(path, res)