## Controllability of the gene regulatory network in zebrafish embryogenesis 

### 1) What's in this repo
- **data directory**  
	Reconstructed inferred-GRNs (per phase) and a TF list 
- **script directory**  
	workflow scripts (each script contains its own run commands and comments):
		- `01_mannual_clustering/prepare_TENET_input.R` — prepare inputs for TENET
		- `02_run_TENET/running_TENET.bash` — run TENET
		- `03_run_netctrl/running_netctrl.bash` — run netctrl
- ** docs directory**  
	Reproducibility and provenance documents

### File formats
- **inferred-GRN files (`*.ncol`)**  
	Gene–gene edge list in NCOL-like format:  

### 2) Data sources & provenance
- **Raw data**  
	Please download directly from the original paper (https://doi.org/10.1126/science.aar3131)
- **TF list**  
	The TF list was obtained from AnimalTFDB 4.0 (https://doi.org/10.1093/nar/gkac907)

### 3) Third-party tools
- **TENET**  
	The TENET is a Tool for Reconstructing Gene regulatory networks from scRNA-seq   
	Paper / GitHub: (https://doi.org/10.1093/nar/gkaa1014), (https://github.com/hg0426/TENETPLUS)
	
- **netctrl**  
	The netctrl is a Tool for searching driver nodes in complex networks   
	Paper / GitHub: (https://doi.org/10.1038/nature10011), (https://github.com/ntamas/netctrl)

> Please see comments and commands inside each script under `script/`

---

> **Licensing**  
> - **Code**: Apache-2.0 (see `LICENSE`)  
> - **Derived data** (inferred-GRNs): CC BY 4.0 (see `LICENSE-DATA`)  
> - **Raw data** are **NOT** redistributed; please obtain from original sources.
