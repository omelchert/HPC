import sys

x=0
xMax=100
dx = 1

b1 = float(sys.argv[1])
b2 = float(sys.argv[2])

while x<xMax: 

  print x,x-b1, x-b2
  x+=dx
