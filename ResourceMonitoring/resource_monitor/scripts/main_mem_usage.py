"""main_mem_usage.py 

BRIEF  implements function that parses xml output of qstat 
       and filters for resource information related to the hosts.
       Here, the pivotal resource processed further is the 
       memory consumption on the hosts. A simple ascii histogram
       that illustrates the memory consumption is sent to stdout.

DATE   2013-05-08
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-08
        1.00.01 -- 2013-05-08
                + added output of hosts in state E and hosts with no free slots
"""
import sys
import commands
import datetime
from xml.dom.minidom import parseString
from resource_monitor.modules.host_list import HostList
from resource_monitor.modules.hist_ascii import histAscii_memUsage
from resource_monitor.modules.opt_parse import myOptionParser_memUsage
from resource_monitor.modules.utils import myGenerator


def mainMemUsage(argList=sys.argv[1:]):

        # print auxiliary information
        print "# arguments: %s"%(' '.join(argList))
        print "# timestamp: %s"%(datetime.datetime.now())

        # parse command line arguments
        (myOpts,myArgs) = myOptionParser_memUsage(argList)

	# construct proper call to qstat from cmdline args
        #myWrappedCmd = "qstat -F -l %s -xml"%(myOpts.myCmd)
        myWrappedCmd = "%s"%(myOpts.myCmd)
	print "# wrapped command: %s \n"%(myWrappedCmd)
        # fetch xml output from qstat as string
        myXmlOutput = commands.getoutput(myWrappedCmd)
        
        try:
                # parse string via xml.dom.minidom
                domObj = parseString(myXmlOutput)
        except:
                print "could not parse xml-output obtained from: ",myWrappedCmd
                print "exit now!"
                sys.exit(1)
                    
        # filter document object for host details
        hDict = HostList(domObj)

        # list ascii histogram for MEMORY that is NOT ALLOCATED 
        print "# histogram: not allocated memory"
        histAscii_memUsage(hDict.hostList(),lambda h: h.notAllocMemory(),myOpts.binWidth,myOpts.flag_listHosts)

        # list ascii histogram for MEMORY that is actually FREE 
        # NOTE: this is a HIDDEN OPTION, only accessible via the commandline option --all 
        if myOpts.flag_fullMemInfo:
                print "# histogram: free memory"
                histAscii_memUsage(hDict.hostList(),lambda h: h.freeMemory(),myOpts.binWidth,myOpts.flag_listHosts)


        hostList = [host.name() for host in hDict.hosts.values() if host.state()=='E']
        print "# %d hosts in state E:"%(len(hostList))
        for subList in myGenerator(hostList):
                print '\t', ' '.join(subList)

        hostList = [host.name() for host in hDict.hosts.values() if host.freeSlots()==0]
        print "# %d hosts with no free slots:"%(len(hostList))
        for subList in myGenerator(hostList):
                print '\t', ' '.join(subList)
