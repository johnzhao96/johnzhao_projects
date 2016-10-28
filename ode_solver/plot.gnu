set terminal png
set style data lines
unset key

set output "plot_pngs/marble_trace_non_rotating.png"
set xrange [-6500000 : 6500000]
set yrange [-6500000 : 6500000]
set title "Marble Trace in Non-rotating Plane"
plot 'plots/marble_trace.txt' using 1:2

set output "plot_pngs/marble_trace_rotating.png"
set title "Marble Trace in Rotating Plane"
theta(t) =  2 * pi * t / (24*60*60)
plot 'plots/marble_trace.txt' using (cos(theta($3))*$1 - sin(theta($3))*$2):(sin(theta($3))*$1 + cos(theta($3))*$2)

unset xrange
set yrange [0 : 40000000]

set output "plot_pngs/energy.png"
set title "Energy of Marble vs Time"
plot 'plots/marble_trace.txt' using 3:5

unset yrange

set output "plot_pngs/dt.png"
set title "log10(dt) vs Time"
plot 'plots/marble_trace.txt' using 3:4
