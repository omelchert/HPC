"""hist_ascii.py 

BRIEF  implements simple ascii histogram 

DATE   2013-05-08
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-08
        1.00.01 -- 2013-05-10
                + restricted histogram to also not take into account hosts in state E
"""
from math import ceil

def histAscii_memUsage(hostList,myFcn,dx=1,flag_listHosts=False):
        """histogram using linear binning of supplied data

        NOTE: histogram is used to illustrate memory usage on the
              HERO/FLOW HPC Clusters. 


        EXEMPLARY USAGE:

        histAscii_memUsage(hDict.hostList(),
                           lambda h: h.notAllocMemory(),
                           dx=1,
                           flag_listHosts=1
                           )
        
	Input:
	hostList - list containing host data structures for which full
                   resource information is available
        myFcn    - custom function that provides access to the host
                   attribute for which the histogram will be computed.
                   So far only tested for: h.notAllocMemory(), h.freeMemory()
        dx       - bin width (default=1G) 
        flag_listHosts - 0/1 flag that indicates if all hosts for the
                         binned memory range should be listed (default=0)

	Returns: (nothing)

	"""
	# get bin id that corresponds to supplied numerical value
	def binId(val):   return int((val-xMin)/dx)
        # get lower and upper boundary for supplied bin id
        def bdry(myBin):  return xMin+myBin*dx, xMin+(myBin+1)*dx

        # get binning information
        xMin  = 0
        xMax  = max([myFcn(host) for host in hostList])
        nBins = binId(xMax)+1

        # set empty bins; bin is represented by list of hosts
        # that fall in respective memory range
	h = [[] for myBins in range(nBins)]	

	# data binning procedure
	for host in hostList:
            # consider only hosts with at least one free slot
            if host.freeSlots() and host.state()!='E': 
		h[binId(myFcn(host))].append(host)
        
	# dump histogram
	N=sum([len(hi) for hi in h]) 
        # set number of symbols for full histogram bar
	widthHistoBar = 70
        print "# number of hosts (free slots + not in state E) =",N
	print "# (memRange in G): ***histogram-bar*** | (# hosts) (% hosts)"
	for myBin in range(nBins):
		hRel   = float(len(h[myBin]))/N ## normalized freq.
		low,up = bdry(myBin)
		sCount = int(ceil(widthHistoBar*hRel))
		print "%2d-%2d: %s |%3d %2d%% "%(low, up, '*'*sCount+' '*(widthHistoBar-sCount),len(h[myBin]),int(round(100*hRel)))
        print

        # if requested, list all hosts that offer memory in binned range
        if flag_listHosts:
                print "# hosts in memory range:"
                for myBin in range(nBins):
                   if h[myBin]:
                     print "%2d - %2d G:\n\t(nr) (hostName) (total/free slots) (total/free/notAlloc memory) [queue instances]"%bdry(myBin)
                     for idx,host in enumerate(h[myBin]):
                             print "\t %3d  %s"%(idx+1,host)
                     print
                print

def histAscii_loadPerUsedSlot(hostList,myFcn,dx=1,flag_listHosts=False):
        """histogram using linear binning of supplied data

        NOTE: histogram is used to illustrate cpu load on the
              HERO/FLOW HPC Clusters. 


        EXEMPLARY USAGE:

        histAscii_memUsage(hDict.hostList(),
                           lambda h: h.loadShort()/h.usedSlots(),
                           dx=1,
                           flag_listHosts=1
                           )
        
	Input:
	hostList - list containing host data structures for which full
                   resource information is available
        myFcn    - custom function that provides access to the host
                   attribute for which the histogram will be computed.
        dx       - bin width (default=1G) 
        flag_listHosts - 0/1 flag that indicates if all hosts for the
                         binned memory range should be listed (default=0)

	Returns: (nothing)

	"""
	# get bin id that corresponds to supplied numerical value
	def binId(val):   return int((val-xMin)/dx)
        # get lower and upper boundary for supplied bin id
        def bdry(myBin):  return xMin+myBin*dx, xMin+(myBin+1)*dx

        # get binning information
        xMin  = 0
        xMax  = max([myFcn(host) for host in hostList])
        nBins = binId(xMax)+1

        # set empty bins; bin is represented by list of hosts
        # that fall in respective memory range
	h = [[] for myBins in range(nBins)]	

	# data binning procedure
	for host in hostList:
            # consider only hosts for which load info is available and are not in error state
            if host.loadShort() and host.state()!='E': 
		h[binId(myFcn(host))].append(host)
        
	# dump histogram
	N=sum([len(hi) for hi in h]) 
        # set number of symbols for full histogram bar
	widthHistoBar = 70
        print "# number of hosts (with available load info + not in state E) =",N
	print "# (load range in load/usedSlot): ***histogram-bar*** | (# hosts) (% hosts)"
	for myBin in range(nBins):
		hRel   = float(len(h[myBin]))/N ## normalized freq.
		low,up = bdry(myBin)
		sCount = int(ceil(widthHistoBar*hRel))
		print "%3.2lf-%3.2lf: %s |%3d %2d%% "%(low, up, '*'*sCount+' '*(widthHistoBar-sCount),len(h[myBin]),int(round(100*hRel)))
        print

        # if requested, list all hosts that have load in binned range
        if flag_listHosts:
                print "# hosts in load/usedSlot range:"
                for myBin in range(nBins):
                   if h[myBin]:
                     print "%3.2lf - %3.2lf:\n\t(nr) (hostName) (load/usedSlots) "%bdry(myBin)
                     for idx,host in enumerate(h[myBin]):
                             print "\t %3d %s %lf"%(idx+1, host.name(),myFcn(host))
                     print
                print
