# this is a script of running TENET from 3 input

# ===== Dependency
# openmpi 4.1.2
# openjdk 11.0.26
# python 3.10.12
# jpype1 1.6.0
# statsmodels 0.14.5

# ===== run TENET
# run TENET with TF list
./TENET_Plus expression.csv [number_of_threads] pseudotime.txt cell.txt 1 zebrafish

# ===== Downstream analysis
# reconstructing GRN
python3 makeGRNbyTF.py zebrafish 0.05

# trimming indirect edges 
# the output file TE_result_matrix.byGRN.fdr0.05.trimIndirect0.0.sif is also used to netctrl
python3 trim_indirect.py TE_result_matrix.byGRN.fdr0.05.sif 0
