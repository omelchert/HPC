set terminal postscript eps enhanced lw 1. 18
set output "memDissipation_raw_memPerSlot.eps"

set style fill   solid 0.25 noborder

set title "Memory dissipation per slot (MPCS nodes only)"

unset key

set xlabel "{/Times-Italic m_a}"
set ylabel "{/Times-Italic m_u}"

set multiplot
set origin 0.,0.
set size 1.
set xr [:5]
set yr [0:]

set label 1 "{/Times-Italic m_u}={/Times-Italic m_a}" at graph 0.87,0.905 rotate by 35 left front
set label 2 "{/Times-Italic m_u}={/Times-Italic m_a}-0.7" at graph 0.87,0.77 rotate by 35 left front 
set label 3 "{/Times-Italic m_u}={/Times-Italic m_a}-2.1" at graph 0.87,0.49 rotate by 35 left front


#p "<grep 'mpcs' ../memDissipation_raw.dat" u ($3/$2):($4/$2) w p pt 7 ps 0.75, x w l lt 1, 0.8*x w l lt 2,0.35*x w l lt 2, 0.5*x w l lt 4, (x-1.)
p "<python fillArea.py 0.7 2.1" u 1:2:3 w filledcu, (x-0.7) w l lt 2, (x-2.1) w l lt 2\
, "<grep 'mpcs' ../memDissipation_raw.dat" u ($3/$2):($4/$2) w p pt 7 ps 0.75, x w l lt 1\

unset label 1
unset label 2
unset label 3
unset title

set origin 0.1,0.5
set size 0.41
unset xlabel
unset ylabel
set xr [:12]
p "<python fillArea.py 0.7 2.1" u 1:2:3 w filledcu, (x-0.7) w l lt 2\
, "<grep 'mpcs' ../memDissipation_raw.dat" u ($3/$2):($4/$2) w p pt 7 ps 0.75, x w l lt 1, (x-0.7)


unset multiplot
