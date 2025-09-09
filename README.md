# Controllability of the gene regulatory network in zebrafish embryogenesis 
Time-resolved single-cell GRN reconstruction and controllability analysis for zebrafish embryogenesis. 

> **Licensing**  
> - **Code**: Apache-2.0 (see `LICENSE`)  
> - **Derived data** (inferred-GRNs): CC BY 4.0 (see `LICENSE-DATA`)  
> - **Raw data** are **NOT** redistributed; please obtain from original sources.

---

## 1) What's in this repo
data/
├─ inferred_grn/ # Reconstructed GRNs (per phase)
│ ├─ phase1/ *.ncol
│ ├─ phase2/ *.ncol
│ ├─ phase3/ *.ncol
│ └─ phase4/ *.ncol
└─ tf_list/
└─ GO_symbol_zebrafish_regulation_of_transcription+sequence-specific_DNA_binding_list.txt
script/
├─ 01_mannual_clustering/ 
│ └─ prepare_TENET_input.R # (R) 
├─ 02_run_TENET/ 
│ └─ running_TENET.bash # (bash)
└─ 03_run_netctrl/ 
└─ running_netctrl.bash # (bash) 

### File formats
- **GRN files (`*.ncol`)**  
  Gene–gene edge list in NCOL-like format:  




