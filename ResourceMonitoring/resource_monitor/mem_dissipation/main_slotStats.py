"""main_dissipation.py 

BRIEF  implements function that parses xml output of qstat 
       and filters for resource information related to the hosts.
       Here, the pivotal resource processed further is the 
       memory consumption on the hosts. 

DATE   2013-07-30
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-07-30
"""
import sys
sys.path.append('../../')
import commands
import datetime
from xml.dom.minidom import parseString
from resource_monitor.modules.host_list import HostList
from resource_monitor.modules.hist_ascii import histAscii_memUsage
from resource_monitor.modules.opt_parse import myOptionParser_memUsage
from resource_monitor.modules.utils import myGenerator
from resource_monitor.modules.simpleStatistics import basicStatistics


def mainMemDissipation(argList=sys.argv[1:]):

        # parse command line arguments
        (myOpts,myArgs) = myOptionParser_memUsage(argList)

	# construct proper call to qstat from cmdline args
        myWrappedCmd = "%s"%(myOpts.myCmd)
        myDate = int( myWrappedCmd.split('_')[-2])
        myHour = myWrappedCmd.split('_')[-1][1:3]
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

	hostDetails_list = [(host.name(), 
			host.usedSlots(), 
			host.mem_total-host.mem_notAlloc, 
			host.mem_used, 
			host.mem_total-host.mem_notAlloc-host.mem_used, 
			(host.mem_total-host.mem_notAlloc-host.mem_used)/host.usedSlots(),
                        host.loadLong()/host.usedSlots())
			for host in hDict.hosts.values() if host.fullInfoAvailable() and host.usedSlots()>0 and host.state()!='E' ]
			#for host in hDict.hosts.values() if host.fullInfoAvailable() and host.usedSlots()>0 and host.usedSlots()<12 and host.state()!='E' ]

	print "# (timestamp of snapshot) (slots from fully occ hosts) (overall number of occ slots)"
	nSlotList = sorted([ x[1] for x in hostDetails_list if "mpcs" in x[0] ])
	slotList_filtered = filter(lambda x: x==12, nSlotList)
	print str(myDate)+myHour, sum(slotList_filtered), sum(nSlotList)

	
mainMemDissipation()
