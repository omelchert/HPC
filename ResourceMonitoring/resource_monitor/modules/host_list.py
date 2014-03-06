"""host_list.py 

BRIEF  implements data structures that hold information on
       host resources and queue-instance resources extracted
       by parsing xml-output, previously obtained from qstat

DATE   2013-05-08
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-08
        1.00.01 -- 2013-05-10
                + added attribute hostState and method _fetchHostState() to Host class 
"""
from xml.dom.minidom import parse, parseString

class QueueInstance(object):
        """QueueInstance data structure

	(internal) class that holds all relevant resource information associated
        to a particular queue instances on a particular host

        """
        def __init__(self,myQInst):
		"""default constructor
		
		Upon initialization, an instance of the class requires
		a xml element:

		myQInst	- xml element that encodes all information related
                          to a particular queue instance

                NOTE: the default constructor also invokes several (private)
                methods that set the name and resources attributes of the 
                class instance thus constructed

		"""
                # Q name
                self.fullName=''
                self.qType=''
                self.nameHost=''
                # slot info
                self.slots_total=None
                self.slots_used=None
                self.slots_free=None
                # get properties of Q Instance 
                self._fetchName(myQInst)
                self._fetchQueueState(myQInst)
                self._fetchSlotInfo(myQInst)
                # misc
                self.state=None

        def _fetchName(self,el):
                """(private fcn) filter xml element to set Q name attributes"""
                self.fullName   = el.getElementsByTagName('name')[0].childNodes[0].data
                self.qType      = self.fullName.split('.')[0]
                self.nameHost   = self.fullName.split('.')[1].split('@')[-1]

        def _fetchQueueState(self,el):
                """(private fcn) filter xml element to set Q state attribute"""
                if el.getElementsByTagName('state'):
                       self.state      = el.getElementsByTagName('state')[0].childNodes[0].data

        def _fetchSlotInfo(self,el):
                """(private fcn) filter xml element to set slot resource attributes"""
                self.slots_total = int(el.getElementsByTagName('slots_total')[0].childNodes[0].data)
                self.slots_used  = int(el.getElementsByTagName('slots_used')[0].childNodes[0].data)
                self.slots_free  = self.slots_total-self.slots_used

        def __repr__(self):
                """represent queue instances as string"""
                myStr ='qName    = %s\n'%(self.fullName)
                myStr+='qType    = %s\n'%(self.qType)
                myStr+='\t slots  (total,used,free) = %d %d %d\n'%(self.slots_total,self.slots_used,self.slots_free)
                return myStr 

        def queueInstanceType(self):
                """return attribute: queue-type"""
                return self.qType

        def hostName(self):
                """return attribute: host name"""
                return self.nameHost 

        def numberOfSlots(self):
                """return attribute: total number of slots"""
                return self.slots_total

        def usedSlots(self):
                """return attribute: number of slots used"""
                return self.slots_used

