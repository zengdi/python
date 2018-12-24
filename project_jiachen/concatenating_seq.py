from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os


class RebuildData(object):
    def __init__(self, path):
        self.basePath = path
        self.spName = set()
        self.__data = {}
        self.__seqs = {}
        self.fileNames = []
        self.seqRecords = []
        self.data_construction()
        self.buildSeqRecord()

    def rebuilt_by_species(self, fastaFile, fileName):
        for sequence in SeqIO.parse(fastaFile, 'fasta'):
            self.spName.add(str(sequence.name))
            if str(sequence.name) not in self.__seqs.keys():
                self.__seqs[str(sequence.name)] = [{fileName: str(sequence.seq)}]
            else:
                self.__seqs[str(sequence.name)].append({fileName: str(sequence.seq)})

    def get_sp_seqs(self):
        try:
            self.fileNames.extend(os.listdir(self.basePath))
        except Exception as e:
            print(e)
        # spName = set()
        # seqs = {}
        for file in self.fileNames:
            # print(os.path.join(basePath, file))
            file_name = file.split('.')[0]
            # print(file_name)
            self.rebuilt_by_species(os.path.join(self.basePath, file), file_name)

    def data_construction(self):
        self.get_sp_seqs()
        # data_temp = {}
        for sp in self.spName:
            if sp not in self.__data.keys():
                self.__data[sp] = self.__seqs[sp]
            else:
                self.__data[sp].update(self.__seqs[sp])

    def buildSeqRecord(self):
        for name in self.__data.keys():
            des = 'fileName'
            seq = ''
            for record in self.__data[name]:
                for key in record.keys():
                    des = des + ',' + str(key)
                    seq = seq + str(record[key])
            self.seqRecords.append(SeqRecord(id=name, seq=Seq(seq), name=name, description=des))

    def writeFasta(self):
        resName = input('请输入结果文件名')
        SeqIO.write(self.seqRecords, resName, 'fasta')

    def showFileName(self):
        # for file in self.fileNames:
        #     print(file)
        return self.fileNames

    def getSpeciesName(self):
        # for sp in self.spName:
        #     print(sp)
        return self.spName

    def getseqRecod(self):
        # for record in self.seqRecords:
        #     print(record)
        return self.seqRecords


if __name__ == '__main__':
    basePath = 'data/'
    rd = RebuildData(basePath)
    record = rd.getseqRecod()
    SeqIO.write(record, 'res.fasta', 'fasta')
