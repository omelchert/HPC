## \file   simpleStatistics.py
#  \brief  tiny libary that contains useful functions
# 	   for data postprocesssing
#	   
#  \date   04.03.2011
from math   import sqrt,floor,log,exp
from random import randint

def covariance(xList,yList):
        """compute covariance to see whether the values 
        the two lists vary together

        NOTE: both input lists need to have the same length

        Input:
        xList   -  list of x values
        yList   -  list of y values

        Returns: (cov)
        cov     - covariance of the data in the two input lists
        """
        xAv = mean(xList)
        yAv = mean(yList)
        return float(sum(map(lambda x,y: (x-xAv)*(y-yAv),xList,yList)))/len(xList)
                
def correlation(xList,yList):
        """compute Pearson correlation coefficient for the two 
        data sets

        NOTE: both input lists need to have the same length

        Input:
        xList   -  list of x values
        yList   -  list of y values

        Returns: (corr)
        corr    - corr of the data in the two input lists
        """
        xAv,xDev,xErr = basicStatistics(xList)
        yAv,yDev,yErr = basicStatistics(yList)
        return float(sum(map(lambda x,y: (x-xAv)*(y-yAv),xList,yList)))/(len(xList)*xDev*yDev)

def median(myList):
        """compute median for given sample

        Input:
        myList  - sample

        Returns: (med)
        med     - median value
        """
	myList.sort()
	N = len(myList)
	if N%2: # N odd
		return myList[N/2]
	else:   # N even
		return 0.5*(myList[N/2-1]+myList[N/2])

def medianAbsDev(myList):
        """compute median of absolut deviations from 
        the median 

        NOTE: robust measure for variability of the dataset

        Input:
        myList  - sample

        Returns: (mad)
        mad     - median absolute deviation
        """
        med = median(myList)
        return median(map(lambda x: abs(x-med),myList))

def pmfAv(myPmf):
        """compute average using probability mass function (PMF)

        Input:
        myPmf   - probability mass function

        Returns: (av)
        av      - average computed from PMF
        """
        return sum(map(lambda (xi,pi): xi*pi,myPmf.iteritems()))

def pmfUVar(myPmf):
        """compute uncorrected variance using PMF 

        Input:
        myPmf   - probability mass function

        Returns: (uVar)
        uVar    - uncorrected var computed from PMF
        """
        av = pmfAv(myPmf)
        return sum(map(lambda (xi,pi): pi*(xi-av)**2,myPmf.iteritems()))

def getPmf(myList):
	"""construct approximate pmf from values in 
	supplied list

	Input:
	myList	-- outcomes of random experiments for
		   which pmf shall be approximated

	Returns: (pMap)
	pMap	-- pmf of the values stored in myList
	"""
	pMap = {}  ## ini empty map
	nInv=1./len(myList) 
	for element in myList:
	   if element not in pMap:
	      pMap[element] = 0.
	   pMap[element] += nInv
	return pMap

def mean(myList):
        return float(sum(myList))/len(myList)

def basicStatistics(myList):
	"""compute mean value, standard deviation,
	and standard error of the mean for the 
	supplied list of numerical values

	NOTE: so as to reduce roundoff errors, 
	variance is computed via the corrected
	two-pass algorithm

	Input:
	myList	-- sequence of numerical values

	Returns: (av,sDev,sErr)
	av	-- mean value
	sDev	-- standard deviation
	sErr	-- standard error of the mean
	"""
	av=var=tiny=0.
	N  = len(myList) 
        av = mean(myList)
	for el in myList:
		dum   = el - av
		tiny += dum
		var  += dum*dum
	var = (var - tiny*tiny/N)/(N-1)
	sDev = sqrt(var)
	sErr = sDev/sqrt(N)
	return av, sDev, sErr

def bootstrap(array,estimFunc,nBootSamp=128):
	"""Empirical bootstrap resampling of data.
	
	estimates value of function 'estimFunc' from original data 
	stored in list 'array'. Calculates corresponding error as 
	standard deviation of the 'nBootSamp' resampled bootstrap 
	data sets

	Input:
	array     	-- list of values for resampling procedure
	estimFunc  	-- estimator function for resampling procedure
	nBootSamp  	-- number of bootstrap samples (default 128)

	Returns: (origEstim,resError)
	origEstim	-- value of estimFunc for original data
	resError	-- corresponding error estimated via resampling
	"""
	# estimate mean value from original array
	origEstim=estimFunc(array)
	## resample data from original array
	nMax=len(array)		
	h   = [0.0]*nBootSamp
	bootSamp = [0.0]*nMax 
	for sample in range(nBootSamp):
		for val in range(nMax):
			bootSamp[val]=array[randint(0,nMax-1)]
		h[sample]=estimFunc(bootSamp)
	## estimate error as std deviation of resampled values
	resError = basicStatistics(h)[1]
	return origEstim,resError



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