class Host(object):
        """Host data structure

	(internal) class that holds all relevant resource information associated
        to a particular host

        """
        def __init__(self,hostName,el):
		"""default constructor
		
		Upon initialization, an instance of the class requires
		an input string and a xml element:

		hostname - string that encodes hostname 
		el       - xml element that encodes all information related
                           to a particular host 

                NOTE: the default constructor also invokes several (private)
                methods that set various attributes of the class instance 
                thus constructed

		"""
                # Q name
                self.hostName=hostName
                self.QueueInstances=[]
                # slot info
                self.slots_total=0
                self.slots_used=0
                # memory info
                self.mem_total=None
                self.mem_free=None
                self.mem_used=None
                self.mem_notAlloc=None
		# load info
		self.load_short=None
		self.load_long=None
		self.load_av=None
                # mist
                self.hostState=None
                # retrieve memory info for host
                self._fetchHostState(el)
                self._fetchResourceInfo(el)

        def _fetchResourceInfo(self,el):
                """(private fcn) filter xml element to set memory resource attribute""" 
                for nd in el.getElementsByTagName('resource'):
                        ndName,ndType,ndValue = self._readNode(nd)
                        if ndName=='mem_total': self.mem_total = self._memValue(ndValue)
                        if ndName=='mem_free':  self.mem_free  = self._memValue(ndValue)
                        if ndName=='mem_used':  self.mem_used  = self._memValue(ndValue)
                        if ndName=='h_vmem':    self.mem_notAlloc = self._memValue(ndValue)
                        if ndName=='load_short': self.load_short = float(ndValue)
                        if ndName=='load_long': self.load_long = float(ndValue)
                        if ndName=='load_avg':   self.load_av = float(ndValue)

        def _checkResourceInfo(self):
                """(private fcn) check if memory resource attributes are set""" 
                if self.mem_total==None: return 0
                if self.mem_free==None: return 0
                if self.mem_used==None: return 0
                if self.mem_notAlloc==None: return 0
                else: return 1

        def _fetchHostState(self,el):
                """(private fcn) filter xml element to set Q state attribute"""
                if el.getElementsByTagName('state'):
                       self.hostState = el.getElementsByTagName('state')[0].childNodes[0].data

        def _readNode(self,nd):
                """(private fcn) helper to retrieve 'name' and 'type' attributes and return value of xml element"""
                return nd.getAttribute('name'), nd.getAttribute('type'),nd.childNodes[0].data

        def _memValue(self,valueWithUnit):
                """(private fcn) helper to convert memory information (valueWithUnit) to unit G"""
                if valueWithUnit[-1]=="G":
                        return float(valueWithUnit.split("G")[0])
                if valueWithUnit[-1]=="M":
                        return float(valueWithUnit.split("M")[0])*0.001
                if float(valueWithUnit)==0.:
                        return 0. 

        def __repr__(self):
                """represent host instances as string"""
                myStr='%s\t'%(self.hostName)
                myStr+=' %3d  %3d \t'%(self.slots_total,self.freeSlots())
                myStr+=' %5.2lf  %5.2lf  %5.2lf \t'%(self.mem_total,self.mem_free,self.notAllocMemory())
                myStr+=' [%s]'%(', '.join([Q.queueInstanceType() for Q in self.QueueInstances]))
		myStr+=' %s'%(self.state())
                return myStr 

        def name(self):
                """return attribute: host name"""
                return self.hostName

        def QueueInstanceList(self):
                """return attribute: list of queue instances on host"""
                return self.QueueInstances

        def usedSlots(self):
                """return number of used slots on host"""
                return self.slots_used

        def freeSlots(self):
                """return number of free slots on host"""
                return self.slots_total-self.slots_used

        def usedMemory(self):
                """return attribute: used memory in G"""
                return self.mem_used

        def freeMemory(self):
                """return attribute: free memory in G"""
                return self.mem_free

        def allocMemory(self):
                """return allocated memory in G"""
                return self.mem_total-self.mem_notAlloc

        def notAllocMemory(self):
                """return attribute: memory that is not allocated in G"""
                return self.mem_notAlloc

	def loadShort(self):
                """return attribute: short time average of load per used slot"""
                return self.load_short 

	def loadLong(self):
                """return attribute: long time average of load per used slot"""
                return self.load_long 

	def loadAv(self):
                """return attribute: average of load per used slot"""
                return self.load_av 

        def state(self):
                """return attribute: state of host"""
                return self.hostState

        def fullInfoAvailable(self):
                """return 1 if all memory resource attributes are set, else return 0"""
                return self._checkResourceInfo()

        def addQueueInstanceToHost(self,myQInst):
                """(function) add queue instances and related resource info to host"""
                self.QueueInstances.append(myQInst)
                self.slots_total = max(self.slots_total,myQInst.numberOfSlots())
                self.slots_used += myQInst.usedSlots()

class HostList(object):
        """HostList data structure

	class that holds all relevant resource information associated
        to the list of hosts in an xml file.

        """
        def __init__(self,domObj):
		"""default constructor
		
		Upon initialization, an instance of the class requires
		a document object that represents a xml file:

		domObj  - document object parsed via xml.dom.minidom 

                NOTE: the default constructor also invokes a (private)
                method that parses the full document object 

		"""
                self.hosts=dict()       
                self._parseQueueInstances(domObj)

        def _parseQueueInstances(self,domObj):
                """(private fcn) parse document object (domObj) to obtain host details"""
                # queue instances are specified by the <Queue-List> elements
                for myQInst in domObj.getElementsByTagName('Queue-List'):
                        # create new queue instance that holds all relevant resource info
                        q = QueueInstance(myQInst)
                        # add the queue instance to its respective host
                        if q.hostName() not in self.hosts.keys():
                                self.hosts[q.hostName()] = Host(q.hostName(),myQInst)
                        self.hosts[q.hostName()].addQueueInstanceToHost(q)

        def __repr__(self):
                """represent host list as string"""
                return '\n'.join(['%s'%(host) for host in sorted(self.hosts.values()) if host.fullInfoAvailable()])

        def hostList(self):
                """return sorted list of hosts for which full resource info is available"""
                return sorted([host for host in self.hosts.values() if host.fullInfoAvailable()])

        def xhostList(self):
                """return sorted list of host-names for which full resource info is NOT available"""
                return sorted([host.name() for host in self.hosts.values() if not host.fullInfoAvailable()])
