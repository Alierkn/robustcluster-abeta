# Questions needed to complete the equilibrium analysis

These questions are prepared for the data provider. No message has been sent.

For the supplied `FES_AB_40.dat` (SHA256 `6fd6c3d7c04e20859cf91abb4765e126e0f3fcb982d3795b643165dde26fa3f4`):

1. Are the `file.free` values in kJ/mol, and do they represent the reconstructed free energy F rather than the final bias or a differently scaled quantity?
2. Which PLUMED/sum_hills command and UNITS setting produced the file? Was a flag such as `--negbias` used?
3. How were the three replicas combined, including energy-offset alignment, averaging/combination operation and time interval?
4. Are the generating HILLS/COLVAR and PLUMED input available for verification? For a separate time-dependent comparison, how was the supplied `metad.rbias` column generated and in which units?

The grid is complete and every converted descriptor query lies inside it. These questions concern its physical interpretation, not download completeness.
