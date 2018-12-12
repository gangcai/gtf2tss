import argparse
import re
parser = argparse.ArgumentParser(description='Extract TSS from GTF file')
parser.add_argument('--flanking', dest="flanking",type=int,default=0,
		                    help='extend TSS by flanking size(default=0)')
parser.add_argument("--gtf",dest="gtf",type=str,help="GTF file")
parser.add_argument("--outfile",dest="outfile",type=str,help="output file new")

args=parser.parse_args()
gtf=args.gtf
flanking=args.flanking
outfile=args.outfile
#chr1    HAVANA  exon    13221   14409   .       +       .       gene_id "ENSG00000223972.5"; transcript_id "ENST00000456328.2"; gene_type "transcribed_unprocessed_pseudogene"; gene_name "DDX11L1"; transcript_type "processed_transcript"; transcript_name "RP11-34P13.1-002"; exon_number 3; exon_id
#read GTF file

def get_gene_name(gtf_items):
	last_info=gtf_items[-1]
	for p in last_info.split(";"):
		(type_,name_)=p.split()
		if type_ == "gene_name":
			return(re.sub("\"","",name_))
outfile=open(outfile,"w")
for line in open(gtf):
	if re.search("^#",line):
		continue
	items=line.rstrip().split("\t")
	chr_=items[0]
	type_=items[2]
	s_=items[3]
	e_=items[4]
	strand_=items[6]
	name=get_gene_name(items)
	if not type_ == "gene":
		continue
	if strand_ == "+":
		tss=int(s_)
		left_tss=tss-flanking
		right_tss=tss+flanking+1
		if left_tss<1:
			left_tss=1
		outfile.write(chr_+"\t"+str(left_tss)+"\t"+str(right_tss)+"\t"+name+"\t1000\t"+strand_+"\n")
	if strand_ == "-":
		tss=int(e_)
		left_tss=tss-flanking
		right_tss=tss+flanking+1
		if left_tss<1:
			left_tss=1
		outfile.write(chr_+"\t"+str(left_tss)+"\t"+str(right_tss)+"\t"+name+"\t1000\t"+strand_+"\n")
	#chr1    HAVANA  gene    11869   14409   .       +
outfile.close()
