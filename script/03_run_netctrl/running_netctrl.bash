# this is a script of running netctrl for calculating network controllability

# ===== version
# netctrl 0.2.0
# igraph 0.10.3
# libxml2 2.9.13

# ===== prepare netctrl input
awk '{print $1, $3}' TE_result_matrix.byGRN.fdr0.05.trimIndirect0.0.sif > input.ncol

# ===== run netctrl
# calculate driver node
netctrl input.ncol -m liu -o liu.driver

# calculate edge fraction and count
netctrl input.ncol -m liu -M statistics -o liu.statistics
