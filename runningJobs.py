import sys
import commands
import datetime

def getSlotFreqs(qstatOutput):
	"""construct frequency histogram for used slots

	given the accumulated output from qstat, the info
	for the number of used slots is located in column
	with integer ID 8
	"""
	myFreq=dict()
	myUserDict=dict()
	for line in qstatOutput.split("\n"):
		userName=line.split()[3]
		nSlots=int(line.split()[8])
		# update slot freq hist
		if nSlots not in myFreq.keys(): myFreq[nSlots]=0
		myFreq[nSlots]+=1
		# update user list
		if userName not in myUserDict.keys(): myUserDict[userName]=0
		myUserDict[userName]+=1
	return myFreq, sum(myFreq.values()),myUserDict

def getRealName(userName):
	"""obtain real name and unix-group name associated to user account
	use administrative database to obtain further user information
	"""
	myOutput = commands.getoutput("getent passwd %s" % (userName))
	if myOutput:
		return myOutput.split(":")[5].split("/")[-2], myOutput.split(":")[4]
	else:
		return "none", "none"

def dumpInfo(slotFreqs,N,userDict):
	"""list number of jobs, occupied slots and running jobs by users
	"""
	print "# found %d jobs"%(N)
	print "# found %d occupied slots"%(sum(map(lambda (x,y): x*y, slotFreqs.items())))
	print "# nSlots cts"
	for nSlots,ctr in sorted(slotFreqs.items()):
		print "%4d %4d"%(nSlots, ctr)

	print "# no. userName nJobs // agName realName"
	for no,(userName,nJobs) in enumerate(sorted(userDict.items(),key=lambda (k,v):(v,k),reverse=True)):
		agName,realName=getRealName(userName)
		print "%3d %s %3d // %-16s %s"%(no+1,userName,nJobs,agName,realName) 
	print

def main():
        print "# timestamp: %s"%(datetime.datetime.now())
	for ndType in ["mpcs","mpcb","uv100"]:
		# construct proper call to qstat 
		myWrappedCmd = "qstat -u \"*\" | grep \"%s\" | grep \" r \" "%(ndType)
		# fetch output from qstat as string
		myOutput = commands.getoutput(myWrappedCmd)
		# construct frequency histogram for used slots
		slotFreqs,N,userDict=getSlotFreqs(myOutput)
		# list details to stdout
		print "%s\n%s ndType %5s %s\n%s"%("#"*34,"#"*10,ndType,"#"*10,"#"*34)
		dumpInfo(slotFreqs,N,userDict)

main()
