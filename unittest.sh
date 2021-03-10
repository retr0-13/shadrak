#!/usr/bin/env bash
#set -x

dir=tests
rm -rf $dir
mkdir $dir

formats=$(python3 shadrak.py list)
num_formats=$(echo "$formats" | wc -l)
echo "Performing tests on $num_formats formats in ${dir}/"
echo "Formats: $(echo $formats)"
echo ""

for f in $formats
do
	echo "Testing $f"
	python3 shadrak.py $f -o ${dir}/bomb -q
    ls -la ${dir}/bomb.$f
    echo ""
done
echo ""
echo "########## Tests completed ##########"
ls -la --block-size=M -S ${dir}/
