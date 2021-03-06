from pylab import *
import atpy

class trial:
    def __init__(self):
        infile='/home/share/research/luminosityfunction/testLF.fits'
        self.ldat=atpy.Table(infile)

    def plotlum(self):
        figure()
        t=hist(self.ldat.logL,bins=100)
        clf()
        bins=t[1]
        yvalue=t[0]
        yerror=sqrt(t[0])
        bincenter=[]
        for x in range(len(yvalue)):
            bincenter.append((bins[x]+(bins[x+1]))/2)
            print bincenter
        yplot=log10(yvalue)    
        plot(bincenter,yplot,'ko')
        yerrup=log10(yvalue+yerror)-log10(yvalue)
        yerrdown=log10(yvalue)-log10(yvalue-yerror)
        yerrboth=zip(yerrdown,yerrup)
        yerrboth=transpose(yerrboth)
         errorbar(bincenter,yplot,yerrboth)
        #lummy=arange(-.01,5.,.1)
        Lvalues=linspace(-2.,1.,100)
        Llin=10**(Lvalues)
        schfun=(Llin**(-.25))*exp(-Llin)*55
        plot(Lvalues,log10(schfun))

        chisqu = 1*10**7
        steps=100
        amin=-1.5
        amax=-1
        bmin=3.7*10**26
        bmax=3.9*10**26
        for alpha in range(steps):
            for lsun in range(steps):
                a=amin+(amax-amin)*float(alpha)/(steps-1)
                b=bmin+(bmax-bmin)*float(lsun)/(steps-1)
                for n in range(chisqu):
                    schfun=(b**(a+1))*exp(-b)*55
                    chisqu=chisqu+schfun*schfun
                #chisqumin = ((lsunmin-lsundata)**2)/some error**2
                #if chisqu<chisqumin
                   #print alpha
                   #print phi
                   #print lsun

#def lumfun():
trial=trial()
    
