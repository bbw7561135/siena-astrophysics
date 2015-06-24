#!/usr/bin/env python

"""Label the coadds.
"""

from __future__ import division, print_function

import os
import sys
import logging
import argparse
import numpy as np
import seaborn as sns

import Image, ImageDraw
import pyregion
import matplotlib.pyplot as plt

from decals_simulations import get_brickinfo

from astropy.io import fits
from astrometry.libkd.spherematch import match_radec

# Global variables.
scratch_dir = '/global/work/decam/scratch/'
fake_decals_dir = os.getenv('FAKE_DECALS_DIR')

logging.basicConfig(format='%(message)s',level=logging.INFO,stream=sys.stdout)
log = logging.getLogger('decals_simulations')

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='DECaLS simulations.')
    parser.add_argument('-b', '--brick', type=str, default='2428p117', metavar='', 
                        help='process this brick (required input)')
    parser.add_argument('--no-qaplots', action='store_true',
                        help='do not generate QAplots')

    args = parser.parse_args()
    if args.brick is None:
        parser.print_help()
        sys.exit(1)

    brickname = args.brick
    log.info('Analyzing brick {}'.format(brickname))

    brickinfo, brickwcs = get_brickinfo(brickname)
    
    # Read the prior parameters
    priorsfile = os.path.join(fake_decals_dir,'priors_'+brickname+'.fits')
    log.info('Reading {}'.format(priorsfile))
    cat = fits.getdata(priorsfile,1)
    nobj = len(cat)

    xy = brickwcs.radec2pixelxy(cat['ra'],cat['dec'])
    rad = cat['disk_r50']/0.262 # half-light radius [pixels]

    imfile = os.path.join(scratch_dir,'coadd',brickname[:3],brickname,'decals-'+brickname+'-image.jpg')
    im = Image.open(imfile)
    draw = ImageDraw.Draw(im)
    for ii in range(nobj):
        draw.ellipse(((3600-xy[1][ii])-rad[ii], xy[2][ii]-rad[ii],
                      (3600-xy[1][ii])+rad[ii], xy[2][ii]+rad[ii]))
    im.save('junk.png')

if __name__ == "__main__":
    main()
