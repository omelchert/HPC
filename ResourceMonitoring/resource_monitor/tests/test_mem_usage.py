"""test_mem_usage.py 

BRIEF  imports function that parses xml output of qstat 
       and filters for resource information related to the hosts.
       Here, the pivotal resource processed further is the 
       memory consumption on the hosts. A simple ascii histogram
       that illustrates the memory consumption is sent to stdout.

       NOTE: this file is a test file that illustrates the
       mainMemUsage() funtion

DATE   2013-05-08
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-08
"""
import sys
sys.path.append('../../')
from resource_monitor.scripts.main_mem_usage import mainMemUsage

mainMemUsage(['--fromFile',' sample_mpcs.xml', '-f'])
