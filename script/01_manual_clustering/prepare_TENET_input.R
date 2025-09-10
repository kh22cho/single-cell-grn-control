# first you need download a raw data in original paper 
Zebrafish <- readRDS("[PATH]/URD_Zebrafish_Object.rds")

# ===== URD object subset
# use metadata from object
metadata <- Zebrafish@meta

# we provide which cell type use which stage and segmentation in excel file
# first, trajectory filtering
zf <- Zebrafish@group.ids %>% filter(segment %in% c("[segment information]"))
# second, zebrafish developmental stage filering
zf <- zf %>% filter(init %in% c("[zebrafish developmental stage 1]", "[zebrafish developmental stage 2]"))

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

# now we make 3 TENET input succesfully!
