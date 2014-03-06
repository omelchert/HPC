import sys
from math import floor,sqrt


def hist_linBinning(rawData,xMin,xMax,nBins=10):
	"""histogram using linear binning of supplied data

	Input:
	rawData	-- list containing data to be binned 
	xMin    -- lower boundary for numerical values (inclusive)
	xMax    -- upper boundary for numerical values (exclusive)
	nBin    -- desired number of bins (default =10)

	Returns: (nothing)
	"""
	h = [0]*nBins		## initial frequencies for each bin
	dx = (xMax-xMin)/nBins	## uniform bin width

	## get bin id that corresponds to supplied numerical value
	def binId(val):   return int(floor((val-xMin)/dx))
	## get lower and upper boundary for supplied bin id
	def bdry(bin):	  return xMin+bin*dx, xMin+(bin+1)*dx
	## compute gaussian error bar for particular bin
	def GErr(q,n,dx): return sqrt(q*(1-q)/(N-1))/dx 

	## data binning procedure: obtain frequencies
	for value in rawData:
		if 0<=binId(value)<nBins:
		  h[binId(value)] += 1
	
	## dump histogram
	N=sum(h) ## overall number of events
	for bin in range(nBins):
		hRel   = float(h[bin])/N ## normalized freq.
		low,up = bdry(bin)
		width  = up-low
		print low, up, hRel/width, GErr(hRel,N,width) 

def getData(fName,Mmin,Mmax):
        rawData = []

        for line in open(fName,'r'):
                sline = line.split()
                Ma = float(sline[2])
                Mu = float(sline[3])
                if Ma>Mmin and Ma<Mmax:
                        rawData.append(Mu)

        return rawData

def main():
        fName=sys.argv[1]
        Mmin = int(sys.argv[2])
        Mmax = int(sys.argv[3])
        nBins = int(sys.argv[4])
        rawData = getData(fName,Mmin,Mmax)

        hist_linBinning(rawData,min(rawData),max(rawData),nBins)


main()
