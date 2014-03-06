set terminal postscript eps enhanced color lw 1. 18
set output "nSlots_2013.eps"

LW=1.
PS=1.
set style line 1 lw LW ps PS lt 1 pt 5 lc rgb "red" 
set style line 2 lw LW ps PS lt 1 pt 7 lc rgb "blue" 
set style line 3 lw LW ps PS lt 1 pt 9 lc rgb "brown" 
set style line 4 lw LW ps PS lt 1 pt 11 lc rgb "grey" 
set style line 5 lw LW ps PS lt 1 pt 13 lc rgb "grey" 
set style line 6 lw LW ps PS lt 2 lc rgb "black" 

set bmargin 3.
set tmargin 0.
set lmargin 8

unset key

set size 1.0,0.5
set origin 0.,0.
set yr [0:1600]
set ytics 0,400,1600
set timefmt "20%y%m%d%H"
set xdata time
set ylabel "# slots"
set xlabel "date"
set xrange ["2013080100":"2013111800"]
p '../MPCS_nOccSlots_2013.dat' u 1:3 w filledcurve x1 ls 2 t "# slots on fully occ. hosts"\
, '../MPCS_nOccSlots_2013.dat' u 1:2 w filledcurve x1 ls 1 t "total # slots"\
, 1548 w l ls 6 t "max. # slots"




