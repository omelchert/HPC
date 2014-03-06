set terminal postscript eps enhanced lw 1. 18
set output "memDissipation_raw_mem.eps"

set title "Memory dissipation (MPCS nodes only)" 

set multiplot
set size 1.
set origin 0.,0.

unset key

set xr [0:24]
set yr [0:24]

set xlabel "{/Times-Italic M_a}"
set ylabel "{/Times-Italic M_u}"

p "<grep 'mpcs' ../memDissipation_raw.dat" u 3:4 w p pt 7 ps 0.75, x w l lt 1, 0.8*x w l lt 2


unset title

set size 0.45,0.4
set origin 0.1,0.5

set key left
set key samplen 1.

unset xlabel
unset ylabel
set yr [:0.4]
set xr [0:16]

set ytics (0.,0.1,0.2,0.3, "{/Times-Italic P(M_u)}" 0.4)
set xtics (0,4,8,12, "{/Times-Italic M_u}" 16)

p '<python ../../filterRawData.py ../memDissipation_raw.dat 22 24 25' u 1:3 w lp lt 1 pt 4 t "{/Times-Italic M}_a=22-24G"\
, '<python ../../filterRawData.py ../memDissipation_raw.dat 20 22 25' u 1:3 w lp lt 1 pt 6 t "20-22G"\
, '<python ../../filterRawData.py ../memDissipation_raw.dat 18 20 25' u 1:3 w lp lt 1 pt 8 t "18-20G"\

unset multiplot
