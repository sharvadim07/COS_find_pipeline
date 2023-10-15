#!/bin/bash

COS_FASTA=$1
CONTIGS_FASTA=$2
CONTIGS_BLAST_DB=$3
NUM_BP_L=$4
NUM_BP_R=$5
NUM_BP_AROUND=$6
OUT_DIR=$7
PREFIX=$8

set -e
#-evalue 1e-10 \

script_dir=$(dirname $(readlink -f $0))
aux_scripts=${script_dir}/aux_scripts
select_first_last_from_fasta=${aux_scripts}/select_first_last_from_fasta.py
find_in_contigs_st_end_blast_and_cut=${aux_scripts}/find_in_contigs_st_end_blast_and_cut.py

mkdir -p ${OUT_DIR}
cd ${OUT_DIR}

LOG=${OUT_DIR}/COS_find_pipeline.log


if  [[ $1 && $2 && $3 && $4 && $5 && $6 && $7 && $8 ]]
then

### Stage 0
if  [[ ${CONTIGS_BLAST_DB} == 'none' ]]                 
then
makeblastdb -in ${CONTIGS_BLAST_DB} -dbtype nucl -out ${OUT_DIR}/CONTIGS_db \
|| { echo "Error in makeblastdb!" >> ${LOG}; exit 1; }
CONTIGS_BLAST_DB=${OUT_DIR}/CONTIGS_db
fi

### Stage 1 
cat ${COS_FASTA} | sed 's/ /_/g' | sed 's/<//g' > ${OUT_DIR}/${PREFIX}_COS.fasta
COS_FASTA=${OUT_DIR}/${PREFIX}_COS.fasta
python3.8 $select_first_last_from_fasta \
-f ${COS_FASTA} \
-l ${NUM_BP_L} \
-r ${NUM_BP_R} \
|| { echo "Error in select_first_last_from_fasta.py!" >> ${LOG}; exit 1; }

left_right_seq_file=`ls ${OUT_DIR}/left_*_right_*`
mv ${left_right_seq_file} ${OUT_DIR}/${PREFIX}_left_${NUM_BP_L}_right_${NUM_BP_R}.fasta
left_right_seq_file=${OUT_DIR}/${PREFIX}_left_${NUM_BP_L}_right_${NUM_BP_R}.fasta


### Stage 2 BLAST
date > ${LOG}
echo "Start BLAST" >> ${LOG}
blastn -task blastn \
-query ${left_right_seq_file} \
-db ${CONTIGS_BLAST_DB} \
-qcov_hsp_perc 30 \
-outfmt 5 \
-num_threads 2 \
-out ${OUT_DIR}/${PREFIX}_left_${NUM_BP_L}_right_${NUM_BP_R}_vs_contigs.xml \
|| { echo "Error in blastn!" >> ${LOG}; exit 1; }

blast_res=${OUT_DIR}/${PREFIX}_left_${NUM_BP_L}_right_${NUM_BP_R}_vs_contigs.xml

date > ${LOG}
echo "End BLAST" >> ${LOG}

### Stage 3 find_in_contigs_st_end_blast_and_cut
python3 $find_in_contigs_st_end_blast_and_cut \
-f ${CONTIGS_FASTA} \
-b ${blast_res} \
-l ${NUM_BP_AROUND} \
|| { echo "Error in find_in_contigs_st_end_blast_and_cut.py!" >> ${LOG}; exit 1; }

cd ${OUT_DIR}
selected_res_seq=`ls exact_selected_COS_from_*`
mv ${selected_res_seq} ${OUT_DIR}/${PREFIX}_around_${NUM_BP_AROUND}_${selected_res_seq}


fi
