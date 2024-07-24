import pprint as pp
import psicalc as pc

# data1 = pc.durston_schema(pc.read_csv_file_format("../Histone H3 105 seq alignment.csv"), 1)
# data1 = pc.read_txt_file_format("/Users/mas/Downloads/CDT1 CompSeq Revised v2.txt")
data1 = pc.read_csv_file_format("../Histone H3 105 seq alignment.csv")
data1 = data1.replace({'[-#?.]': None}, regex=True)
data1 = pc.durston_schema(data1, 1)

# data2 = pc.read_txt_file_format("/Users/mas/Downloads/TOP2A CompSeq USE THIS ONE v2.txt")
# data2 = data2.replace({'[-#?.]': None}, regex=True)
# data2 = pc.deweese_schema(data2, 'None')

msa = pc.merge_sequences([data1], ['A'])
result = pc.find_clusters(1, msa, "pairwise", 0.0)

pp.pprint(result)
