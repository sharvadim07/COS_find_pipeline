# COS_find_pipeline
Pipeline of procedure of COS extraction from genome (contigs)

## Algorithm
1. From each sequence, 50 nts are cut off from the beginning. and from the end of 50 n.a.;
2. Blastom finds the location of these segments.
blastn parameters:
-evalue 1e-10
-qcov_hsp_perc 50 (minimum percentage of alignment length from segment length).
Keep in mind that sometimes the blast found segments in the reverse strand of the contig, this is taken into account.
The blast does not find some segments in contigs (they represent about 5% of sequences).
3. Positions (beginning of the first segment 50 nt, end of the second segment 50 nt) found by the blast are cut out from the contigs, including another 1000 nt. on both sides (or to the ends of the contig).
4. Segments of 15 n.a. are created. on the left and on the right from BUSCO genes that were not found in the contigs.

## How to use
To work you need:
python version no lower than 3.8 (if it is older, the results will not be correct)
biopython https://biopython.org/wiki/Download
ncbi-blast
  
COS_find_pipeline.sh is a bash script with main pipeline. You just need to run it.
aux_scripts - this directory must be located in the directory with COS_find_pipeline.sh
 
Make COS_find_pipeline.sh executable using the command chmod +x ./COS_find_pipeline.sh
 
The parameters for launching COS_find_pipeline.sh are specified in order:
1. Path to the file with COS;
2. Path to the file with contigs;
3. Path to the blast database for contigs, or you can specify none and the database will be built;
4. The number of nucleotides that need to be cut from the 5' end of COS (default 50);
5. The number of nucleotides that need to be cut from the 3' end of COS (default 50);
6. The number of nucleotides around the found COS ends that we cut from the contigs (default 1000);
7. Output directory;
8. Prefix for output files;

An example of how to run it here:
start_COS_find_pipeline_example.sh
