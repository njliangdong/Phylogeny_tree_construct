# Phylogeny_tree_construct
mafft --maxiterate 1000 --localpair All_NPP.fa >All_NPP.afa
Gblocks data.afa -t=p -b5=n
#perl MFAtoPHY.pl data.afa-gb
iqtree -s data.afa.phy -m MFP -alrt 1000 -B 1000 --prefix 1 -T AUTO

# 将domain及信号肽注释结果转化为ITOL网站需求格式，可在ITOL网站上将功能域分析结果与进化树整合
python convert_itol.py -i GH28.domain.txt -o itol.domain.upload.txt
转换成功！结果已保存至: itol.domain.upload.txt
