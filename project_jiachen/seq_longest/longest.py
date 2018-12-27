from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os

basePath = 'data/'
#fileName = 'hemiptera.fasta'
fileName = 'hemiptera.fasta'
file = os.path.join(basePath, fileName)
seq_records = SeqIO.parse(file, 'fasta')
res = {}

for seq in seq_records:
    if seq.name not in res.keys():
        res[seq.name] = seq
    else:
        if len(res[seq.name].seq) < len(seq.seq):
            res[seq.name] = seq
SeqIO.write(res.values(), os.path.join(basePath, 'res.fasta'), 'fasta')
