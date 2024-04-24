#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Merge multiple Geotiffs for further analysis - also included, NDWI calculation

import glob
from osgeo import gdal

ls = glob.glob('/Volumes/dmk/Pittsburgh_Sept2023_psscene_analytic_sr_udm2/Analytic/*.tif') # where [...] is the remainder of the path of all geotiff files
# Make sure all files are in the same projection

# pixel size:
# QGIS: check pixel size under properties -> information -> pixel size
# Note: keep any negative signs
dx = 3
dy = -3

vrt = gdal.BuildVRT("mergeTiffs.vrt, ls")
gdal.Translate("mergeTiffs.tif", vrt, xRes = dx, yRes = dy)
vrt = None
