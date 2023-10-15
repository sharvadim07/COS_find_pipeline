import argparse
import os
from Bio import SeqIO

parser = argparse.ArgumentParser(
    description='Take only last bp from all sequences of fasta file.')

parser.add_argument('-f', '--fasta_file', type=str,
                    help='Fasta file input.', required=True)
parser.add_argument('-l', '--num_bp_l', type=int,
                    help='Get bp from left part of sequences.', required=True)
parser.add_argument('-r', '--num_bp_r', type=int,
                    help='Get bp from right part of sequences.', required=True)

args = parser.parse_args()


def take_right_bp(in_fasta_file_name, l_bp_num, r_bp_num):
    with open('left_' + str(l_bp_num) + '_' + 'right_' + str(r_bp_num) + '_' + os.path.basename(in_fasta_file_name), 'w') as out_fasta:
        for i, record in enumerate(SeqIO.parse(in_fasta_file_name, "fasta")):
            out_fasta.write('>' + str(i) + ':' + record.description + '_left_' + str(l_bp_num) + '\n' + str(record.seq[:l_bp_num]) + '\n')
            out_fasta.write('>' + str(i) + ':' + record.description + '_right_' + str(r_bp_num) + '\n' + str(record.seq[-r_bp_num:]) + '\n')

take_right_bp(args.fasta_file, args.num_bp_l, args.num_bp_r)