set terminal postscript eps enhanced color lw 1. 18
set output "memDissipation_av.eps"

LW=1.
PS=1.
set style line 1 lw LW ps PS lt 1 pt 5 lc rgb "red" 
set style line 2 lw LW ps PS lt 1 pt 7 lc rgb "blue" 
set style line 3 lw LW ps PS lt 1 pt 9 lc rgb "brown" 
set style line 4 lw LW ps PS lt 1 pt 11 lc rgb "grey" 
set style line 5 lw LW ps PS lt 1 pt 13 lc rgb "grey" 

set bmargin 3.
set tmargin 0.
set lmargin 8

unset key

set size 1.,1.1
set origin 0.,0.
set multiplot

set title "Average memory dissipation (MPCS nodes only)"
set size 1.0,0.5
set origin 0.,0.5
set yr [0:20]
set timefmt "20%y%m%d%H"
set xdata time
set ylabel "{/Times-Italic M_a}-{/Times-Italic M_u} (in G)"
unset xlabel
p '../data_august/MPCS_memDissipation_average.dat' u 1:3:4 w yerrorlines ls 1\
, './MPCS_memDissipation_average.dat' u 1:3:4 w yerrorlines ls 2
unset title

set size 1.0,0.5
set origin 0.,0.
set yr [0:3.5]
set timefmt "20%y%m%d%H"
set xdata time
set xlabel "date"
set ylabel "{/Times-Italic m_a}-{/Times-Italic m_u} (in G)"
set ytics 0,1,4
p '../data_august/MPCS_memDissipation_average.dat' u 1:5:6 w yerrorlines ls 1 \
, './MPCS_memDissipation_average.dat' u 1:5:6 w yerrorlines ls 2


unset multiplot
