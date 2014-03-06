"""utils.py 

BRIEF  implements auxiliary data structures and helper functions  

DATE   2013-05-10
AUTHOR Oliver Melchert

VERSION HISTORY:
	1.00.00 -- 2013-05-10
"""


def myGenerator(myList,dN=10):
        '''generator used for pretty-printing of long lists
        yields sub-lists of desired length

        Input:
        myList  - list of things to print
        dN      - desired number of elements in one line

        '''
        for i in range(len(myList)/dN+1):
                yield myList[i*dN:(i+1)*dN]

