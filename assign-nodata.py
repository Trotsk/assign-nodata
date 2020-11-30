"""Takes a directory of GeoTIFF files and reassigns NoData value
according to user input

Solves issue of requiring Spatial Analyst extension to perform
the same task in ArcGIS
"""

from osgeo import gdal
import os
import glob
import numpy as np
import rasterio


dir = input('What is the full path of your TIF files? \n > ')
try:
    os.chdir(dir)
except:
    raise ValueError('Invalid directory')

filenames = glob.glob('*.tif')                                  # find TIF files and pass to list

try:
    new_ndval = int(input('NoData value: '))
except TypeError:
    print('Must be an integer')

def nodata_val():
    """returns NoData value currently assigned to TIF files"""
    with rasterio.open(filenames[0]) as src:
        return src.nodata

for file in filenames:
    ds = gdal.Open(file, 1)                                     # open files for modification
    band = ds.GetRasterBand(1)                                  # DEM files only have one band
    array = band.ReadAsArray()                                  # pass array to numpy
    array = np.where(array == nodata_val(), new_ndval, array)   # update NoData value
    band.WriteArray(array)                                      # write to file
    band.SetNoDataValue(new_ndval)                              # assign NoData value
    band.FlushCache()                                           # save changes
del ds                                                          # close file