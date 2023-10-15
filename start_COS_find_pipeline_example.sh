#!/bin/bash

#COS_FASTA=$1
#CONTIGS_FASTA=$2
#CONTIGS_BLAST_DB=$3
#NUM_BP_L=$4
#NUM_BP_R=$5
#NUM_BP_AROUND=$6
#OUT_DIR=$7
#PREFIX=$8

set -e

`pwd`/COS_find_pipeline.sh \
/gpfs/SharedDATA/Betula/COS_4/coding_seqs_cos/cross_blast_single_copy_COS/Betula_nana/b500_gwdg_nana_vs_pe_db_vs_pl_db.fasta \
/gpfs/SharedDATA/Betula/COS_4/contigs/GCA_000327005_Betula_nana.fna \
/gpfs/SharedDATA/Betula/COS_4/contigs/GCA_000327005_Betula_nana.fna \
50 \
50 \
1000 \
/gpfs/SharedDATA/Betula/COS_4/selected_Betula_nana/b500_gwdg_nana_vs_pe_db_vs_pl_db \
b500_gwdg_nana_vs_pe_db_vs_pl_db

####
