# Data and provenance

The local raw descriptor table is preserved without modifications and excluded from Git and the source archive. Obtain the original file from its owner; place it at data/raw/input_clustering_ab40.dat and check the SHA256 in docs/PROJECT_INVENTORY.md. A complete FES must be supplied separately as data/raw/FES_AB_40.dat. Partial .crdownload files are never accepted.

The CLI supports absolute or config-root-relative input paths. Project configs are relative to the repository root, specified by project_root relative to the config file. Generated processed tables retain replica and source frame identity. Test fixtures are explicitly synthetic and do not represent Aβ40 measurements.
