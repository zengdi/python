# 导入Biopython相关的包
from Bio import SeqIO
from Bio.Seq import Seq
# 设定终止密码子
codon_stop_array = ["TAA", "TA", "T", "TAG"]
# 打开一个文件用于存放结果
with open('test_res.fasta','w') as output:
    # 取得每个序列对象
    for record in SeqIO.parse("a6.nu.fas", "fasta"):
        print(len(record.seq))
        # 显示原始序列
        print('raw:',record.seq)
        # 判断原始序列是否可以被3整除
        n = len(record.seq) % 3
        print(n)
        # 如果不可以就删除末尾多余的碱基
        if n != 0:
            seq_data = str(record.seq)[:-n]
        # 如果可以整除，就保留原始序列
        else:
            seq_data = str(record.seq)
        # 显示新序列
        print('new:',seq_data)
        # 将序列的碱基序列转化为列表，即每个碱基是一个元素
        tempRecordSeq = list(seq_data)

        # 删除的是否是最后三位碱基标记
        flag = True
        # 每三个碱基取为一组与密码子比较
        for index in range(0, len(tempRecordSeq), 3):
            codon = tempRecordSeq[index:index+3]
            # 如果三个碱基组与密码子相同删除这三个碱基
            if ''.join(codon) in codon_stop_array:
                if index+3 != len(tempRecordSeq):
                    flag = False
                del tempRecordSeq[index:index+3]
        # 如果长度差等于3，则代表最后三位发现终止子，并用新序列替代原来的序列
        if len(seq_data) - len(Seq("".join(tempRecordSeq))) == 3 and flag:
            record.seq = Seq("".join(tempRecordSeq))
        # 如梦长度差等于0，则代表序列中没有发现终止子，并用新序列替代原来的序列
        elif len(seq_data) - len(Seq("".join(tempRecordSeq))) == 0:
            record.seq = Seq("".join(tempRecordSeq))
        # 如果最后的结果序列与原始序列长度不等于3，则在末尾添加ZZZ用于辨别中间有终止密码子的情况
        else:
            record.seq = Seq("".join(tempRecordSeq)) + Seq('Z')
        # 显示新的序列
        print('fin:',record.seq)
        # 把序列对象写出为fasta格式
        SeqIO.write(record, output, "fasta")

