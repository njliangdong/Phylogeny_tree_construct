cd /Users/liangdong/Downloads/iqtree-3.0.1-macOS
muscle -align 1.fa -output 1.afa
perl MFAtoPHY.pl 1.afa
./bin/iqtree3 -s 1.afa.phy -m MFP -alrt 1000 -B 1000 --prefix 1 -T AUTO