#! /usr/bin/env python

import sextutils as sex
import numpy as np
import pyfits
from astLib import astWCS
from astLib import astImages
import argparse
# import matplotlib.pyplot as plt

def get_cutout(clustername):

    outpath = '/home/obsastro1/clash/'
    datapath = '/home/obsastro1/siena-astrophysics/summer2013/clash/'
    rootpath = '/clash-archive/clash_archive/'+ clustername + '/HST/'
    fits_path = rootpath+'images/mosaicdrizzle_image_pipeline/scale_65mas/'
    color_path = rootpath+'color_images/mosaicdrizzle_image_pipeline/'

    fits_file = fits_path + clustername + '_mosaic_065mas_wfc3ir_f160w_drz_20110815.fits.gz'
    color_file = color_path + clustername + '_ir.png'

#   im = imread('macs1206_ir.png').astype(np.float32)
    im = pyfits.getdata(fits_file)
    hdr = pyfits.getheader(fits_file)
    wcs = astWCS.WCS(hdr,mode='pyfits')

    arcfile = datapath+clustername+'-arcs.txt'
    arcs = sex.se_catalog(arcfile)
# get the celestial coordinates at the center
#   for i in range(10):
    for i in range(len(arcs.ra)):
#       ww = float(width[i])
        #width = arcs.width[i]/3600.0
        cutim = astImages.clipImageSectionWCS(im,wcs,arcs.ra[i],arcs.dec[i],float(arcs.width[i]/3600.0),returnWCS=True)

        gal = str(arcs.id[i]).split('.')
        outfile = outpath+clustername+'-arc'+gal[0]+'-im'+gal[1]+'.png'
        print i, outfile
        astImages.saveBitmap(outfile,cutim['data'],[0.0,0.5],300,'gray')
           
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Retrieve cluster cutouts.')
    parser.add_argument('cluster', type=str, default=None, help='Cluster name')

    args = parser.parse_args()

    if args.cluster is None:
        print "Need a cluster name!"
        parser.print_help()

    clustername = args.cluster
    get_cutout(clustername)

   
