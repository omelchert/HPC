"""opt_parse.py 

BRIEF  implements command line argument parser 

DATE   2013-05-08
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-08
"""
from optparse import OptionParser,SUPPRESS_HELP


def myCallback(opt,opt_str,value,parser,*args):
        """callback function that customizes command by means of
        which xml-output is obtained
        """
        if opt_str=='--fromFile':
                parser.values.myCmd = 'cat %s'%(parser.rargs[0])
        if opt_str=='-l':
                parser.values.myCmd = 'qstat -F -l %s -xml'%(parser.rargs[0])


def myOptionParser_memUsage(argList):
        """parser for commandline arguments

	Input:
        argList - list of input arguments (shoule be sys.argv[1:])

	Returns: (opts,args)
        opts    - object in which option arguments are stored 
        args    - positional arguments that remain after all options have been processed
	"""

        myParser = OptionParser()

        myParser.add_option("-l",
                        dest="myCmd",
                        metavar="resource=val",
                        action="callback",
                        callback=myCallback,
                        default="qstat -F -l hostname=* -xml",
                        help="resource for which to assemble a simple ascii histogram\
                              that illustrates the distribution of allocated memory on\
                              the respective hosts (default: hostname=*)",
                        )

        myParser.add_option("--fromFile",
                        dest="myCmd",
                        action="callback",
                        callback=myCallback,
                        help="alternative to -l option: if xml output of qstat was\
                              previously stored in a file, --fromFile <xmlFileName>\
                              will parse the contents of that xml file instead of\
                              wrapping a call to qstat",
                        )

        myParser.add_option("-b", 
                        dest="binWidth",
                        metavar="BIN_WIDTH",
                        type="int",
                        action="store",
                        help="set bin width (in G) for the simple ascii histogram (must\
                                        be larger than 0, default: 1)",
                        default=1,
                        )

        myParser.add_option("-f",
                        dest="flag_listHosts",
                        action="store_true",
                        default=False,
                        help="in addition to the simple ascii histogram, all hosts that \
                              fall into the respective memory ranges are listed toghether\
                              with more information on the host resources",
                        )


        myParser.add_option("-o",
                        dest="flag_memOverestim",
                        action="store_true",
                        default=False,
                        help="in addition to the simple ascii histogram, list the memory \
                              overestimation factor 1-freeMem/notAllocMem for each host",
                        )

        myParser.add_option("--all", 
                        dest="flag_fullMemInfo",
                        action="store_true",
                        default=False,
                        help=SUPPRESS_HELP
                        )
        
        return myParser.parse_args(argList)


if __name__=='__main__':
        import sys
        (opts,args) = myOptionParser_memUsage(sys.argv[1:])
        print opts
