#! /usr/bin/env python
from pylab import *
import atpy
import pylab

class cluster:
    def __init__(self,clustername):
        infile='/home/rfinn/research/LocalClusters/NSAmastertables/'+clustername+'_NSAmastertable.fits'
        self.mdat=atpy.Table(infile)
        
    def plotradec(self):
        figure()
        plot(self.mdat.RA,self.mdat.DEC,'b.')

    def plotRedshift(self):
        figure()
        hist(self.mdat.ZDIST)
        title (' ')

class ediscs:
    def __init__(self):
        infile='/home/share/research/ediscs/ediscs_kcorrect_v4.0.topcat.fits'
        self.kdat=atpy.Table(infile)

    def kcorrect(self):
        figure()
        hist(self.kdat.UGRIZ_ABSMAG_00[:,1],bins=5)
        title ('UGRIZ ABSMAG IVAR 00')

    def abs_gband_mag(self):
        figure()
        hist(self.kdat.UGRIZ_ABSMAG_00[:,1],bins=5)
        title ('UGRIZ ABSMAG IVAR ')
        
        ax=gca()
        ax.set_yscale('log')
        ylabel('Number of Galaxies')
        xlabel('Absolute G-Band Magnitude')

    def gbandlum(self):
        figure()
        absmag=self.kdat.UGRIZ_ABSMAG_00[:,1]
        luminosity = ((absmag-4.83)/-2.5)
        print luminosity
        hist(luminosity,bins=600, range=[7,15])
        #ax=gca()
        #ax.set_yscale('log')
        xlim(7,15)
        ylabel('N')
        xlabel('log(g-band L/L$_\odot$)')
        title ('EDisCS')
    
edi=ediscs()
