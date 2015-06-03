#!/usr/bin/env python

import galsim
import numpy as np
import os
import math
from astropy.io import fits

def decals_makefake():

    gsparams = galsim.GSParams(maximum_fft_size=2**16)

    #Set parameter ranges.
    nfake = 20
    nmin = 0.8
    nmax = 5.0
    r50min = 0.1
    r50max = 1.0
    phimin = 0.0
    phimax = 180.0
    axismin = 0.2
    axismax = 1.0
    rmagmin = 16.0
    rmagmax = 18.0
    grmin = -0.3
    grmax = 0.5
    rzmin = 0.0
    rzmax = 1.5
    
    # Set directories.
    decals_dir = os.getenv('DECALS_DIR')
    out_dir = os.getenv('HOME')+'/decals-fake/'
    root_dir = '/home/desi3/'
    brickinfo = fits.getdata(decals_dir+'/decals-bricks.fits',1)
    
    # Create an array for both the bricks and the bands.
    mybricks = ['2426p197']
    #mybricks = ['2426p197','2428p117']
    band = ['g','r','z']
    
    #  Loop randomly generating priors.
    for thisbrick in mybricks:
        print('Getting info on brick {}'.format(thisbrick))
        info = brickinfo[np.where((brickinfo['brickname']==thisbrick)*1==1)]
        
        # Randomly generate location and flux parameters.
        ra = np.random.uniform(info['ra1'],info['ra2'],nfake)
        dec = np.random.uniform(info['dec1'],info['dec2'],nfake)
        rmag = np.random.uniform(rmagmin,rmagmax,nfake)
        grmag = np.random.uniform(grmin,grmax,nfake)
        rzmag = np.random.uniform(rzmin,rzmax,nfake)

        # Calculate the g, r, and z band fluxes and stack them in an array.
        gflux = 10**(-0.4*((rmag+grmag)-22.5))
        rflux = 10**(-0.4*(rmag-22.5))
        zflux = 10**(-0.4*((rmag-rzmag)-22.5))
        flux = np.vstack([gflux,rflux,zflux])
        
        # Randomly generate parameters.
        sersicn = np.random.uniform(nmin,nmax,nfake)
        r50 = np.random.uniform(r50min,r50max,nfake)
        phi = np.random.uniform(phimin,phimax,nfake)
        axisratio = np.random.uniform(axismin,axismax,nfake)

        # Create a fits table containing the arrays of the randomly generated parameters.
        tbhdu = fits.BinTableHDU.from_columns([
            fits.Column(name='ra',format='f4',array=ra),
            fits.Column(name='dec',format='f4',array=dec),
            fits.Column(name='rmag',format='f4',array=rmag),
            fits.Column(name='grmag',format='f4',array=grmag),
            fits.Column(name='rzmag',format='f4',array=rzmag),
            fits.Column(name='r50',format='f4',array=r50),
            fits.Column(name='phi',format='f4',array=phi),
            fits.Column(name='axisratio',format='f4',array=axisratio)])
        tbhdu.writeto(root_dir+'decals_fake_priors.fits',clobber=True)

        # Loop, which reads in an already existing fits image.
        for iband, thisband in enumerate(band):
            print('Working on band {}'.format(thisband))
            imfile = decals_dir+'/coadd/'+thisbrick[0:3]+'/'+thisbrick+'/decals-'+thisbrick+'-image-'+thisband+'.fits'

            # Read the pre-existing decals image.
            print('Reading {}'.format(imfile))
            im = galsim.fits.read(imfile)
            wcs = im.wcs
            
            # Loop, which assigns an index (soon to be home to a galaxy) to a randomly selected position.
            for iobj in range(nfake):
                print(iobj)
                pos = wcs.posToImage(galsim.CelestialCoord(
                    ra[iobj]*galsim.degrees,dec[iobj]*galsim.degrees))
            
                # Need to deal with PSF.
                #psf = galsim.Gaussian(flux=1.0, sigma=1.0)

                local = wcs.local(pos)

                # Creates the galaxies.
                stamp = galsim.Sersic(n=sersicn[iobj],half_light_radius=r50[iobj],gsparams=gsparams,flux=flux[iband,iobj])
                stamp = stamp.shear(q=axisratio[iobj],beta=phi[iobj]*galsim.degrees)
                #im = galsim.Convolve([stamp,psf])
                stamp = stamp.drawImage()
                stamp.setCenter(int(pos.x),int(pos.y))
    
    #stamp = im.drawImage(wcs=local, offset=offset)
    #stamp.setCenter(ixx,iyy)

                # Sets the bounds of the image.   
                bounds = stamp.bounds & im.bounds
                im[bounds] += stamp[bounds]
  
            # Writes the images to the output directory.
            outfile = out_dir+thisbrick+'_'+thisband+'.fits'
            print('Writing {}'.format(outfile))
            galsim.fits.write(image=im,file_name=outfile,clobber=True)

if __name__ == "__main__":
    decals_makefake()

