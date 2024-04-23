#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# To prepare for MintPy and maintain compatability for the outputs with GIS.

# Clip a bunch of geotiffs to the same area
import os
import glob
from multiprocessing import Pool

# custom function to reproject and crop
# Note: reprojection is needed so that output is compatible with Google Earth (kmz) format
def crop_and_save(fn):
    split = fn.split(".")
    tout = split[0] + ".trns.tif"
    wout = split[0] + ".rprj.tif"
    gdal.Translate(destName = tout, srcDS = fn, projWin = [ulx, uly, lrx, lry])
    gdal.Warp(wout, tout, srcSRS = 'EPSG:32617', dstSRS = 'EPSG:4326', xRes = dx, yRes = dy, cutlineDSName = clip, cropToCutline=True)
    os.remove(tout)
    print(str(split[0]))

# list all image files
ls = glob.glob('/Volumes/[...]/hyp3/*/*.tif') # where [...] is the remainder of the path of all geotiff files
lt = [f for f in ls if '.rprj.' not in f] # this is to check and remove previously cropped and reprojected images from the list to be processed.
ls = lt
del(lt)

# determine the largest area covered by all input files
# This is sufficiently fast that it will be run single-thread
corners = [gdal.Info(f, format='json')['cornerCoordinates'] for f in ls]
ulx = max(corner['upperLeft'][0] for corner in corners)
uly = min(corner['upperLeft'][1] for corner in corners)
lrx = min(corner['lowerRight'][0] for corner in corners)
lry = max(corner['lowerRight'][1] for corner in corners)
del(corners)

# identify the area of interest to clip.  This was done in QGIS atop one of the unwrapped images.
# Note: aoi should have the latitude and longitude CRS (EPSG:4326)
clip = "/Volumes/[...]/aoi.shp"

# pixel size:
# QGIS: Warp, properties, information, resolution
# gdalinfo: take translated example (e.g., from below or QGIS) and look for pixel size.
# Note: keep any negative signs
dx = 0.000
dy = -0.000

# Body of code:
if __name__ == '__main__':
    p = Pool()
    result = p.map(crop_and_save, ls)

    p.close()
    p.join()

