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
python3 makeGRNbyTF.py zebrafish 0.05
python3 trim_indirect.py TE_result_matrix.byGRN.fdr0.05.sif 0
python3 countOutdegree.py TE_result_matrix.byGRN.fdr0.05.trimIndirect0.0.sif
