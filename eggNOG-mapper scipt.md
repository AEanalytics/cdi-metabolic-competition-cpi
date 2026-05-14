### eggNOG-mapper

We map the protein sequences from both genomes to their respective KEGG pathways by running the protein sequences through eggNOG-mapper. The code used is below

### c_difficile
```bash
emapper.py -i GCA_018885085.1_ASM1888508v1_protein.faa \
--data_dir ~/eggnog_db \
--database bact \
-o C_difficile_annotations
```

### c_scindens
```bash
emapper.py -i GCA_004295125.1_ASM429512v1_protein.faa \
--data_dir ~/eggnog_db \
--database bact \
-o C_scindens_annotations
```

### Paraclostridium bifermentans 
```bash
emapper.py -i GCF_019916025.1_ASM1991602v1_protein.faa \
--data_dir ~/eggnog_db \
--output Paraclostridium_bifermentans_annotations \
--cpu 4
```

### Faecalibacterium prausnitzii

```bash
emapper.py -i Faecalibacterium_prausnitzii.faa \
--data_dir ~/eggnog_db \
--database bact \
-o Faecalibacterium_prausnitzii_annotations \
--cpu 4 
```

### Clostridium_sardiniense
```bash
emapper.py -i Clostridium_sardiniense.faa \
--data_dir ~/eggnog_db \
--database bact \
-o Clostridium_sardiniense_annotations \
--cpu 4 
```
