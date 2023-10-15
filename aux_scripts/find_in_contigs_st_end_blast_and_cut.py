import argparse
import os
from Bio import SeqIO
from Bio.Blast import NCBIXML
import logging

parser = argparse.ArgumentParser(
    description='Take only last bp from all sequences of fasta file.')

parser.add_argument('-f', '--fasta_file', type=str,
                    help='Fasta file input.', required=True)
parser.add_argument('-b', '--blast_file', type=str,
                    help='BLAST xml file input.', required=True)
parser.add_argument('-l', '--num_bp_around', type=int,
                    help='Get bp around of sequences.', required=True)

args = parser.parse_args()
logging.basicConfig(filename='find_in_contigs_st_end_blast_and_cut.log', level=logging.INFO)

def set_pos(blast_record, cont_seq_found_start_end_pos_dict, hit_def, seq_name):
    if '_left_' in blast_record.query:
        if blast_record.alignments[0].hsps[0].strand[1] == 'Minus':
            cont_seq_found_start_end_pos_dict[hit_def][seq_name][1] = \
                blast_record.alignments[0].hsps[0].sbjct_start
        else:
            cont_seq_found_start_end_pos_dict[hit_def][seq_name][0] = \
                blast_record.alignments[0].hsps[0].sbjct_start
    elif '_right_' in blast_record.query:
        if blast_record.alignments[0].hsps[0].strand[1] == 'Minus':
            cont_seq_found_start_end_pos_dict[hit_def][seq_name][0] = \
                blast_record.alignments[0].hsps[0].sbjct_end
        else:
            cont_seq_found_start_end_pos_dict[hit_def][seq_name][1] = \
                blast_record.alignments[0].hsps[0].sbjct_end
    else:
        raise ValueError('left and right not found in name!')
    
def proc_blast_xml(blast_out_xml_name):
    result_handle = open(blast_out_xml_name)
    blast_records = NCBIXML.parse(result_handle)
    cont_seq_found_start_end_pos_dict = {}
    for blast_record in blast_records:
        if len(blast_record.alignments) == 0:
            logging.info(blast_record.query + ' - not found in input contigs.')
            continue
        hit_def = blast_record.alignments[0].hit_def
        if blast_record.alignments[0].hit_def not in cont_seq_found_start_end_pos_dict:
            cont_seq_found_start_end_pos_dict[hit_def] = {}
        #seq_name = ':'.join(blast_record.query.split(':')[:-1])
        seq_name = blast_record.query
        if '_left_' in seq_name:
            seq_name = seq_name.split('_left_')[0]
        elif '_right_' in seq_name:
            seq_name = seq_name.split('_right_')[0]

        if seq_name not in cont_seq_found_start_end_pos_dict[hit_def]:
            cont_seq_found_start_end_pos_dict[hit_def][seq_name] = [None, None]
        set_pos(blast_record, cont_seq_found_start_end_pos_dict, hit_def, seq_name)      
            
    return cont_seq_found_start_end_pos_dict

def take_seq_around_with_start_end(in_fasta_file_name, cont_seq_found_start_end_pos_dict, around = 0):
    with open('exact_selected_COS_from_' + os.path.basename(in_fasta_file_name), 'w') as out_fasta:
        for record in SeqIO.parse(in_fasta_file_name, "fasta"):
            if record.description in cont_seq_found_start_end_pos_dict:
                for seq_name in cont_seq_found_start_end_pos_dict[record.description]:
                    start_pos = cont_seq_found_start_end_pos_dict[record.description][seq_name][0]
                    end_pos = cont_seq_found_start_end_pos_dict[record.description][seq_name][1]
                    if start_pos != None and end_pos != None:
                        start_pos = start_pos - around - 1
                        end_pos = end_pos + around
                        if start_pos < 0:
                            start_pos = 0
                        if end_pos >= len(record.seq):
                            end_pos = len(record.seq)
                        out_fasta.write('>' + seq_name + ':' + str(start_pos) + '-' + str(end_pos) + '\n' + str(record.seq[start_pos:end_pos]) + '\n')

cont_seq_found_start_end_pos_dict = proc_blast_xml(args.blast_file)
take_seq_around_with_start_end(args.fasta_file, cont_seq_found_start_end_pos_dict, args.num_bp_around)
