#!/usr/bin/env bash
#set -x

dir=bombs
rm -rf $dir
mkdir $dir

formats=$(python3 shadrak.py list)
num_formats=$(echo "$formats" | wc -l)
echo "Generating $num_formats bombs in ${dir}/"
echo "Arguments: $@"
echo "Formats: $(echo $formats)"
echo ""

for f in $formats
do
	echo "Generating $f"
	python3 shadrak.py $f -o ${dir}/bomb -q $@
    echo ""
done
echo ""
echo "########## All payloads generated ##########"
ls -la --block-size=M -S ${dir}/