def hist(rawData,xRange,nBins=10,mode='lin'):
	"""histogram using linear binning of supplied data

	Input:
	rawData	-- list containing data to be binned 
	xRange  -- lower(incl)/upper(excl) boundary for numerical values
	nBin    -- desired number of bins (default =10)
	mode	-- binning type (possible choices: lin, log)

	Returns: (nothing)
	"""

	h = [0]*nBins
	xMin=float(xRange[0])
	xMax=float(xRange[1])

	if mode == 'lin':
		dx = (xMax-xMin)/nBins
		def binId(val):   return int(floor((val-xMin)/dx))
		def bdry(bin):	  return xMin+bin*dx, xMin+(bin+1)*dx
		def GErr(q,n,dx): return sqrt(q*(1-q)/(N-1))/dx 

	elif mode == 'log':
		dx = log(xMax/xMin)/nBins
		def binId(val):   return int(floor(log(val/xMin)/dx))
		def bdry(bin):	  return xMin*exp(bin*dx), xMin*exp((bin+1)*dx)
		def GErr(q,n,dx): return "##" 

	for value in rawData:
		if 0<=binId(value)<nBins:
		  h[binId(value)] += 1
	
	N=sum(h)
	for bin in range(nBins):
		hRel   = float(h[bin])/N
		low,up = bdry(bin)
		width  = up-low
		print low, up, hRel/width, GErr(hRel,N,width) 


def chiSquare(obsFreq,expFreq,nConstr):
	"""perform chi-square test for supplied
	list of data

	Input:
	obsFreq	-- observed frequencies
	expFreq -- expected frequencies

	Returns: (dof,chi2)
	dof	-- number of degrees of freedom
	chi2	-- numerical value of chi-square
	"""
	nBins=len(obsFreq)
	chi2=0.0
	for bin in range(nBins):
		dum   = obsFreq[bin]-expFreq[bin]
		chi2 += dum*dum/expFreq[bin]
	dof = nBins-nConstr
	return dof,chi2

def jacknife_binderRatio(x):
        """compute binder parameter via jacknife resampling

        NOTE: 
        - binder parameter g = 0.5*(3-<x4>/<x2>2)
        - error estimates can be computed via two sweeps over
          the data, only! More efficient than bootstrap 
          resampling
        
        Subfcts:
        binderRatio()   - no dependencies
        sDev()          - calls basicStatistics()

        Input:
        x       - data sample

        Returns: (g,gErr)
        g       - binder parameter
        gErr    - error for binder parameter
        """
        # abreviations for binder parameter and standard dev
        def binderRatio(x2,x4): return 0.5*(3.- x4/pow(x2,2))
        def sDev(x): return basicStatistics(x)[1]

        # get full sums involving N terms
        N = len(x)
        x2_sum = sum(map(lambda xi: pow(xi,2),x))
        x4_sum = sum(map(lambda xi: pow(xi,4),x))
        # substract one term to yield jacknifed data sets
        x2_jack = map(lambda xi: float(x2_sum-pow(xi,2) )/(N-1),x)
        x4_jack = map(lambda xi: float(x4_sum-pow(xi,4) )/(N-1),x)

        # compute binder parameter
        g = binderRatio(x2_sum/N ,x4_sum/N)
        # compute error to binder parameter from the 
        # standard deviation of the resampled data sets
        g_jack = map(lambda x4,x2: binderRatio(x2,x4),x4_jack,x2_jack)

        gErr = sqrt( N-1) * sDev(g_jack) 
        return g,gErr

def jacknife_variance(x):
        """compute variance error bars via jacknife resampling

        NOTE: 
        - variance = <x2> - <x>2 
        - error estimates can be computed via two sweeps over
          the data, only! More efficient than bootstrap 
          resampling
        
        Subfcts:
        sDev()          - calls basicStatistics()

        Input:
        x       - data sample

        Returns: (g,gErr)
        var       - variance 
        varErr    - error for variance 
        """
        def sDev(x): return basicStatistics(x)[1]

        # compute full sums
        N = len(x)
        x_sum = sum(x)
        x2_sum = sum(map(lambda xi: xi*xi, x))
        # substract one term to yield jacknifed data sets
        x_jack  = map(lambda xi: float(x_sum-xi)/(N-1), x)
        x2_jack = map(lambda xi: float(x2_sum-xi*xi)/(N-1), x)

        # compute variance 
        var = x2_sum/N - pow(x_sum/N,2)
        # compute error to variance from the 
        # standard deviation of the resampled data sets
        var_jack = map(lambda xi,x2i: x2i-pow(xi,2), x_jack,x2_jack )
        varErr = sqrt(N-1)*sDev(var_jack)
        return var, varErr


## EOF: simpleStatistics.py
