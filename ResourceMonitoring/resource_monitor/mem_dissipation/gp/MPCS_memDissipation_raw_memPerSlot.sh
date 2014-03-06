
FNAME=$1

gnuplot << EOF
set terminal postscript eps enhanced lw 1. 18
set output "${FNAME}_memPerSlot.eps"


unset key

set xlabel "{/Times-Italic m_a}"
set ylabel "{/Times-Italic m_u}"

set multiplot
set origin 0.,0.
set size 1.
set xr [:5]
p "<grep 'mpcs' ${FNAME}" u (\$3/\$2):(\$4/\$2) w p pt 7 ps 0.75, x w l lt 1, 0.8*x w l lt 2,0.35*x w l lt 2, 0.5*x w l lt 4


set origin 0.1,0.54
set size 0.41
unset xlabel
unset ylabel
set xr [:12]
p "<grep 'mpcs' ${FNAME}" u (\$3/\$2):(\$4/\$2) w p pt 7 ps 0.75, x w l lt 1


unset multiplot
EOF

#mv ../data/*.eps ../eps/
