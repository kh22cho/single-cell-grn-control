# this is a script of zebrafish embryogenesis 40 cell type cluster

# ===== preparation
# package load
library(dplyr)

# first you need download a raw data in 10.1126/science.aar3131
Zebrafish <- readRDS("[PATH]/URD_Zebrafish_Object.rds")

# ===== URD object subset
# use metadata from object
metadata <- Zebrafish@meta

# we provide which cell type use which stage and segmentation in excel file
# if you want subset just one zebrafish developmental stage
zf <- metadata %>% filter(STAGE == "[zebrafish developmental stage]") 
# or multiple zebrafish developmental stage
zf <- metadata %>% filter(STAGE %in% c("[zebrafish developmental stage 1], [zebrafish developmental stage 2]")) 

# trajectory filtering
zf <- Zebrafish@group.ids %>% filter(segment %in% c("[segment information]"))
# extract cell barcodes
zf_cell_names <- rownames(zf)
# URD object subset based on cell barcodes
ZF_object <- urdSubset(Zebrafish, zf_cell_names)

# ===== prepare input of TENET
# TENET need 3 input; raw count expression matrix, pseudotime information, cell select file

# raw count expression matrix
exp_matrix <- t(as.data.frame(as.matrix(ZF_object@count.data)))
write.csv(exp_matrix, file = "[PATH]/expression.csv", quote = FALSE)

# pseudotime information
pseudo_matrix <- as.data.frame(as.matrix(ZF_object@pseudotime[,1]))
colnames(pseudo_matrix) <- 'psedotime'
rownames(pseudo_matrix) <- row.names(ZF_object@pseudotime)
write.table(pseudo_matrix, file = "[PATH]/pseudotime.txt", row.names = FALSE, col.names = FALSE)

# cell select file, we just use all cell
select_file <- matrix(1, length(t(pseudo_matrix)))
colnames(select_file) <- 'select'
rownames(select_file) <- row.names(ZF_object@pseudotime)
write.table(select_file, file = "[PATH]/cell.txt", row.names = FALSE, col.names = FALSE)
