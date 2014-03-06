set terminal postscript eps enhanced lw 1. 18
set output "memDissipation_av.eps"


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
p './MPCS_memDissipation_average.dat' u 1:3:4 w yerrorlines pt 6
unset title

set size 1.0,0.5
set origin 0.,0.
set yr [0:3.5]
set timefmt "20%y%m%d%H"
set xdata time
set xlabel "date"
set ylabel "{/Times-Italic m_a}-{/Times-Italic m_u} (in G)"
set ytics 0,1,4
p './MPCS_memDissipation_average.dat' u 1:5:6 w yerrorlines pt 6



unset multiplot
