---
tags: [gradio-custom-component, SimpleTextbox]
title: gradio_perturbation_graph
short_description: 
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_perturbation_graph`
<a href="https://pypi.org/project/gradio_perturbation_graph/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_perturbation_graph"></a>  

Python library for easily interacting with trained machine learning models

## Installation

```bash
pip install gradio_perturbation_graph
```

## Usage

```python

import gradio as gr
from gradio_perturbation_graph import perturbation_graph
import json

default = {"ligands": [{"name": "4g", "content": "4g\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.8923   39.9203   68.4006 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0165   40.2127   67.4304 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2640   39.8257   66.1503 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4483   39.0944   65.8451 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.3218   38.8195   66.8379 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9926   39.2534   68.0473 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.2919   40.9677   63.2538 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.9432   40.3275   64.3911 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8788   39.9516   65.3742 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2449   40.2418   65.1706 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6000   40.9184   63.9830 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.5940   41.2601   63.0612 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.6112   37.5983   61.9541 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5856   38.0630   62.8536 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1983   38.5389   64.1189 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8370   38.5679   64.5131 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8781   38.0641   63.6022 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.2579   37.5988   62.3303 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.9796   69.0287 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.9447   41.9779   61.7744 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.4692   40.0215   64.5589 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5597   39.4359   66.2697 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.6317   41.1681   63.7806 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.9018   37.2394   60.9779 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.6287   38.0594   62.5740 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9651   38.8967   64.7914 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.8337   38.0252   63.8729 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5065   37.2379   61.6440 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.7954   38.5755   68.8020 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.6995   39.2616   69.9892 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.7589   42.6851   61.9378 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2614   41.2599   61.0167 H   0  0  0  0  0  0  0  0  0  0  0  0\n   38.0904   42.5334   61.3862 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2961   39.3711   65.4177 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.0769   39.5211   63.6720 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9055   40.9433   64.7111 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n45\n\n>  <s_m_entry_name>  (1) \n4g.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4g.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n9\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.6907191665867\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.509081865075556\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.40451826388878\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.64325871130641\n\n>  <r_glide_XP_GScore>  (1) \n-10.6907191665867\n\n>  <r_i_glide_gscore>  (1) \n-10.6907191665867\n\n>  <r_i_glide_evdw>  (1) \n-37.0795974731445\n\n>  <r_i_glide_ecoul>  (1) \n-10.3729629516602\n\n>  <r_i_glide_energy>  (1) \n-47.4525604248047\n\n>  <r_i_glide_einternal>  (1) \n0.266062557697296\n\n>  <r_i_glide_emodel>  (1) \n-76.7900510348869\n\n>  <r_glide_XP_HBond>  (1) \n-2.1998989631454\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n13\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}, {"name": "4h", "content": "4h\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.9064   39.7369   68.5006 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0280   40.0883   67.5529 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2502   39.7559   66.2528 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4272   39.0295   65.9030 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.3091   38.7005   66.8734 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9945   39.0716   68.1083 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.1883   41.0713   63.5115 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.8693   40.4631   64.6733 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8364   40.0225   65.5968 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2070   40.2192   65.3140 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.5298   40.8624   64.0979 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.4933   41.2626   63.2350 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.5445   37.6383   61.9633 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.1962   37.6236   62.3574 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8305   38.0632   63.6420 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8008   38.5490   64.5503 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1576   38.5312   64.1396 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5300   38.0851   62.8582 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.7334   69.0706 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.8101   41.9374   61.9174 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.3903   40.2666   64.9335 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5333   39.5330   66.5116 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5599   41.0442   63.8288 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8908   37.2225   60.7243 F   0  0  0  0  0  0  0  0  0  0  0  0\n   40.4423   37.2636   61.6744 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.7896   38.0165   63.9263 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9333   38.8717   64.8110 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.5687   38.0872   62.5617 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.8347   38.4624   68.8045 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.7438   39.0734   70.0189 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6903   42.5745   62.0138 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.0087   41.1862   61.1522 H   0  0  0  0  0  0  0  0  0  0  0  0\n   37.9793   42.5589   61.5830 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2205   39.6511   65.8173 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9130   39.7749   64.0847 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9048   41.2307   65.0904 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n42\n\n>  <s_m_entry_name>  (1) \n4h.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4h.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n10\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.9240224934919\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.496546476976904\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.39134275655409\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.67022956081143\n\n>  <r_glide_XP_GScore>  (1) \n-10.9240224934919\n\n>  <r_i_glide_gscore>  (1) \n-10.9240224934919\n\n>  <r_i_glide_evdw>  (1) \n-37.0752029418945\n\n>  <r_i_glide_ecoul>  (1) \n-11.095742225647\n\n>  <r_i_glide_energy>  (1) \n-48.1709451675415\n\n>  <r_i_glide_einternal>  (1) \n3.07485175132751\n\n>  <r_i_glide_emodel>  (1) \n-75.4398956663047\n\n>  <r_glide_XP_HBond>  (1) \n-1.85263067703808\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n1\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}, {"name": "4i", "content": "4i\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.8919   39.9317   68.6581 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0062   40.2477   67.7050 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2293   39.8896   66.4121 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4109   39.1628   66.0762 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.2926   38.8541   67.0549 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9814   39.2610   68.2822 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.1366   41.1072   63.6536 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.8345   40.5359   64.8379 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8118   40.1268   65.7650 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.1781   40.3269   65.4674 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.4851   40.9403   64.2316 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.4395   41.2915   63.3572 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.5871   37.9688   62.0816 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.2328   37.9406   62.4555 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8537   38.2632   63.7697 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8047   38.7058   64.7192 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1636   38.7278   64.3193 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5534   38.3726   63.0164 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.9778   69.2530 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.7425   41.9063   62.0065 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.3609   40.3520   65.1242 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5178   39.6622   66.6955 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5110   41.1263   63.9498 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8789   37.7138   61.0741 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2821   37.6626   61.5356 F   0  0  0  0  0  0  0  0  0  0  0  0\n   39.8066   38.2069   64.0260 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9312   39.0505   65.0048 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.8543   38.4616   62.6542 F   0  0  0  0  0  0  0  0  0  0  0  0\n   43.7770   38.5476   69.0070 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.7222   39.2594   70.2322 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6477   42.5128   62.0545 H   0  0  0  0  0  0  0  0  0  0  0  0\n   38.8924   41.1219   61.2636 H   0  0  0  0  0  0  0  0  0  0  0  0\n   37.9250   42.5441   61.6695 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2015   39.7693   66.0313 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.8704   39.8358   64.2983 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.8902   41.3262   65.2534 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n46\n\n>  <s_m_entry_name>  (1) \n4i.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4i.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n1\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.6533176352112\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.463187723270053\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.31724427030359\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.57606880313763\n\n>  <r_glide_XP_GScore>  (1) \n-10.6533176352112\n\n>  <r_i_glide_gscore>  (1) \n-10.6533176352112\n\n>  <r_i_glide_evdw>  (1) \n-35.6582565307617\n\n>  <r_i_glide_ecoul>  (1) \n-11.9602022171021\n\n>  <r_i_glide_energy>  (1) \n-47.6184587478638\n\n>  <r_i_glide_einternal>  (1) \n1.16375911235809\n\n>  <r_i_glide_emodel>  (1) \n-78.3857381921686\n\n>  <r_glide_XP_HBond>  (1) \n-1.79390146925849\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n13\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}], "pairs": [{"ligandA": "4g", "ligandB": "4h", "similarity": 0.90173, "link": False}, {"ligandA": "4g", "ligandB": "4i", "similarity": 0.8154, "link": True}, {"ligandA": "4h", "ligandB": "4i", "similarity": 0.73849, "link": True}]}

defaultStr = json.dumps(default)

after = {"ligands": [{"name": "4g", "content": "4g\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.8923   39.9203   68.4006 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0165   40.2127   67.4304 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2640   39.8257   66.1503 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4483   39.0944   65.8451 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.3218   38.8195   66.8379 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9926   39.2534   68.0473 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.2919   40.9677   63.2538 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.9432   40.3275   64.3911 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8788   39.9516   65.3742 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2449   40.2418   65.1706 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6000   40.9184   63.9830 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.5940   41.2601   63.0612 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.6112   37.5983   61.9541 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5856   38.0630   62.8536 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1983   38.5389   64.1189 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8370   38.5679   64.5131 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8781   38.0641   63.6022 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.2579   37.5988   62.3303 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.9796   69.0287 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.9447   41.9779   61.7744 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.4692   40.0215   64.5589 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5597   39.4359   66.2697 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.6317   41.1681   63.7806 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.9018   37.2394   60.9779 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.6287   38.0594   62.5740 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9651   38.8967   64.7914 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.8337   38.0252   63.8729 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5065   37.2379   61.6440 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.7954   38.5755   68.8020 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.6995   39.2616   69.9892 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.7589   42.6851   61.9378 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2614   41.2599   61.0167 H   0  0  0  0  0  0  0  0  0  0  0  0\n   38.0904   42.5334   61.3862 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2961   39.3711   65.4177 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.0769   39.5211   63.6720 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9055   40.9433   64.7111 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n45\n\n>  <s_m_entry_name>  (1) \n4g.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4g.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n9\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.6907191665867\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.509081865075556\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.40451826388878\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.64325871130641\n\n>  <r_glide_XP_GScore>  (1) \n-10.6907191665867\n\n>  <r_i_glide_gscore>  (1) \n-10.6907191665867\n\n>  <r_i_glide_evdw>  (1) \n-37.0795974731445\n\n>  <r_i_glide_ecoul>  (1) \n-10.3729629516602\n\n>  <r_i_glide_energy>  (1) \n-47.4525604248047\n\n>  <r_i_glide_einternal>  (1) \n0.266062557697296\n\n>  <r_i_glide_emodel>  (1) \n-76.7900510348869\n\n>  <r_glide_XP_HBond>  (1) \n-2.1998989631454\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n13\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}, {"name": "4h", "content": "4h\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.9064   39.7369   68.5006 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0280   40.0883   67.5529 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2502   39.7559   66.2528 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4272   39.0295   65.9030 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.3091   38.7005   66.8734 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9945   39.0716   68.1083 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.1883   41.0713   63.5115 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.8693   40.4631   64.6733 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8364   40.0225   65.5968 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.2070   40.2192   65.3140 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.5298   40.8624   64.0979 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.4933   41.2626   63.2350 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.5445   37.6383   61.9633 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.1962   37.6236   62.3574 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8305   38.0632   63.6420 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8008   38.5490   64.5503 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1576   38.5312   64.1396 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5300   38.0851   62.8582 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.7334   69.0706 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.8101   41.9374   61.9174 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.3903   40.2666   64.9335 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5333   39.5330   66.5116 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5599   41.0442   63.8288 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8908   37.2225   60.7243 F   0  0  0  0  0  0  0  0  0  0  0  0\n   40.4423   37.2636   61.6744 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.7896   38.0165   63.9263 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9333   38.8717   64.8110 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.5687   38.0872   62.5617 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.8347   38.4624   68.8045 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.7438   39.0734   70.0189 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6903   42.5745   62.0138 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.0087   41.1862   61.1522 H   0  0  0  0  0  0  0  0  0  0  0  0\n   37.9793   42.5589   61.5830 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2205   39.6511   65.8173 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9130   39.7749   64.0847 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.9048   41.2307   65.0904 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n42\n\n>  <s_m_entry_name>  (1) \n4h.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4h.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n10\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.9240224934919\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.496546476976904\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.39134275655409\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.67022956081143\n\n>  <r_glide_XP_GScore>  (1) \n-10.9240224934919\n\n>  <r_i_glide_gscore>  (1) \n-10.9240224934919\n\n>  <r_i_glide_evdw>  (1) \n-37.0752029418945\n\n>  <r_i_glide_ecoul>  (1) \n-11.095742225647\n\n>  <r_i_glide_energy>  (1) \n-48.1709451675415\n\n>  <r_i_glide_einternal>  (1) \n3.07485175132751\n\n>  <r_i_glide_emodel>  (1) \n-75.4398956663047\n\n>  <r_glide_XP_HBond>  (1) \n-1.85263067703808\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n1\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}, {"name": "4i", "content": "4i\n     RDKit          3D\n\n 36 38  0  0  1  0  0  0  0  0999 V2000\n   40.8919   39.9317   68.6581 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.0062   40.2477   67.7050 N   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2293   39.8896   66.4121 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.4109   39.1628   66.0762 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.2926   38.8541   67.0549 N   0  0  0  0  0  0  0  0  0  0  0  0\n   41.9814   39.2610   68.2822 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.1366   41.1072   63.6536 N   0  0  0  0  0  0  0  0  0  0  0  0\n   36.8345   40.5359   64.8379 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.8118   40.1268   65.7650 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.1781   40.3269   65.4674 C   0  0  0  0  0  0  0  0  0  0  0  0\n   39.4851   40.9403   64.2316 C   0  0  0  0  0  0  0  0  0  0  0  0\n   38.4395   41.2915   63.3572 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.5871   37.9688   62.0816 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.2328   37.9406   62.4555 C   0  0  0  0  0  0  0  0  0  0  0  0\n   40.8537   38.2632   63.7697 C   0  0  0  0  0  0  0  0  0  0  0  0\n   41.8047   38.7058   64.7192 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.1636   38.7278   64.3193 C   0  0  0  0  0  0  0  0  0  0  0  0\n   43.5534   38.3726   63.0164 C   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8919   38.9778   69.2530 N   0  0  0  0  0  0  0  0  0  0  0  0\n   38.7425   41.9063   62.0065 C   0  0  0  0  0  0  0  0  0  0  0  0\n   35.3609   40.3520   65.1242 C   0  0  0  0  0  0  0  0  0  0  0  0\n   37.5178   39.6622   66.6955 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.5110   41.1263   63.9498 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.8789   37.7138   61.0741 H   0  0  0  0  0  0  0  0  0  0  0  0\n   40.2821   37.6626   61.5356 F   0  0  0  0  0  0  0  0  0  0  0  0\n   39.8066   38.2069   64.0260 H   0  0  0  0  0  0  0  0  0  0  0  0\n   43.9312   39.0505   65.0048 H   0  0  0  0  0  0  0  0  0  0  0  0\n   44.8543   38.4616   62.6542 F   0  0  0  0  0  0  0  0  0  0  0  0\n   43.7770   38.5476   69.0070 H   0  0  0  0  0  0  0  0  0  0  0  0\n   42.7222   39.2594   70.2322 H   0  0  0  0  0  0  0  0  0  0  0  0\n   39.6477   42.5128   62.0545 H   0  0  0  0  0  0  0  0  0  0  0  0\n   38.8924   41.1219   61.2636 H   0  0  0  0  0  0  0  0  0  0  0  0\n   37.9250   42.5441   61.6695 H   0  0  0  0  0  0  0  0  0  0  0  0\n   35.2015   39.7693   66.0313 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.8704   39.8358   64.2983 H   0  0  0  0  0  0  0  0  0  0  0  0\n   34.8902   41.3262   65.2534 H   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0\n  1  6  1  0\n  2  3  1  0\n  3  4  2  0\n  3 10  1  0\n  4  5  1  0\n  4 16  1  0\n  5  6  2  0\n  6 19  1  0\n  7  8  2  0\n  7 12  1  0\n  8  9  1  0\n  8 21  1  0\n  9 10  2  0\n  9 22  1  0\n 10 11  1  0\n 11 12  2  0\n 11 23  1  0\n 12 20  1  0\n 13 14  2  0\n 13 18  1  0\n 13 24  1  0\n 14 15  1  0\n 14 25  1  0\n 15 16  2  0\n 15 26  1  0\n 16 17  1  0\n 17 18  2  0\n 17 27  1  0\n 18 28  1  0\n 19 29  1  0\n 19 30  1  0\n 20 31  1  0\n 20 32  1  0\n 20 33  1  0\n 21 34  1  0\n 21 35  1  0\n 21 36  1  0\nM  END\n>  <s_m_entry_id>  (1) \n46\n\n>  <s_m_entry_name>  (1) \n4i.1\n\n>  <s_pdb_PDB_format_version>  (1) \n3.0\n\n>  <s_m_Source_Path>  (1) \nD:\\DPLC\\A2A-OPTI\\10mole\\sdf\n\n>  <s_m_Source_File>  (1) \n4i.sdf\n\n>  <i_m_Source_File_Index>  (1) \n1\n\n>  <s_pdb_PDB_TITLE>  (1) \nSTRUCTURE OF THE A2A-STAR2-BRIL562-COMPOUND 4E COMPLEX AT 1.9A OBTAINED FROM BESPOKE CO-CRYSTALLISATION EXPERIMENTS.\n\n>  <r_pdb_PDB_CRYST1_a>  (1) \n39.369\n\n>  <r_pdb_PDB_CRYST1_b>  (1) \n179.247\n\n>  <r_pdb_PDB_CRYST1_c>  (1) \n140.066\n\n>  <r_pdb_PDB_CRYST1_alpha>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_beta>  (1) \n90\n\n>  <r_pdb_PDB_CRYST1_gamma>  (1) \n90\n\n>  <s_pdb_PDB_CRYST1_Space_Group>  (1) \nC 2 2 21\n\n>  <r_mpc_ALogP>  (1) \n3.9604\n\n>  <s_mpc_SMILES>  (1) \nFC(F)(F)c1cc(cc(n1)C)-c(nnc(n2)N)c2-c3ccc(F)cc3\n\n>  <s_pdb_PDB_ID>  (1) \n5OLZ\n\n>  <i_pdb_PDB_CRYST1_z>  (1) \n8\n\n>  <s_pdb_PDB_CLASSIFICATION>  (1) \nMEMBRANE PROTEIN\n\n>  <s_pdb_PDB_DEPOSITION_DATE>  (1) \n28-JUL-17\n\n>  <r_pdb_PDB_R>  (1) \n0.173\n\n>  <r_pdb_PDB_Rfree>  (1) \n0.196\n\n>  <r_pdb_PDB_RESOLUTION>  (1) \n1.9\n\n>  <s_pdb_PDB_EXPDTA>  (1) \nX-RAY DIFFRACTION\n\n>  <r_pdb_PDB_EXPDTA_TEMPERATURE>  (1) \n100\n\n>  <r_pdb_PDB_EXPDTA_PH>  (1) \n5.3\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Chains>  (1) \nA\n\n>  <s_pdb_PDB_REMARK_350_Biomolecule_1_Transform_1_Matrix_1>  (1) \n1.000000 0.000000 0.000000   0.000000;0.000000 1.000000 0.000000   0.000000;0.000000 0.000000 1.000000   0.000000\n\n>  <s_m_job_name>  (1) \nglide-dock_XP_42\n\n>  <i_glide_grid_version>  (1) \n94137\n\n>  <r_glide_gridbox_xcent>  (1) \n-20.9351295\n\n>  <r_glide_gridbox_ycent>  (1) \n4.78096038888889\n\n>  <r_glide_gridbox_zcent>  (1) \n17.6285738055556\n\n>  <r_glide_gridbox_xrange>  (1) \n18\n\n>  <r_glide_gridbox_yrange>  (1) \n18\n\n>  <r_glide_gridbox_zrange>  (1) \n18\n\n>  <r_glide_gridbox_ligxrange>  (1) \n10\n\n>  <r_glide_gridbox_ligyrange>  (1) \n10\n\n>  <r_glide_gridbox_ligzrange>  (1) \n10\n\n>  <s_glide_grid_type>  (1) \nglide\n\n>  <s_i_glide_gridfile>  (1) \nglide-grid_12\n\n>  <i_i_glide_lignum>  (1) \n1\n\n>  <i_i_glide_rotatable_bonds>  (1) \n2\n\n>  <r_i_docking_score>  (1) \n-10.6533176352112\n\n>  <r_i_glide_ligand_efficiency>  (1) \n-0.463187723270053\n\n>  <r_i_glide_ligand_efficiency_sa>  (1) \n-1.31724427030359\n\n>  <r_i_glide_ligand_efficiency_ln>  (1) \n-2.57606880313763\n\n>  <r_glide_XP_GScore>  (1) \n-10.6533176352112\n\n>  <r_i_glide_gscore>  (1) \n-10.6533176352112\n\n>  <r_i_glide_evdw>  (1) \n-35.6582565307617\n\n>  <r_i_glide_ecoul>  (1) \n-11.9602022171021\n\n>  <r_i_glide_energy>  (1) \n-47.6184587478638\n\n>  <r_i_glide_einternal>  (1) \n1.16375911235809\n\n>  <r_i_glide_emodel>  (1) \n-78.3857381921686\n\n>  <r_glide_XP_HBond>  (1) \n-1.79390146925849\n\n>  <i_i_glide_confnum>  (1) \n1\n\n>  <i_i_glide_posenum>  (1) \n13\n\n>  <r_i_glide_eff_state_penalty>  (1) \n0\n\n>  <i_glide_XP_PoseRank>  (1) \n1\n\n>  <r_i_glide_rmsd>  (1) \n1.35407454623776e-06\n\n>  <s_glide_core_constrain_type>  (1) \nsnapped_core_restrain\n\n>  <s_glide_core_smarts>  (1) \n[*]~[*]~1~[*]~[*]~[*](~[*])~[*]~[*]1~[*]~2~[*]~[*]~[*]~[*]~[*]2\n\n>  <s_glide_core_atoms>  (1) \n4 3 2 8 7 5 1 12 11 10 9 14 13 6\n\n>  <i_lp_mmshare_version>  (1) \n57137\n\n>  <s_epik_input>  (1) \nRmMxW2NIXVtjSF1jKFtjSF1bY0hdMSktYzJuYyhbTkgyXSlubmMyLWMoW2NIXTMpW2NIXWMoQyhGKShGKUYpbmMzW0NIM10=\n\n>  <s_epik_cmdline>  (1) \nJ2VwaWtfcHl0aG9uJywgJy1waCcsICc3LjQnLCAnLXRuJywgJzgnLCAnLW1hJywgJzUwMCcsICctaW1hZScsICc8aW5maWxlLm1hZT4nLCAnLW9tYWUnLCAnPG91dGZpbGUubWFlPic=\n\n>  <r_lp_tautomer_probability>  (1) \n1\n\n>  <r_epik_Ionization_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Charging>  (1) \n  0.0000\n\n>  <r_epik_Ionization_Penalty_Neutral>  (1) \n  0.0000\n\n>  <r_epik_State_Penalty>  (1) \n  0.0000\n\n>  <r_epik_Charging_Adjusted_Penalty>  (1) \n0\n\n>  <i_epik_Tot_Q>  (1) \n0\n\n>  <i_epik_Tot_abs_Q>  (1) \n0\n\n>  <i_f3d_flags>  (1) \n0\n\n>  <s_lp_Force_Field>  (1) \nS-OPLS\n\n>  <r_lp_Energy>  (1) \n41.638328\n\n>  <b_lp_Chiralities_Consistent>  (1) \n1\n\n>  <s_lp_Variant>  (1) \n4l-1\n\n>  <s_m_subgroup_title>  (1) \nglide-dock_XP_42_pv1\n\n>  <s_m_subgroupid>  (1) \nglide-dock_XP_42_pv1\n\n>  <b_m_subgroup_collapsed>  (1) \n0\n\n$$$$\n", "formalCharge": None, "expDG": None}], "pairs": [{"ligandA": "4g", "ligandB": "4h", "similarity": 0.90173, "link": True}, {"ligandA": "4g", "ligandB": "4i", "similarity": 0.8154, "link": True}, {"ligandA": "4h", "ligandB": "4i", "similarity": 0.73849, "link": True}]}
afterStr = json.dumps(after)
with gr.Blocks() as demo:
    with gr.Row():
        perturbation = perturbation_graph(placeholder=defaultStr, visible=True)
    with gr.Row():
        showbox_button = gr.Button("Calculation")
        update_button = gr.Button("Update")
    def my_print_function():
        return perturbation_graph(placeholder=afterStr, visible=True)
        # print(after['pairs'])
        # for pair in list(after['pairs']):
        #     def match(item):
        #         return item['ligandA'] == pair['ligandA'] and item['ligandB'] == pair['ligandB']
        #     target = list(filter(lambda item: item['ligandA'] == pair['ligandA'] and item['ligandB'] == pair['ligandB'], a))
        #     if len(target) > 0:
        #         pair['link'] = True
        #     else:
        #         pair["link"] = False
        

    def updatePerturbation1():
        print('Click1')
        return perturbation_graph(placeholder=defaultStr, visible=True)
    showbox_button.click(
        updatePerturbation1,
        outputs=perturbation,
    )
    perturbation.change(
        my_print_function,
        outputs=perturbation,
    )
    print(dir(perturbation))
    def updatePerturbation():
        print('Click')
        return perturbation_graph(placeholder=afterStr, visible=True)
    update_button.click(updatePerturbation, outputs=perturbation)

if __name__ == "__main__":
    demo.launch()
```

## `perturbation_graph`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>placeholder</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">placeholder hint to provide behind textbox.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">component name in interface.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>rtl</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `input` | This listener is triggered when the user changes the value of the perturbation_graph. |
| `change` | Triggered when the value of the perturbation_graph changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `submit` | This listener is triggered when the user presses the Enter key while the perturbation_graph is focused. |
| `like` | This listener is triggered when the user likes/dislikes from within the perturbation_graph. This event has EventData of type gradio.LikeData that carries information, accessible through LikeData.index and LikeData.value. See EventData documentation on how to use this event data. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes text value as a {str} into the function.
- **As input:** Should return, expects a {str} returned from function and sets textarea value to it.

 ```python
 def predict(
     value: str | None
 ) -> str | None:
     return value
 ```
 
